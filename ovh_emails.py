#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' OVH Email Manager (ovhEmailMan)
A small script that helps to add and remove one or more email addresses on the OVH shared domains

    Usage:
        ovh_mails.py list 
        ovh_mails.py add (<address> [(--pswd=<password> | -p <password)] | --file <filename>)[--description=<description> | -d <description>]
        ovh_mails.py remove (<address> | --file <filename>)
        ovh_mails.py flush
        ovh_mails.py (-h | --help)
    
    Arguments:
        <password>                        Password to access the mailbox (if not provided it's random generated)
        <filename>                        Name of the files to process. Check README to see how to format it
    
    Options: 
        -h, --help                        Show this help message
        -p <password>, --pswd=<password>  Set the password to the one provided
        
    Commands:
        list                              list all the email addresses currently configured
        add                               add one ore more (configured in <filename>) email addresses
        remove                            remove one ore more (configured in <filename>) email addresses
        flush                             flush all the credentials released
    '''
    


import ovh
from docopt import docopt
import functions as fs


if __name__ == '__main__':
    args = docopt(__doc__)
    #Validate args ---- TODO
  
    
__author__ = "Ruben Di Battista"
__license__ = "BSD 2-clause"
__version__ = "0.1a"
__email__ = "tidusuper91@gmail.com"
__status__ = "Prototype"
    