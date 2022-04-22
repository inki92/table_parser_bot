#!/bin/bash

#bash_parser.sh
#This is part of table_parser.py

#########################################################
#MESSAGE VARIANTS(uncomment string to message creation):
#########################################################

#######################################################
#This parser for line in message like "link_to_item item_name item_version" , for example:
#    "link package 8.0"

cat /tmp/table.txt | grep ">New<" | awk -F "\"" '{print ">"$4"<",",",$9,$7}' | awk -F "/td>" '{print $1$2}' | awk -F "<td align= " '{print $1$2}' | tr "<" " " | tr ">" " " | awk -F "/x86_64" '{print $1}' | tr "_" "-"




