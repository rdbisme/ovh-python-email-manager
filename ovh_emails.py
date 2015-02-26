#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' OVH Email Manager (ovhEmailMan)
A small script that helps to add and remove one or more email addresses on the OVH shared domains

    Usage:
        ovh_mails.py list [--ugly]
        ovh_mails.py add (<address> [--pswd=<password>][--description=<description>] | --file <filename>)
        ovh_mails.py remove (<address> | --file <filename>)
        ovh_mails.py (-h | --help)
    
    Arguments:
        <password>                        Password to access the mailbox (if not provided it's random generated)
        <filename>                        Name of the files to process. Check README to see how to format it
    
    Options: 
        -h, --help                        Show this help message
        -u, --ugly                        Print without nice tables
        -p, --pswd=<password>  Set the password to the one provided
        
    Commands:
        list                              list all the email addresses currently configured
        add                               add one ore more (configured in <filename>) email addresses
        remove                            remove one ore more (configured in <filename>) email addresses
        flush                             flush all the credentials released
    '''
    


import ovh
from docopt import docopt
from ovhem import EmailManager


if __name__ == '__main__':
    args = docopt(__doc__)
    #Validate args ---- TODO
    
    print args
    
    if args['list']:
        if args['--ugly']:
            eman = EmailManager(niceoutput=False)
        else:
            eman = EmailManager()
        eman.list_emails()
    elif args['add']:
        eman = EmailManager()
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
        
        eman.add_emails(emails)


            
    elif args['remove']:
        raise NotImplemented
              
  
    
__author__ = "Ruben Di Battista"
__license__ = "BSD 2-clause"
__version__ = "0.1a"
__email__ = "tidusuper91@gmail.com"
__status__ = "Prototype"
    