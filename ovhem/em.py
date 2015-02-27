import ovh
import ConfigParser
import string
import warnings
from random import choice
from prettytable import PrettyTable

class EmailManager :
    ''' This class uses the ovh Python API and provide some 
    functionalities to interact with email accounts
    
    Arguments: 
        niceoutput              Optional. If True (default), prints out better looking tables
    
    Properties:
        client:                 ovh.Client() object 
        
    Methods:
        list_emails             List all the domain-associated email accounts
        add_emails              Add the emails from the dictionary given as argument
        remove_emails           Remove the emails from the dictionary given as argument
        update_emails           Update the emails from the dictionary as argument
    
    '''
    
    client = ovh.Client()
    parser = ConfigParser.SafeConfigParser()
    parser.read('ovh.conf')
    DOMAIN = parser.get('ovh-eu', 'domain')
    
    def __init__(self,niceoutput = True):
        ''' Constructor. Checks for token validity and if not present or invalid prompt the user 
        for getting it '''
        
        self.niceoutput = niceoutput
        if not(self.__check_token()):
            self.__get_token()

    
    def __check_token(self):
        print 'Checking Token...'
        try:
            self.client.get('/me/api/credential')
            return True
        except ovh.APIError as e:
            print "API Error ({0})\n".format(e)
            return False

    def __get_token(self):
        access_rules = [
                    {'method': 'GET', 'path': '/me/api/*'},
                    {'method': 'POST', 'path': '/me/api/*'},
                    {'method': 'PUT', 'path': '/me/api/*'},
                    {'method': 'DELETE', 'path': '/me/api/*'},
                    {'method': 'GET', 'path': '/email/domain*'},
                    {'method': 'POST', 'path': '/email/domain*'},
                    {'method': 'PUT', 'path': '/email/domain*'},
                    {'method': 'DELETE', 'path': '/email/domain*'}
        
                     ]
        validation = self.client.request_consumerkey(access_rules)
        
        print "To access OVH Api you must validate. Please visit the following\
        link:\n %s" % validation['validationUrl']
        
        raw_input('Press Enter when done...')

        self.parser.set('ovh-eu', 'consumer_key', validation['consumerKey'])
        
        with open('ovh.conf','wb') as configfile:
            self.parser.write(configfile)
            
    def __get_emails(self):
        accounts=self.client.get('/email/domain/{0}/account'.format(self.DOMAIN))
        accountData = []
        for account in accounts:
            accountData.append(self.client.get('/email/domain/{0}/account/{1}'.format(self.DOMAIN,\
                                                                                     account)))
        return accountData
    
    def list_emails(self):
        
        accounts=self.__get_emails()
        
        if not(self.niceoutput):
            for account in accounts:
                print account['accountName']+'@'+account['domain']
        else:
            tab = PrettyTable(["Account Name","Description","Size","Blocked"])
            tab.align["City name"] = "c" 
            for account in accounts:

                tab.add_row([
                             account['accountName']+'@'+account['domain'],
                             account['description'],
                             account['size'],
                             account['isBlocked']
                             ])
            print tab
    
    def add_emails(self,emails):
        print 'Adding emails...'
        for i,email in enumerate(emails):
            # If password is not set
            if not(email['password']):
                password = self.__mkpassword()
                emails[i]['password'] = password
                email['password'] = password
                
            self.__add_email(email['address'], email['password'], email['description'])
        return emails
    
    def remove_emails(self,emails):
        print 'Removing emails...'
        for email in emails:
            self.__remove_email(email['address'])
            
    def update_emails(self,emails):
        print 'Updating emails...'
        for email in emails:
            self.__update_email(email['address'], email['password'], email['description'])
            
    def __update_email(self,email,password,desc=None):
        #Checking if email already present
        accounts = self.__get_emails()
        if not(email in [account['accountName']+'@'+account['domain'] for account in accounts]):
            warnings.warn('{email} cannot be updated: not present!'.format(email=email),\
                          RuntimeWarning)
        else:
            self.client.put('/email/domain/{0}/account'.format(self.DOMAIN),
                             accountName=email.split('@')[0],
                             description = desc,
                             password = password,
                             size = 5E9
                             )
        print email+' updated!'
            
           
    def __add_email(self,email,password,desc=None):
        #Checking if email already present
        accounts = self.__get_emails()
        if email in [account['accountName']+'@'+account['domain'] for account in accounts]:
            warnings.warn('{email} is already there!'.format(email=email),RuntimeWarning)
        else:
            self.client.post('/email/domain/{0}/account'.format(self.DOMAIN),
                             accountName=email.split('@')[0],
                             description = desc,
                             password = password,
                             size = 5E9
                             )
        print email+' added!'
    
    def __remove_email(self,email):
        #Checking if email is present
        accounts = self.__get_emails()
        if not(email in [account['accountName']+'@'+account['domain']  for account in accounts]):
            print [account['accountName']+'@'+account['domain']  for account in accounts]
            warnings.warn('{email} cannot be deleted: not present!'.format(email=email),\
                          RuntimeWarning)
        else:
            self.client.delete('/email/domain/{0}/account/{1}'.format(self.DOMAIN,email.split('@')[0]))
        
        print email+' removed!'
    
    def __mkpassword(self,size=18):
        chars = string.ascii_letters+string.digits
        return ''.join(choice(chars) for _ in range(size))