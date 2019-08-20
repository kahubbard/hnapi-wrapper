#!/usr/bin/python

import json
import argparse

import sseclient

from firebase import firebase


class HNUser:

    def __init__(self, user):
        self.user = user
        self.id = user['id']
        self.delay = user['delay']
        self.created = user['created']
        self.karma = user['karma']
        self.about = user['about']
        self.submitted = user['submitted']


class HNItem:

    def __init__(self, item):
        self.keys_list = ['id', 'deleted', 'type', 'by', 'time', 'text', 'dead', 'parent', 'kids', 'url', 'score', 'title', 'parts', 'descendants']

        for key in self.keys_list:
            if key in item.keys():
                setattr(self, key, item[key])


class HNAPI:

    url = 'https://hacker-news.firebaseio.com/v0/'

    def __init__(self):
        self.firebase = firebase.FirebaseApplication(HNAPI.url, None)
        self.loaded_users = {} #dict of usernames to HNUser objects
        
    def get_user(self, user):
        if user in self.loaded_users.keys():
            return self.loaded_users[user]
        else:
            user_map = self.firebase.get('user/' + user, None)
            user = HNUser(user_map)
            self.loaded_users[user.id] = user
            return user

    def get_item(self, item):
        item_map = self.firebase.get('item/' + item, None)
        return HNItem(item_map)

    def get_user_submitted(self, username, comment_type):
        comments = []
        user = self.get_user(username)
        for id in user.submitted:
            comment = self.get_item(str(id))
            if hasattr(comment, comment_type) and comment.type == comment_type:
                comments.append(comment.text)
        return comments

    def get_user_stories(self, username):
        return get_user_submitted(username, 'story')
        
    def get_user_comments(self, username):
        return get_user_submitted(username, 'comment')

    def get_stories(self, story_type):
        if story_type not in ['show', 'ask', 'job', 'new', 'top']:
            return None
        stories = []
        for story_id in self.firebase.get(story_type + 'stories', None):
            story = self.get_item(str(story_id))
            stories.append(story)
        return stories

    def get_top_stories(self):
        return self.get_stories('top')

    def get_new_stories(self):
        return self.get_stories('new')

    def get_ask_stories(self):
        return self.get_stories('ask')

    def get_job_stories(self):
        return self.get_stories('job')

    def get_show_stories(self):
        return self.get_stories('show')

    def get_updates(self):
        return self.firebase.get('updates', None)

    def subscribe_to_user(self, username, function):
        messages = sseclient.SSEClient(HNAPI.url + 'user/' + username + '.json')
        for message in messages:
            msg_data = json.loads(message.data)
            if msg_data is None:
                continue
            function(msg_data)


if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Hacker News Job Search')
   parser.add_argument('--user', dest='user', type=str)
   parser.add_argument('--item', dest='item', type=str)
   args = parser.parse_args()
   print args.user
   print args.item
