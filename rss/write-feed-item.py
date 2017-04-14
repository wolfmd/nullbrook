#!/usr/bin/python
#
# Name write-feed-item.py
#
# Requires:
# pip install pyrss2gen
#
# Usage ./write-feed-item.py feedgen
#                               -t. --title TITLE
#                               -d, --description DESC
#                               -o, --output OUTPUT (default feed.xml)
#
#                            Append an entry to the feed
#                            entry
#                               -t --title TITLE
#                               -d --description DESC
#                               -l --link LINK
#                               -i --input INPUT
#

import argparse
import datetime
import PyRSS2Gen
from lxml import etree as ET

def write_new_file(title, description, link, output_file):
    rss = PyRSS2Gen.RSS2(
    title = title,
    link = link,
    description = description,
    lastBuildDate = datetime.datetime.now(),

    items = [
    ])

    rss.write_xml(open("feed.xml", "w"))

def write_new_entry(title, description, link, input_file):
    tree = ''
    with open(input_file, 'r') as feed:
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(input_file, parser)
        channel = tree.getroot()
        item = ET.SubElement(channel, "item")
        xmltitle = ET.SubElement(item, "title")
        xmltitle.text = title
        xmllink = ET.SubElement(item, "link")
        xmllink.text = link
        xmldescription = ET.SubElement(item, "description")
        xmldescription.text = description

        channel.find(".//docs").addnext(item)

        print ET.tostring(channel, pretty_print=True, xml_declaration=True)
        tree = ET.ElementTree(channel)
        feed.close()https://www.sub.fm/

    with open(input_file, 'w') as feed:
        tree.write(feed, pretty_print=True, xml_declaration=True)
        feed.close()


parser = argparse.ArgumentParser(description='Play with some RSS stuff.', prog='write-feed-item.py')
subparsers = parser.add_subparsers(dest='subprogram',
                                   help='sub-command help')

#Feedgen command
parser_feedgen = subparsers.add_parser('feedgen',
                                        help='feedgen [-t, --title TITLE]'
                                        '[-d, --description DESC]'
                                        '[-o, --output OUTPUT]')
parser_feedgen.add_argument('-t','--title',
                            help='title the title of the feed to be created',
                            required=True)
parser_feedgen.add_argument('-d','--description',
                            help='the description of the feed to be created',
                            required=True)
parser_feedgen.add_argument('-l','--link',
                            help='the link for the feed',
                            required=True)
parser_feedgen.add_argument('-o','--output_file', help='the output file, defaults to \'feed.xml\'', default='feed.xml')

#Entry command
parser_entry = subparsers.add_parser('entry',
                                        help='entry [-t, --title TITLE] '
                                        '[-d, --description DESC]'
                                        '[-l, --link LINK]'
                                        '[-i, --input_file INPUT_FILE]')
parser_entry.add_argument('-t',
                            '--title',
                            help='-t: title the title of the feed entry',
                            required=True)
parser_entry.add_argument('-d','--description',
                            help='the description of feed entry',
                            required=True)
parser_entry.add_argument('-l','--link',
                            help='the link for the feed entry',
                            required=True)
parser_entry.add_argument('-i','--input_file',
                            help='the input XML file',
                            required=True)

args = parser.parse_args()

if 'entry' == args.subprogram:
    write_new_entry(args.title, args.description, args.link, args.input_file)
elif 'feedgen' == args.subprogram:
    write_new_file(args.title, args.description, args.link, args.output_file)
