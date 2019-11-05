from praw import Reddit
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from os import getenv, environ
from dotenv import load_dotenv
from pathlib import Path


def parsemsg(s):
  s = s[1:]
  command = s.split(" ")[1]
  nick = s[:s.find("!")]
  message = s[s.find(":") + 1:].replace("\r\n", "")

  return (nick, command, message)


def send_data(command):
    IRC.send((command + "\n").encode())


def login(nickname, password, channel):
    send_data("PASS " + password)
    send_data("NICK " + nickname)
    send_data("JOIN #%s" % channel)


def send_msg(msg):
    IRC.send(("PRIVMSG #{} : {}\n".format(CHANNEL, msg)).encode())
    print(NICK + " -> " + msg)


# Check arguments or .env
if len(argv) != 6:
  env_path = Path('.') / '.env'
  load_dotenv(dotenv_path=env_path)
  for e in ["CLIENTID", "CLIENTSEC", "NICK", "ACCESS_TOKEN", "CHANNEL"]:
    if e not in environ or getenv(e) is "":
      print('Incorrect number of arguments or .env not configured')
      exit()

# Set all the variables necessary to connect to Reddit
CLIENTID = getenv("CLIENTID") or argv[1]
CLIENTSEC = getenv("CLIENTSEC") or argv[2]
# As well as Twitch IRC
NICK = getenv("NICK") or argv[3]
ACCESS_TOKEN = getenv("ACCESS_TOKEN") or argv[4]
CHANNEL = getenv("CHANNEL") or argv[5]

# Connect to Reddit api
reddit = Reddit(client_id=CLIENTID,
                client_secret=CLIENTSEC,
                user_agent="windows:FromReddit(https://github.com/Tarasa24/FromReddit):v0.1 (by /u/Tarasa24_CZE)")

# Open up a socket and login
IRC = socket(AF_INET, SOCK_STREAM)
IRC.connect(("irc.twitch.tv", 6667))
IRC.setblocking(False)
login(NICK, ACCESS_TOKEN, CHANNEL)

while True:
  try:
    buffer = IRC.recv(1024)
    msg = parsemsg(buffer.decode())
    if msg[1] == "PING":
      send_data("PONG tmi.twitch.tv\r\n")  # Answer with pong as per RFC 1459
    elif msg[1] == "PRIVMSG":
      print(msg[0] + " -> " + msg[2])
      if msg[2] == "!question":
        for submission in reddit.subreddit("askreddit").random_rising(limit=1):
          send_msg("\"{}\"".format(submission.title))
  except BlockingIOError:
    pass
