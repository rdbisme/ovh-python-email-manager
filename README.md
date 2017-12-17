# ovh-python-email-manager
Simple command line program to manage OVH shared hosting email accounts.

I created this program because when I changed hosting to OVH I needed to create like 80 mailboxes and I didn't want to do it manually. 

## TL;DR
Basically you can use the provided command line program as usual after you provided the `application_key`, the `application_secret` and the `domain` in the `ovh.conf` file (you can create them [here](https://api.ovh.com/g934.first_step_with_api)), just check the help:

```
python ovh_emails.py -h
```
or even 
```
chmod u+x ovh_emails.py
./ovh_emails.py -h
```
PS: If you need to send notifications to a particular email address you have also to fill the `[smtp]` config file entries.

## Functionalities

The CLI provides three basic commands
- Listing Entries
```
ovh_emails.py list [--ugly]
```
you can also provide a `--ugly` option to avoid the nice tables formatting

- Adding Entries 
```
ovh_emails.py add (<address> [--pswd=<password>][--description=<description>] [--notify <notifyEmail>] | --file <filename> [--notify]) 
```
The nice thing is that you can process a file that is formatted as 4 field csv :
``` 
['Account Name'*,'Description','Password','Notification Email'] 
e.g.
['rdb@domain.com', 'A sample mailbox','','rdb@gmail.com']
```
the only field needed is `Account Name`. If `Password` is not filled up the program auto-calculates it. `Notification Email` is only needed if the `--notify` flag is used.

- Removing Entries
```ovh_mails.py remove (<address> | --file <filename>)```

Even here you can use the same csv formatting if setting `--filename` flag. In this case the only field used is `Account Name`

### Notifications

When you set the flag `-n` the script sends via the SMTP settings you configured in `ovh.conf` a mail using the `mail.template`.

An example is reported in the `mail.template.example`. Basically you have to provide a text, where the placheholders `{username}` and `{password}` are replaced with the true values
