<center>
<img align="left" width="128" src="https://i.imgur.com/s4eR1Vn.png">
<h1>FromReddit</h1>
Simple Twitch IRC chatbot for displaying r/AskReddit questions on demand
</center> 
</br>

---

## Table of contents

- [General info](#general-info)
- [Technologies](#technologies)
- [Requirements and Setup](#requirements-and-setup)
  - [Reddit](#Reddit)
  - [Twitch](#Twitch)
  - [conf.ini](#conf.ini)
  - [pip](#pip)
- [Execution](#execution)

## General info

Have you ever felt like your chat is too silent? Like there isn't anything to discuss that haven't been discussed? Well what about you shoot some interesting question from r/AskReddit. That will surely evoke some kind of response. From your favorite movie quote to the multiverse theory, FromReddit got you covered.

![Screenshot_01](https://i.imgur.com/iTgRx06.png)
![Screenshot_02](https://i.imgur.com/Q0z11yd.png)
![Screenshot_03](https://i.imgur.com/Qhz93mi.png)
![Screenshot_04](https://i.imgur.com/KzQwDRD.png)

## Technologies

Project is created with:

- <a href="https://github.com/praw-dev/praw" target="_blank">Python Reddit API Wrapper</a>

## Requirements and Setup

#### Reddit

Head to [Reddit's developed applications page](https://www.reddit.com/prefs/apps) and create a new app. Give it a sexy name, **select script**, and put `http://localhost` to the redirect url box.
![Reddit developer create](https://i.imgur.com/ID5d1VH.png)

If all done well, you should end up with a created application (as shown in the image below). From there you should take note of two things, **client id** and **client secret**. In this case:

```py
CLIENTID = "Gz4oQcPJ3Tj03A"
CLIENTSEC = "qjx4d77aFSgsO7bHKMeOtmq4GP0"
```

![Reddit developer app details](https://i.imgur.com/cOh6DML.png)

#### Twitch

Head over to my go to [twitch oauth generator](https://twitchtokengenerator.com/quick/p7xAbpkovt), log in with yours (alternatively your bots) account and authorize. Expected result should look something like this and the part you are interested in is the `ACCESS TOKEN`.
![twitchtokengenerator token](https://i.imgur.com/ye7dMEl.png)

#### conf.ini

FromReddit requires to have all the necessary data to be stated in the `conf.ini` file as shown below. Said file can be edited either manually, or using the installer.

```ini
[Reddit]
CLIENTID=Gz4oQcPJ3Tj03A
CLIENTSEC=qjx4d77aFSgsO7bHKMeOtmq4GP0

[Twitch]
NICK=FromReddit
PASS=oauth:aBR6kSj2OdxdwR6zcQXlEG6M4ZdNer
CHANNEL=bobross

[Misc]
TIMEOUT=10
```

#### pip

> This step isn't necessary if using the executable

```
pip install -r requirements.txt
```

## Execution

```
py FromReddit.py
```

or run

```
FromReddit.exe
```
