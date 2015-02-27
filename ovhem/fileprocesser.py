import csv
import smtplib
from email.mime.text import MIMEText
import ConfigParser

def process_file(file):
    ''' This function processes the <file> and return a dictionary
    that can be used with EmailManager class.
    
    <file> must be a csv with 4 fields:
    
    ['Account Name','Description','Password','Notification Email']
    
    e.g.
    
    ['rdb@domain.com'*, 'A sample mailbox','','rdb@gmail.com']
    * = required. The other fields may be empty
    
    '''
    
    with open(file,'rU') as f:
        lines = csv.reader(row for row in f if not row[0] == '#')
        
        emails = []
        for line in lines:
            emails.append({
                           'address': line[0],
                           'description': line[1],
                           'password': line[2],
                           'notification': line[3]
                           }
                          )
    return emails

def send_notifications (emails):
    ''' This function sends the notification mail to the
    emails[i]['notification'] address using the mail.template file'''
    
    #Parser for config file
    parser = ConfigParser.SafeConfigParser()
    parser.read('ovh.conf')
    
    #SMTP connection
    conn = smtplib.SMTP(parser.get('smtp','host'),parser.get('smtp','port'))
    conn.login(parser.get('smtp','username'), parser.get('smtp','password'))
    
    with open('mail.template','rU') as fp:
        template = fp.read()
    for email in emails:
        template = template.format(username=email['address'],\
                                   password=email['password'])
        msg = MIMEText(template)
        msg['Subject'] = 'New personal mailbox!'
        msg['From'] = parser.get('smtp','from')
        msg['To'] = 'tidusuper91@gmail.com' #email['notification']
        
        conn.sendmail(msg['From'], msg['To'], msg.as_string())
        conn.quit()
        

        

        