#!/usr/bin/python
#
# Name bulk-photo-queue.py
# Description: Posts photos from a directory to a desired blog in an unordered way
# while being careful not to post the same file twice
#
# Requires:
# pip install requests pytumblr
#
# Usage ./bulk-photo-queue.py
#                               -n, --number NUMBER default: 1
#                               -d, --directory DIRECTORY
#                               -p, --post POST [OPTIONAL]
#                               -k, --consumer-key CONSUMER_KEY
#                               -c, --consumer-secret CONSUMER_SECRET
#                               -o, --oauth OAUTH
#                               -s, --secret SECRET
#

import argparse
import datetime
import os
import pytumblr
import random
import sys
import time
import json
import urllib2


def load_database(database_file):
    try:
        previously_posted_files = json.loads(open(database_file).read())
    except IOError:
        while True:
            print "Couldn't find the old previously posted files database. Want to create one now? Y/N"
            choice = raw_input(">")
            if str(choice.lower()) == "y":
                with open("prev.json", 'w') as d:
                    d.write("[]")
                previously_posted_files = []
                database_file = "prev.json"
                break
            elif str(choice.lower()) == "n":
                print "Oh okay"
                previously_posted_files = []
                database_file = "prev.json"
                break
            else:
                print "I didn't understand what you said, I'm just going to ignore that."
    return previously_posted_files, database_file

def get_file_info(files, previously_posted_files, directory, rotations):
    # Generate a list of all files in a directory. Done once
    if not files:
        files = [os.path.join(path, filename)
             for path, dirs, files in os.walk(directory)
             for filename in files]
        if rotations > len(files):
            print "ERROR: Not enough unused photos in the directory. Enter a new number or erase the prev.json file."
            sys.exit()
    looking_for_file = True
    while looking_for_file is True:
        chosen_file = random.choice(files)
        previous_set = set(previously_posted_files)
        if not chosen_file in previous_set:
            previously_posted_files.append(chosen_file)
            looking_for_file = False
            break
        else:
            print "Maybe you're out of photos, bub"
            time.sleep(10)

    #test_set=set(test_list)
    filename = chosen_file.split('/')[-1]
    lot = chosen_file.split('/')[-2]
    fullname = urllib2.quote(chosen_file.encode("utf8"))
    return previously_posted_files, filename, fullname, lot, files, chosen_file

def send_to_tumblr(consumer_key, consumer_secret, oauth_key, oauth_secret, content, link, title, tags, chosen_file):
    client = pytumblr.TumblrRestClient(consumer_key,consumer_secret,oauth_key,oauth_secret)
    # Just a little nastiness to prevent some nastiness
    slug = urllib2.quote(title.translate(None, '-'.join(' ')).encode("utf8"))
    client.create_photo("boxesofoldphotos", state="queue", slug=slug, caption=content, data=chosen_file, tags=tags)

def update_database(previously_posted_files, database):
    with open(database, 'w') as f:
        f.write(json.dumps(previously_posted_files))

parser = argparse.ArgumentParser(description='Queue up posts and avoid Tumblr\'s awful GUI', prog='bulk-photo-queue.py')


parser.add_argument('-p','--post',
                            help='the content of the post to be created',
                            required=False)
parser.add_argument('-n','--rotations',
                            type=int,
                            default=1,
                            help='the number of photos to queue up',
                            required=False)
parser.add_argument('-i','--database',
                            default='prev.json',
                            help='a file containing previously posted files',
                            required=False)
parser.add_argument('-d','--directory',
                            help='the directory from which to submit files',
                            required=True)
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

# "database" ;)
database = args.database
previously_posted_files, database = load_database(database)

files = []

for index in range(args.rotations):
    previously_posted_files, filename, fullname, lot, files, chosen_file = get_file_info(files, previously_posted_files, args.directory, args.rotations)
    title = filename.split(".")[0]
    link = "ftp://nullbrook.org/" + fullname[8:]
    content = args.post if args.post else "%s<br><a href=\"%s\">View at Nullbrook</a>" % (filename.split(".")[0], link)
    tags = ["%sLot" % lot , "old photo"]

    print "Posting the following message to Tumblr: \n%s\n%s\n%s" % (title, content, link)
    send_to_tumblr( args.consumer_key,
                    args.consumer_secret,
                    args.oauth_key,
                    args.oauth_secret,
                    content,
                    link,
                    title,
                    tags,
		    chosen_file
                )

update_database(previously_posted_files, database)
