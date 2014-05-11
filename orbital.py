#!/bin/env python

# Orbital Comics new releases email tool
# Author: Bradley Abrahams
# Available on GitHub: https://github.com/mrkipling/orbital-comics-releases
#
# Requirements: BeautifulSoup (pip install beautifulsoup4)
#               Click         (pip install click)
#
# This script scrapes the new comic releases from the Orbital comics website
# (http://www.orbitalcomics.com) and emails them to you. You should set it up as
# a cron job to run every Wednesday whenever you like (early in the morning
# perhaps - I go for 4am).
#
# By default you can just run the script and, assuming it is run on Comic Book
# Wednesday, it will use today's date. If it is not Wednesday then the script
# will figure out the date of the next Wednesday and use that. However you can
# optionally supply an arg in the DD-MM-YYYY format which it will use instead,
# like so: python orbital.py --date=21-08-2013
#
# You need to edit the EMAIL SETTINGS section directly below with mail server
# setings.
#
# You can also edit the FAVOURITE_COMICS array (straight after email settings).
# This will push your favourite comics to the top of your email in their own
# special section. You need not ever miss a comic again! If you don't want this
# feature then just leave the array empty.

import sys
import re
import datetime
import urllib2
import smtplib
import click
from bs4 import BeautifulSoup



### CUSTOMISABLE SETTINGS

# email address where the email should be sent to
receiver_email = ''

# email account used to send the email; leave as-is to use the same address
sender_email = receiver_email

# password for the email account that you are sending the mail from
sender_password = ''

# your name (or whatever you want the email to say it is "from")
sender_name = ''

# SMTP server (if sending from a Gmail account then leave it as-is)
smtp_server = 'smtp.gmail.com:587'

# List your favourite comics in this array to have them appear in their own
# section at the top of the email. Partial text match, case-insensitive.
# Example: FAVOURITE_COMICS = ["Walking Dead", "Sheltered", "Sidekick"]
FAVOURITE_COMICS = []



### And now the actual code

@click.command()
@click.option('--date', default='today', help='the date that you wish to receive an update for (DD-MM-YYYY) - if not specified then next Wednesday will be used')
@click.option('--console', is_flag=True, help='log just your new comics to the console')
def orbital(date, console):
    send_email = True

    if date == 'today':
        date = datetime.date.today().strftime("%d-%m-%Y")

        weekday = int(datetime.date.today().strftime("%w"))

        if weekday < 3: # Weds
            days = 3 - weekday
        elif weekday > 3:
            days = 10 - weekday
        else:
            days = 0

        date = datetime.date.today() + datetime.timedelta(days=days)
        date = date.strftime("%d-%m-%Y")

    if len(date) < 10:
        raise Exception("Incorrect date formatting.")

    fancy_date = date # nicely formatted date for the email
    date = date.replace('-', '')

    if console:
        send_email = False

    # fetch the comic list and parse it

    url = "http://www.orbitalcomics.com/new-comics-week-of-%s/" % (date)

    try:
        html = urllib2.urlopen(url).read()

    except:
        date = datetime.date.today().strftime("%d%m%y")
        url = "http://www.orbitalcomics.com/new-comics-week-of-%s/" % (date)
        html = urllib2.urlopen(url).read()

    soup = BeautifulSoup(html)

    # get rid of sharing buttons HTML
    content = soup.find(class_='entry-content')
    content.find(class_='share-buttons').extract()

    # get rid of all div.clear
    clears = content.find_all(class_='clear')
    [clear.extract() for clear in clears]

    # tweak styling of subheadings
    subtitles = content.find_all('strong')
    for subtitle in subtitles:
        subtitle['style'] = 'display: block; font-size: 16px;'
        subtitle.insert_before(soup.new_tag('br'))

    # find interesting comics so that they can be placed at the top of the email

    interesting = []

    for comic in FAVOURITE_COMICS:
        comic_search = content.find_all(text=re.compile(comic, re.IGNORECASE))
        if comic_search:
            interesting.extend(comic_search)

    if console:
        if len(interesting) == 0:
            print "None of your favourite comics have been released this week. Bugger!"
            return

        click.echo("\nOrbital: your favourite comics released today, %s\n" % fancy_date)

        for comic in interesting:
            click.echo(comic.replace('\n', ''))

        click.echo('\nSee the full list at %s\n' % url)
        return

    interesting_msg = '<p>None of your favourite comics have been released this \
    week. Bugger!</p><p>Why not take a look at what else is on offer though?</p>'

    if len(interesting) > 0:
        interesting_msg = '<p>'
        for comic in interesting:
            interesting_msg += '%s<br />' % (comic.encode('utf-8'))
        interesting_msg += '</p>'

    # format and send the email
    message = """From: %s <%s>
    To: %s
    MIME-Version: 1.0
    Content-type: text/html
    Subject: New Orbital comic releases, Wednesday %s

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html>
        <head>
            <title></title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta name="viewport" content="width=320, target-densitydpi=device-dpi" />
        </head>
        <body>
            <table width="100%%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td style="background-color: #6596C7; color: #fff;
                               font: bold 16px Arial, Helvetica, sans-serif;
                               padding: 7px 10px;">
                        <a href="%s" style="color: #fff; text-decoration: none;">
                            Orbital: your favourite comics released today, %s
                        </a>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px;
                               font: 13px/20px Arial, Helvetica, sans-serif;">
                        %s
                        <br />
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #6596C7; color: #fff;
                               font: bold 16px Arial, Helvetica, sans-serif;
                               padding: 7px 10px;">
                        Other new comics released today
                    </td>
                </tr>
                <tr>
                    <td id="new_comics" style="padding: 0 10px 10px;
                               font: 13px/20px Arial, Helvetica, sans-serif;">
                        %s
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """ % (sender_name, sender_email, receiver_email, fancy_date, url, fancy_date, \
               interesting_msg, content)

    if send_email:
        server = smtplib.SMTP(smtp_server)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()

    else:
        click.echo(message)

if __name__ == '__main__':
    orbital()
