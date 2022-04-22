# **INTRODUCTION**

***table_parser bot*** - it's bot-notifier of new items in any html table(specifies in bash_parser file). 
This parses the table and, when an new item appears, sends a notification in a telegram-clients of some users, presented in "user_list.txt".
At the same time, all such items are saved in the database to exclude repeated notifications.



# **FILES PRESENTED IN DIRECTORY:**

**table_parser.py** - main python script

**bash_parser.sh** - executable bash parser script for creating message from cutted table

**user_list.txt** - empty file, list with users of this bot. Add new user in form like "USER:telegram_CHAT_ID", like   ___NAME:333222111___

**certs/** - directory with crt.pem and key.pem for download table (optional)

**base_old** - empty database file

**README.md** - this file



# **PREPARATION FOR WORK:**

1. Copy all these files to directory on the server

2. Add personal certs (___crt.pem___ and ___key.pem___ to certs directory) - optional

3. Install python3 and bs4 python library on the server	___pip3 install bs4___

4. Edit global paths in ___table_parser.py___, if you need to start this script outside the bots directory:

	path_user_list = '/path/to/user_list.txt'
	
	path_base = '/path/to/base_old'
	
	path_bash_parser = "path/to/directory/with/bash_parser/"
	
Also edit path to certs directory and replace names from test.crt.pem and test.key.pem to yours in the string(optional):

	download = 'wget --certificate=./certs/test.crt.pem --private-key=./certs/test.key.pem --no-check-certificate -P /tmp/ https://test.html'


5. Add script to cron on the server:

	crontab -e

and add string

	*/15 * * * * /bin/python3 /path/to/bot/table_parser.py &> /dev/null


# **LOGGING**

The log file will be created automatically after script starting first time

	/var/log/telegram_log



