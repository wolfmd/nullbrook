#!/usr/bin/python
#
# Name rss-to-tumblr.py
#
# Requires:
# pip install requests pytumblr
#
# Usage ./rss-to-tumblr.py
#                               -k, --consumer-key CONSUMER_KEY
#                               -c, --consumer-secret CONSUMER_SECRET
#                               -t. --title TITLE
#                               -d, --description DESC
#                               -l, --link LINK
#                               -o, --oauth OAUTH
#                               -s, --secret SECRET
#

import argparse
import datetime
import pytumblr
import sys
import urllib2
from lxml import etree as ET

# I'm a monster
def send_to_tumblr(consumer_key, consumer_secret, oauth_key, oauth_secret, title, content, link):
    client = pytumblr.TumblrRestClient(consumer_key,consumer_secret,oauth_key,oauth_secret)
    # Just a little nastiness to prevent some nastiness
    slug = urllib2.quote(title.translate(None, '-'.join(' ')).encode("utf8"))
    client.create_text("boxesofoldphotos", state="queue", slug=slug, title=title, body="%s <a href=\"%s\"><br>Read the rest of this post on Nullbrook.org</a>" % (content,link))

def get_content_from_file(input_file):
    with open(input_file, 'r') as feed:
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(input_file, parser)
        channel = tree.getroot()
        for item in channel.iter('item'):
            title = item.find('title').text
            content = item.find('description').text
            link = item.find('link').text
            break

    return title, content, link


parser = argparse.ArgumentParser(description='Send something sweet to your friends at Tumblahoo?', prog='rss-to-tumblr.py')

parser.add_argument('-t','--title',
                            help='title the title of the post to be created',
                            required=False)
parser.add_argument('-d','--description',
                            help='the content of the post to be created',
                            required=False)
parser.add_argument('-l','--link',
                            help='the link to the blog post',
                            required=False)
parser.add_argument('-i','--input_file',
                            help='the input XML file',
                            required=False)
parser.add_argument('-k','--consumer_key',
                            help='the consumer key of the Tumblr blog',
                            required=True)
parser.add_argument('-c','--consumer_secret',
                            help='the consumer secret of the Tumblr blog',
                            required=True)
parser.add_argument('-o','--oauth_key',
                            help='the oauth key (thanks tumblr)',
                            required=True)
parser.add_argument('-s','--oauth_secret',
                            help='the oauth secret (thanks tumblr)',
                            required=True)

args = parser.parse_args()


if args.input_file:
    title, content, link = get_content_from_file(args.input_file)
else:
    if not args.title or not args.description or not args.link:
        print "Did you forget something, fella? Give me an -i or give me an -ltd"
        sys.exit()

    title = args.title
    content = args.description
    link = args.link

print "Posting the following message to Tumblr: \n%s\n%s\n%s" % (title, content, link)
send_to_tumblr( args.consumer_key,
                args.consumer_secret,
                args.oauth_key,
                args.oauth_secret,
                title,
                content,
                link
            )
