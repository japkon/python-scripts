""" random_recipe.py - Given a gmail address, a password to log into it, and a
list of recipients, send each recipient the same random recipe from food.com """

from bs4 import BeautifulSoup
from email.mime.text import MIMEText

import argparse
import random
import smtplib
import urllib2

URL = 'http://www.food.com/'
FILENAME = 'unwanted_categories'
GMAIL_SMTP_PORT = 587

def sendEmail(sender_email, password, recipients, url, title, categories):

    """ Start an email server by logging into 'sender_email' with the given
    password. Send an email to each email in the recipients list. """

    content = MIMEText("%s\n\nIf this recipe isn't for you, add %s to your "
                       "'unwanted_categories' file."
                       % (url, ', '.join(categories)))

    content['Subject'] = title

    server = smtplib.SMTP('smtp.gmail.com', GMAIL_SMTP_PORT)
    server.ehlo()
    server.starttls()

    try:
        server.login(sender_email, password)
    except Exception:
        print "Could not log in to %s" % sender_email
    else:
        for recipient in recipients:
            try:
                server.sendmail(sender_email, recipient, content.as_string())
            except Exception:
                print "Failed to send email to %s" % recipient

    server.close

def parseRecipePage(html):

    """ Given a recipe page's html, return the recipe title and a list of
    categories the recipe is associated with """

    soup = BeautifulSoup(html)
    breadcrumbs = soup.find('div', 'breadcrumbs')

    if not breadcrumbs:
        return (None, None)

    def isCategory(x):
        return x != u'\n' and x.string and 'Recipes' != x.string

    categories = [x.string for x in breadcrumbs.contents if isCategory(x)]

    title = soup.title.string
    if title:
        title = title.split('-')[0] # strip '- Food.com' from the title

    return (title, set(categories))

def parseArgs():

    """ Parse the given arguments and return them as a tuple """

    parser = argparse.ArgumentParser()

    parser.add_argument('sender_email', help='Address email is sent from')
    parser.add_argument('sender_pass', help='Password for the given address')
    parser.add_argument('recipients',
                        help='Addresses the email is sent to',
                        nargs='+')

    args = parser.parse_args()
    return (args.sender_email, args.sender_pass, args.recipients)

def main(email, password, recipients):

    """ Get a random recipe from food.com, and email it to a list of recipients
    if the recipe's category is not in the 'unwanted_categories' file """

    url = URL + str(random.randint(2670, 100000))
    response = urllib2.urlopen(url)
    html = response.read()
    (title, categories) = parseRecipePage(html)

    with open(FILENAME, 'r') as f:
        badCategories = set(f.read().split())

    if categories and not categories & badCategories:
        sendEmail(email, password, recipients, url, title, categories)
    else:
        main(email, password, recipients)

if __name__ == '__main__':
    main(*parseArgs())
