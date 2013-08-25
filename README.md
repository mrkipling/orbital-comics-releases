<a href="http://www.orbitalcomics.com/"><img src="http://i.imgur.com/dPDgZqG.png" width="300" height="114" alt="Orbital Comics logo"></a>

## Orbital Comics new releases email tool

**Author**: [Bradley Abrahams](https://github.com/mrkipling)

## What is this?

[Orbital Comics](http://www.orbitalcomics.com/) is a very cool comic book shop in Central London.

New comics are consistently released every Wednesday. I decided to write a simple script to email me every Wednesday morning with a list of new comic releases that week, mostly for fun, but also because it's kind of nice having an automated reminder in my inbox.

It also takes an array of comics that I am particularly interested in, and if it finds them in the list it highlights them at the top of the email. Now I'll never miss a copy of The Walking Dead!

## What do the emails looks like?

They look pretty basic, but they get the job done.

<img src="http://i.imgur.com/a1zWdp1.png" alt="Preview of an email">

## How to use this

It should be set up as a cron job on a VPS, home server, Raspberry Pi, basically any PC that is on at the time that it emails you.

It has some requirements, most notably BeautifulSoup (pip install beautifulsoup4). I decided to not bundle everything as I wanted to keep this as simple as possible (just a script).

**This is a work in progress.** I plan on making it better and adding some proper usage instructions. In the meantime just take a look at the script, it should be fairly self-explanatory.

## Please note...

I am not affiliated with Orbital Comics in any way. It is just a fun, not-for-profit project that I wrote for myself and thought that other people might find useful.
