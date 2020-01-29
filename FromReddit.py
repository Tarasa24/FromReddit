from praw import Reddit
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv, exit
from os import getenv, environ
from dotenv import load_dotenv
from pathlib import Path
from time import sleep
import contextlib
from urllib.parse import urlencode
from urllib.request import urlopen
import atexit
from random import shuffle


def signoff(history):
  if history >= 10:
    send_msg("Shameless self-promotion https://github.com/Tarasa24/FromReddit OpieOP")
  print(" > Served {} question(s)".format(history))
  print(" > See ya later o/")
  sleep(3)
  exit()


def make_tiny(url):
  request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url': url}))
  with contextlib.closing(urlopen(request_url)) as response:
    return response.read().decode('utf-8 ')


def parsemsg(s):
  if s[0] is ":":
    s = s[1:]
    command = s.split(" ")[1]
    nick = s[:s.find("!")]
    message = s[s.find(":") + 1:].replace("\r\n", "")

    return {"nick": nick, "command": command, "message": message}
  else:  # Ping edge case
    command = s.split(" ")[0]

    return {"nick": None, "command": command, "message": None}


def send_data(command):
  IRC.send((command + "\n").encode())


def login(nickname, password, channel):
  send_data("PASS " + password)
  send_data("NICK " + nickname)
  send_data("JOIN #%s" % channel)


def send_msg(msg):
  IRC.send(("PRIVMSG #{} : {}\n".format(CHANNEL, msg)).encode())
  print(NICK + ": " + msg)


def getRedditPost(pool):
  for random in pool:
    if random.num_comments >= 20:
      return random
  else:
    return askReddit.random()


# Check arguments or .env
if len(argv) != 6:
  env_path = Path('.') / '.env'
  load_dotenv(dotenv_path=env_path)
  for e in ["CLIENTID", "CLIENTSEC", "NICK", "ACCESS_TOKEN", "CHANNEL"]:
    if e not in environ or getenv(e) is "":
      print('> Incorrect number of arguments or .env not configured')
      sleep(3)
      exit()

# Set all the variables necessary to connect to Reddit
CLIENTID = getenv("CLIENTID") or argv[1]
CLIENTSEC = getenv("CLIENTSEC") or argv[2]
# As well as Twitch IRC
NICK = getenv("NICK") or argv[3]
ACCESS_TOKEN = getenv("ACCESS_TOKEN") or argv[4]
CHANNEL = getenv("CHANNEL") or argv[5]
print(" > Variables loaded")

# Connect to Reddit api
reddit = Reddit(client_id=CLIENTID,
                client_secret=CLIENTSEC,
                user_agent="windows:FromReddit(https://github.com/Tarasa24/FromReddit):v0.1 (by /u/Tarasa24_CZE)")
print(" > Praw initiliazed")

pool = []
askReddit = reddit.subreddit("askreddit")
pool = list(askReddit.hot(limit=500)) + list(askReddit.random_rising(limit=500))
shuffle(pool)
print(" > Pool of {} questions prepared".format(len(pool)))

# Open up a socket and login
IRC = socket(AF_INET, SOCK_STREAM)
IRC.connect(("irc.twitch.tv", 6667))
IRC.setblocking(False)
login(NICK, ACCESS_TOKEN, CHANNEL)
print(" > Twitch IRC connected")

history = 0
atexit.register(signoff, history)

print(" > Listening for new messages")
try:
  while True:
    sleep(0.1)
    try:
      buffer = IRC.recv(1024)
      msg = parsemsg(buffer.decode())
      if msg["command"] == "PING":
        send_data("PONG tmi.twitch.tv\r\n")  # Answer with pong as per RFC 1459
      elif msg["command"] == "PRIVMSG":
        if msg["message"].find(chr(1) + "ACTION") == 0 and msg["message"][-1] == chr(1):  # /me edge case
          msg["message"] = "/me " + msg["message"][8:-1]

        print(msg["nick"] + ": " + msg["message"])

        if msg["message"] == "!question":
          random = getRedditPost(pool)
          pool.remove(random)
          history += 1
          atexit.unregister(signoff)
          atexit.register(signoff, history)
          
          send_msg("\"{}\" ( ⬆️  {}  🗨️  {}  🔗  {} )".format(random.title, random.score, random.num_comments, make_tiny(random.url)))
        elif msg["message"] == "!author":
          send_msg("Made with <3 by @Tarasa24 https://github.com/Tarasa24")
    except BlockingIOError:
      pass
except KeyboardInterrupt:
  exit()
