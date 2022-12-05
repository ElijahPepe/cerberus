import argparse
import re

import tweepy
import logging

__version__ = '0.0.1'

def check_username(username):
	# Prone to change, temporary RegEx check. Very simple, yet effective
	return bool(re.match(r'.*\d{8}', username))

def check_contents(contents):
	contents = contents.lower()
	return "Hello, are you looking for" in contents

class Cerberus:
	def __init__(self):
		self.user = dict(
			consumer_key='',
			consumer_secret='',
			access_token='',
			access_token_secret=''
		)

	def check(self, args):
		try:
			# We don't check for the other keys for brevity
			if args.consumer_key:
				self.user['consumer_key'] = args.consumer_key
				self.user['consumer_secret'] = args.consumer_secret
				self.user['access_token'] = args.access_token
				self.user['access_token_secret'] = args.access_token_secret
				self.client = tweepy.Client(
					consumer_key=self.user['consumer_key'],
					consumer_secret=self.user['consumer_secret'],
					access_token=self.user['access_token'],
					access_token_secret=self.user['access_token_secret']
				)
				self.auth = tweepy.OAuth1UserHandler(
					self.user['consumer_key'],
					self.user['consumer_secret'],
					self.user['access_token'],
					self.user['access_token_secret']
				)
				self.api = tweepy.API(self.auth)
		except Exception as e:
			logging.exception(e)

		direct_message = self.client.get_direct_message_events(expansions=['sender_id'])
		username = direct_message.includes['users'][0].username
		contents = direct_message.data[0].text
		id = direct_message.data[0].id
		if check_username(username):
			self.api.delete_direct_message(id)
		if check_contents(contents):
			self.api.delete_direct_message(id)

def main():
	parser = argparse.ArgumentParser(description=f'Cerberus v{__version__}')

	subparsers = parser.add_subparsers(title='Commands', dest='subparser_name', metavar='<command>')
	check_parser = subparsers.add_parser('check', help='check your DMs')

	check_parser.add_argument('--consumer-key', dest='consumer_key', action='store', metavar='<consumer key>')
	check_parser.add_argument('--consumer-secret', dest='consumer_secret', action='store', metavar='<consumer secret>')
	check_parser.add_argument('--access-token', dest='access_token', action='store', metavar='<access token>')
	check_parser.add_argument('--access-token-secret', dest='access_token_secret', action='store', metavar='<access token secret>')

	args, _ = parser.parse_known_args()

	cli = Cerberus()

	try:
		if args.subparser_name == 'check':
			cli.check(args)
	except KeyboardInterrupt:
		logging.info('Keyboard interrupted!')

if __name__ == '__main__':
	main()