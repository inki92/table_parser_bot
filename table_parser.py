import os
import requests
import re
import datetime

#Setting global variables

#API token of @table_parser_bot
bot_token = "###"

#Path to file with list of users
#Add users in file like NAME:TOKEN, for example NAME:185500000
path_user_list = './user_list.txt'

#Path to log file
path_log = '/var/log/telegram_log'

#Path to file with base of old items
path_base = './base_old'

#Path to bash_parser.sh (see def parse() description)
path_bash_parser = "./"



def download_table():

	"""
	Download table.html page
	"""
	download = 'wget --no-check-certificate -P /tmp/ https://table.html'

	os.system (download)

def open_table():

	"""
	Open table.html and write data to $table
	"""

	path = '/tmp/table.html'

	global table
	with open(path, 'r') as f:
		table = f.read()

	os.remove(path)


def parse():

	"""
	This function will create table.txt
	from table.html in form "one item = one string".
	After that "bash_parser" will
	create table_cut with items with
	status "New" in string and form like ["url", "name"].
	bash_parser.sh must contain next text:

	#!/bin/bash
	cat /tmp/table.txt | grep ">New<" | awk -F "\"" '{print ">"$4"<",",",$9}' | awk -F "/td>" '{print $1}' | tr "<" " " | tr ">" " "

	and this file must be executable.
	"""

	from bs4 import BeautifulSoup

	soup = BeautifulSoup(table, "html.parser")

	path_table = '/tmp/table.txt'

	with open(path_table, 'w') as f_table:
		for tr in soup.find_all('tr'):
			tds = tr.find_all('td')
			f_table.write('{}\n'.format(str(tds)))

	bash_parser = '/bin/bash ' + path_bash_parser + 'bash_parser.sh > /tmp/table_cut.txt'

	os.system(bash_parser)

	os.remove(path_table)



def telegram_bot_sendtext(user_ID, bot_message):

	"""
	Send one message to one user_ID to telegram.
	Part of telegram api.
	"""

	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + user_ID + '&parse_mode=Markdown&text=' + bot_message
	response = requests.get(send_text)
	#response for debug
	return response.json()



def message(text):

	"""
	Send some message to all users in user_list.
	"""

	with open(path_user_list, 'r') as user_list:
		for line in user_list.readlines():
			user = line.split(':')
			user_ID = user[1]
			telegram_bot_sendtext(user_ID, text)



def search_send(table_line):

	"""
	Function for compare with base and:
	if item was in base - only write in log;
	if not - send message and write in base.
	"""

	base = open(path_base, 'r+')
	base_text = base.read()
	item_pre = table_line.split('errata/')
	item = item_pre[1].split(' ')
	item_name = item[0]
	with open(path_log, 'a') as f_log:
			if re.search(item_name, base_text):
				f_log.write('{}'.format('   Was in base: '))
				f_log.write('{}\n'.format(item_name))
			else:
				all_message = table_line.split(',')
#               MESSAGE_TEXT FOR bash_parser with os_version
				message_text = all_message[0] + all_message[1] + all_message[2]
				#log_message info for debug
				log_message = message(message_text)

				base.write(message_text)

				f_log.write('{}'.format('   New item: '))
				f_log.write('{}\n'.format(str(item_name)))

	base.close()

def send_to_all():

	"""
	This function will compare text in table_cut
	with base of old items (search_send function use).
	After it function will use	"def message" to send info
	about new item for all users in user_list and write
	info about this	to log file.
	"""

	path_table_cut = '/tmp/table_cut.txt'

	#time for log
	now_time = datetime.datetime.now()

	with open (path_log, 'a') as f_log:
		f_log.write('{}\n'.format(str('   ***   ')))
		f_log.write('{}\n'.format(str(now_time)))
		f_log.write('{}\n'.format(str('   ***   ')))

	with open(path_table_cut, 'r') as f_table_cut:
		with open (path_log, 'a') as f_log:
			for line in f_table_cut.readlines():
				#Block to bypass exception, when bot try to work with broken items
				try:
					search_send(line)
				except:
					f_log.write('{1}:\n {0}\n'.format(line, 'ERROR IN PARSER'))

	os.remove(path_table_cut)

#Main code

if __name__ == '__main__':
	download_table()

if __name__ == '__main__':
	open_table()

if __name__ == '__main__':
	parse()

if __name__ == '__main__':
	send_to_all()
