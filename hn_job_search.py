#!/usr/bin/python

import argparse

from firebase import firebase

import hnapi

"""
searches the hackernews firebase API for 'whoishiring' submissions that match the given date.
if no date is supplied, it will output the comments from 'whoishiring's latest submission
"""

api = hnapi.HNAPI()
parser = argparse.ArgumentParser(description='Hacker News Job Search')
parser.add_argument('--date', dest='date', type=str, help='month year string, e.g. \'January 2015\'', required=True)
parser.add_argument('--hiring', action='store_true', dest='hiring', help='only search the \'who is hiring\' threads')
parser.add_argument('--hired', action='store_true', dest='hired', help='only search the \'who is looking to be hired\' threads')
parser.add_argument('--freelance', action='store_true', dest='freelance', help='only search the \'freelancer\' threads')
parser.add_argument('--all', action='store_true', dest='all', help='searches all submissions from \'whoishiring\'')
args = parser.parse_args()

def search_list(stories, date):
    for story in stories:
        if date in story.title:
            print 'found a match {0}, for title {1}'.format(date, story.title)
            return story

submitted_list = []
hiring_list = []
hired_list = []
freelance_list = []
search_story = None
stories = api.get_user('whoishiring').submitted

for story_id in stories:
    story = api.get_item(str(story_id))
    if hasattr(story, 'type') and story.type == 'story':
        submitted_list.append(story)
        if hasattr(story, 'title') and 'who is hiring' in story.title.lower():
            hiring_list.append(story)

if args.all:
    search_story = search_list(submitted_list, args.date)
    yclist = get_yc_jobs()
elif args.hiring:
    search_story = search_list(hiring_list, args.date)
elif args.hired:
    search_story = search_list(hired_list, args.date)
elif args.freelance:
    search_story = search_list(freelance_list, args.date)
else:
    search_story = search_list(submitted_list, args.date)

if not search_story:
    print "Couldn't find an item in 'whoishiring's submissions matching '{0}'".format(args.date)
    quit(1)

comments = api.get_item(str(search_story.id))
print "showing comments in submission {0}".format(search_story.title)

utf_comment = u''

for comment_int in comments.kids:
    try:
        comment_item  = api.get_item(str(comment_int))
    except Exception as e:
        print e
        print "Got an error trying to get comment id {0}".format(comment_int)
        continue
    if hasattr(comment_item, 'text') and comment_item.text:
        utf_comment = comment_item.text
        print utf_comment.encode("utf-8") #this is to make sure we're still outputting utf-8, even if stdout is being piped
