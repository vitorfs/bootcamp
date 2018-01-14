# Bootcamp

[![Build Status](https://travis-ci.org/vitorfs/bootcamp.svg?branch=master)](https://travis-ci.org/vitorfs/bootcamp) [![Coverage Status](https://coveralls.io/repos/github/vitorfs/bootcamp/badge.svg?branch=master)](https://coveralls.io/github/vitorfs/bootcamp?branch=master) [![Requirements Status](https://requires.io/github/vitorfs/bootcamp/requirements.svg?branch=master)](https://requires.io/github/vitorfs/bootcamp/requirements/?branch=master)

Bootcamp is an open source **enterprise social network** built with [Python][0] using the [Django Web Framework][1].

The project has four basic apps:

* Feed (A Twitter-like microblog)
* Articles (A collaborative blog)
* Question & Answers (A Stack Overflow-like platform)
* Messenger (A basic chat-a-like tool for asynchronous communication.)

## Feed App

The Feed app allows you to check the most recent activity in the network through limited scrolling, also includes activity notifications, live updates for likes and comments, and comment tracking.

## Articles App

The Articles app is a basic blog, with articles pagination, tag filtering and draft management.

## Question & Answers App

The Q&A app works just like Stack Overflow. You can mark a question as favorite, vote up or vote down answers, accept an answer and so on.

## Messenger

The messenger app works at a basic level, in the same way tools like Slack or MatterMost (not there yet in that level of functionality, but it manages to deliver).

## Technology Stack

* Python 2.7 / 3.6
* Django > 1.9
* Twitter Bootstrap 3
* jQuery 2
* Redis 3.0
* WebSockets (Using django-channels for that!)

## Installation Guide

Take a look at our wiki page for a detailed [installation guide][3].

## Demo

Try Bootcamp now at [http://trybootcamp.vitorfs.com][2].

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
[2]: http://trybootcamp.vitorfs.com/
[3]: https://github.com/vitorfs/bootcamp/wiki/Installing-and-Running-Bootcamp
