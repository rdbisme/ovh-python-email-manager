import ovh
import ConfigParser
from prettytable import PrettyTable

class EmailManager :
    ''' This class wraps the ovh Python API and provide some 
    functionalities to interact with email accounts
    
    Arguments: 
        niceoutput              Optional. If True (default), prints out better looking tables
    
    Properties:
        client:                 ovh.Client() object 
        
    Methods:
        check_token             Checks if the customer key is valid
        get_token               Prompt to user a message to get the customer_key.
                                It puts the key inside the ovh.conf
        __get_emails            Retrieves the email accounts detail
        list_emails             List all the domain-associated email accounts
    
    '''
    
    client = ovh.Client()
    parser = ConfigParser.SafeConfigParser()
    parser.read('ovh.conf')
    DOMAIN = parser.get('smtp', 'domain')
    
    def __init__(self,niceoutput = True):
        self.niceoutput = niceoutput
        if not(self.check_token()):
            self.get_token()

    
    def check_token(self):
        try:
            self.client.get('/me/api/credential')
            return True
        except ovh.APIError as e:
            print "API Error ({0})\n".format(e)
            return False

    def get_token(self):
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
                accountData = self.client.get('/email/domain/{0}/account/{1}'.format(self.DOMAIN,\
                                                                                     account))
                tab.add_row([
                             accountData['accountName']+'@'+accountData['domain'],
                             accountData['description'],
                             accountData['size'],
                             accountData['isBlocked']
                             ])
            print tab