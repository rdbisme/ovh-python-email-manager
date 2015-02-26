from ovhem import EmailManager

em = EmailManager(niceoutput=False)

print em.list_emails()