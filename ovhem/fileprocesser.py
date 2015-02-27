import csv

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
    print len(emails)