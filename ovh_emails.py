#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' OVH Email Manager (ovhEmailMan)
A small script that helps to add and remove one or more email addresses on the OVH shared domains

    Usage:
        ovh_mails.py list [--ugly]
        ovh_mails.py add (<address> [--pswd=<password>][--description=<description>] [--notify <notifyEmail>] | --file <filename> [--notify]) 
        ovh_mails.py remove (<address> | --file <filename>)
        ovh_mails.py (-h | --help)
    
    Arguments:
        <password>                        Password to access the mailbox (if not provided it's random generated)
        <filename>                        Name of the files to process (csv). Check README to see how to format it
        <description>                     Description of the mailbox
        <notifyEmail>                     Email address that receives a notification email using smtp credentials in ovh.conf
    
    Options: 
        -h, --help                        Show this help message
        -u, --ugly                        Print without nice tables
        -p, --pswd=<password>             Set the password to the one provided
        -n, --notify                      If set, notification mail is sent using smtp credentials in ovh.conf
        
    Commands:
        list                              list all the email addresses currently configured
        add                               add one or more (configured in <filename>) email addresses
        remove                            remove one ore more (configured in <filename>) email addresses
    '''
    
__version__ = '0.1a'
__author__ = ('Ruben Di Battista',
              '@rubendibattista',
              'rubendibattista@gmail.com'
              )

import ovh
from docopt import docopt
from ovhem import EmailManager
from ovhem import fileprocesser as fp


if __name__ == '__main__':
    args = docopt(__doc__)
    #Validate args ---- TODO
    
    # Defaults
    password = None
    description = None
    address_arg = args['<address>']
    
    # Email Manager Class
    eman = EmailManager()
    
    # 'List' command parsing
    if args['list']:
        if args['--ugly']:
            eman.niceoutput = False

        eman.list_emails()
    # 'Add' command parsing
    elif args['add']:
        # If address is provided --> single insert
        if address_arg:
            address= address_arg       
            if args['--description']:
                description = args['description']
            if args['--pswd']:
                password = args['description']
            if args['<notifyEmail>']:
                notifyEmail = args['<notifyEmail>']
            emails = (
                      {
                       'address': address,
                       'password': password,
                       'description': description,
                       'notification': notifyEmail,
                       },
                      )
        # Else process a csv file
        elif args['--file']:
            emails = fp.process_file(args['<filename>'])    
            
        # Getting back the emails dict
        emails=eman.add_emails(emails)
        if args['--notify']:
            fp.send_notifications(emails)

    # 'remove' command parsing       
    elif args['remove']:
        # If address is provided --> single insert
        if address_arg:
            address = address_arg

            emails = (
                      {
                       'address': address,
                       },
                      )
        # Else process a csv file
        elif args['--file']:
            emails = fp.process_file(args['<filename>'])
        eman.remove_emails(emails)

