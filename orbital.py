#!/bin/env python

import sys
import re
import datetime
import urllib2
import smtplib
from bs4 import BeautifulSoup

# requirements: BeautifulSoup (pip install beautifulsoup4)

# This script scrapes the new comic releases from the Orbital comics website (http://www.orbitalcomics.com) and emails them to you.
# You should set it up as a cron job to run every Wednesday whenever you like (early in the morning perhaps?)
#
# By default you can just run the script and, assuming it is run on Comic Book Wednesday, it will use today's date.
# However you can supply an arg in the DD-MM-YYYY format which it will use instead (for testing purposes mostly).
#
# You need to change the EMAIL SETTINGS section directly below with mail server setings.
# You can also edit the FAVOURITE_COMICS array (stright after email settings) which will push them to the top of your email, highlighted in red.
# Basically this will tell you when The Walking Dead (or whatever you're into) is released at the very top of the email. Never miss a comic again.

# Here we go. Good luck!



# EMAIL SETTINGS

receiver_name = '' # where you want to receive the email
receiver_email = '' # who the email should come from

gmail_from_name = '' # gmail account used to sned the email; name of account owner
gmail_from = ''  # gmail account used to sned the email; account name / login
gmail_password = ''      # gmail account used to sned the email; password



# Your favourite comics. These comics will be highlighted in red at the top of the enail.
# List your favourite comics in this array so that you don't miss them. Partial text match.

FAVOURITE_COMICS = [
    'Walking Dead', 'Sheltered', 'Dexter'
]



# And now the actual code

if len(sys.argv) > 1:
    # arg should be date in this format: 24-08-2013 (i.e. DD-MM-YYYY)
    date = sys.argv[1]

    if len(date) != 10:
        raise Exception("Incorrect date formatting.")

else:
    # if no arg supplied, get current date, and hope it's a Wednesday
    weekday = datetime.date.today().strftime("%w")

    if weekday != "3": # Weds
        raise Exception("Today is not a new comic day!")

    date = datetime.date.today().strftime("%Y-%m-%d")

fancy_date = date # nicely formatted date for the email
date = date.replace('-', '')

# fetch the comic list and parse it
url = "http://www.orbitalcomics.com/new-comics-week-of-%s/" % (date)
html = urllib2.urlopen(url).read()
soup = BeautifulSoup(html)

# get rid of sharing buttons HTML
content = soup.find(class_='entry-content')
content.find(class_='share-buttons').extract()

# get rid of all div.clear
clears = content.findAll(class_='clear')
[clear.extract() for clear in clears]

# find interesting comics, place them at the top of the email

interesting = []

for comic in FAVOURITE_COMICS:
    comic_search = content.find(text=re.compile(comic))
    if comic_search:
        interesting.append(comic_search)

interesting_msg = '<p style="font-size: 16px; font-weight: bold;">There are no new interesting releases this week. Sorry!</p><p>But why not take a look at what else is on offer...</p>'

if len(interesting) > 0:
    interesting_msg = '<p style="font-size: 16px; font-weight: bold;">New / interesting comics this week</p>'
    interesting_msg += '<ul style="color: red">'
    for msg in interesting:
        interesting_msg += '<li>%s</li>' % (msg.encode('utf-8'))
    interesting_msg += '</ul>'

# format and send the email
message = """From: %s <%s>
To: %s <%s>
MIME-Version: 1.0
Content-type: text/html
Subject: New Orbital comic releases on Wednesday %s

%s
<p style="font-size: 16px; font-weight: bold;">Other Orbital Comics releases on Wednesday %s</p>

%s
""" % (gmail_from_name, gmail_from, receiver_name, receiver_email, fancy_date, interesting_msg, fancy_date, content)

try:
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(gmail_from, gmail_password)
    server.sendmail(gmail_from, receiver_email, message)
    server.quit()

except:
    raise Exception("There was a problem sending the email.")
