import urllib
import urllib2
import logging
import sys

user = "test"

domain = "http://mailinator.com"
userurl = domain + "/maildir.jsp?email="

mailprefix = domain + "/showmail2.jsp?email="
mailsuffix = "&msgid="

cookies = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookies)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    filename='mailscan.log',
                    filemode='w')

if len(sys.argv) < 2:
    print "usage: "+sys.argv[0]+" <username list>"
    sys.exit(0)
userlist = sys.argv[1]

try:
    FILE = open(userlist, "r")
    user = FILE.readline().strip()
    
    while user and len(user) > 0:
        print "checking mail to "+user
        r1 = urllib2.Request(userurl+user)
        resp = opener.open(r1)
        txt = resp.read()
        query = user + mailsuffix
        msgids = []
        
        index = 0
        while index != -1:
            index = txt.find(query, index+1)
            endex = txt.find(">", index)
            bite = txt[index:endex]
            if bite:
               msgids.append( bite.split("=")[1] )
               
        for msgid in msgids:
            r2 = urllib2.Request(mailprefix+user+mailsuffix+msgid)
            resp2 = opener.open(r2)
            
            txt2 = resp2.read()
            txt2lower = txt2.lower()
                    
            if txt2lower.find("password") != -1:
                toHdr = "\nto:"
                start = txt2lower.find(toHdr) + len(toHdr)                
                end = txt2lower.find("\n", start)
                email = txt2lower[start:end].strip()
                if len(email) < 1:
                    email = user

                fromHdr = "\nfrom:"
                start = txt2lower.find(fromHdr) + len(fromHdr)                
                end = txt2lower.find("\n", start)
                sender = txt2lower[start:end].strip()
            
                logging.debug("Message for email: "+email+" from: "+sender)
                logging.debug(txt2.strip())
                print "Match logged for email: "+email+" from: "+sender
    
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


#r1.add_header("User-agent","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1;)")
#r1.add_header("Accept-encoding", "gzip,deflate")

#print "Response Headers:"    
#print resp.info()

#print dir(cookies.cookiejar)
#print cookies.cookiejar._cookies
#print cookies.cookiejar._cookies['JSESSIONID']