<a href="http://www.orbitalcomics.com/"><img src="http://i.imgur.com/dPDgZqG.png" width="300" height="114" alt="Orbital Comics logo"></a>

## Orbital Comics new releases email tool

**Author**: [Bradley Abrahams](https://github.com/mrkipling)

## What is this?

[Orbital Comics](http://www.orbitalcomics.com/) is a very cool comic book shop in Central London.

New comics are consistently released every Wednesday. I decided to write a simple script to email me every Wednesday morning with a list of new comic releases that week, mostly for fun, but also because it's kind of nice having an automated reminder in my inbox.

It also takes an array of comics that I am particularly interested in, and if it finds them in the list it highlights them at the top of the email. Now I'll never miss a copy of The Walking Dead!

**Warning!** This script guesses URLs based on dates and uses BeautifulSoup to parse the contents of a blog. As such it is rather flaky. Expect it to break occasionally!

## How to use this

First of all, you need to fill out the "customisable settings" section in the script. Basically you need to enter an email address, password, and SMTP server (I've pre-filled it with Gmail's, assuming that you'll probably just use a Gmail account to send from). You can also populate the FAVOURITE_COMICS array while you're there.

The script should be set up as a cron job on a VPS, home server, Raspberry Pi... basically any PC that is on at the time that it emails you.

It has some requirements, most notably BeautifulSoup (pip install beautifulsoup4). I decided to not bundle everything as I wanted to keep this as simple as possible (just a single script).

There are some command line switches that you can use:

    python orbital.py --date=21-08-2014

Supplying a date with the --date switch (in DD-MM-YYYY format) will use that date. Useful if you want to try it out, as otherwise the script only works on Comic Book Wednesday!

    python orbital.py --console

This will print the email body to the console and won't actually send an email. Not really all that useful I guess, but handy for testing.

## Adding the script to crontab

Open your crontab file for editing (on the server that will be sending the email):

    sudo crontab -e

Add the following line to make the script run every Wednesday at 4am (so that you have the email in your inbox when you wake up). Make sure to change the path name to point to the actual location of the script!

    0 4 * * 3 python /path/to/orbital.py

In this example 0 = 0 minutes, 4 = the 4th hour (i.e. 04:00am), the asterisks skip the next two settings, and 3 = day of week (Wednesday). The rest is the command that we are running (the script). The above info should allow you to modify the crontab setting to suit your requirements (change 4 to 10 if you want the email to be sent at 10am, for example).

## Please note...

I am not affiliated with Orbital Comics in any way. This is just a fun, not-for-profit project that I wrote for myself and thought that other people might find useful, so I decided to play nice and share.

## If you were wondering what the emails look like...

<img src="http://i.imgur.com/a1zWdp1.png" alt="Preview of an email">
