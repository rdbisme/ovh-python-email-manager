#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' OVH Email Manager (ovhEmailMan)
A small script that helps to add and remove one or more email addresses on the OVH shared domains

    Usage:
        ovh_mails.py list [--ugly]
        ovh_mails.py add (<address> [--pswd=<password>][--description=<description>] | --file <filename> [--notify])
        ovh_mails.py update (<address> [--pswd=<password>][--description=<description>] | --file <filename> [--notify])
        ovh_mails.py remove (<address> | --file <filename>)
        ovh_mails.py (-h | --help)
    
    Arguments:
        <password>                        Password to access the mailbox (if not provided it's random generated)
        <filename>                        Name of the files to process (csv). Check README to see how to format it
    
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
    


import ovh
from docopt import docopt
from ovhem import EmailManager
from ovhem import fileprocesser as fp


if __name__ == '__main__':
    args = docopt(__doc__)
    #Validate args ---- TODO
    eman = EmailManager()
    
    # 'List' command parsing
    if args['list']:
        if args['--ugly']:
            eman.niceoutput = False

        eman.list_emails()
    # 'Add' command parsing
    elif args['add']:
        if args['<address>']:

            emails = (
                      {
                       'address': args['<address>'],
                       'password': None,
                       'description': None,
                       },
                      )
            if args['--description']:
                emails[0]['description'] = args['<description>']
            if args['--pswd']:
                emails[0]['password'] = args['<password>']
        if args['--file']:
            emails = fp.process_file(args['<filename>'])    
            
        # Getting back the emails dict
        emails=eman.add_emails(emails)
        if args['--notify']:
            fp.send_notifications(emails)

    # 'remove' command parsing       
    elif args['remove']:
        if args['<address>']:

            emails = (
                      {
                       'address': args['<address>'],
                       },
                      )
        if args['--file']:
            emails = fp.process_file(args['<filename>'])
        eman.remove_emails(emails)
        
    elif args['update']:
        if args['<address>']:

            emails = (
                      {
                       'address': args['<address>'],
                       'password': None,
                       'description': None,
                       },
                      )
            if args['--description']:
                emails[0]['description'] = args['<description>']
            if args['--pswd']:
                emails[0]['password'] = args['<password>']
        if args['--file']:
            emails = fp.process_file(args['<filename>'])    
            
        # Getting back the emails dict
        emails=eman.add_emails(emails)
        if args['--notify']:
            fp.send_notifications(emails)
              
  
    
__author__ = "Ruben Di Battista"
__license__ = "BSD 2-clause"
__version__ = "0.1a"
__email__ = "tidusuper91@gmail.com"
__status__ = "Prototype"
    