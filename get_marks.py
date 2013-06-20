# load or get user credentials

import credentials 
my_credentials = credentials.credentials()
my_credentials.load()

import iofunctions

# post data

import urllib
params = {"timezoneOffset" : "-120",
          "userid" : 'U'+my_credentials.username,
          'pwd' : my_credentials.password}
data = urllib.urlencode(params)

# Fetch data

try:
    import pycurl
    ##pycurl.global_init(pycurl.GLOBAL_SSL)
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEDATA, file('tmp/StudentCentre.html','w'))
    c.setopt(pycurl.SSL_VERIFYPEER, True)
    c.setopt(pycurl.SSL_VERIFYHOST, 1)
    c.setopt(pycurl.CAINFO, "assets/cacert.pem")
    c.setopt(pycurl.COOKIE, "tmp/cookies.txt")
    c.setopt(pycurl.COOKIEJAR, "tmp/cookies.txt")
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.POSTFIELDS, data)
    c.setopt(pycurl.POST,1)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (compatible; MSIE 7.01; Windows NT 5.0)")
    c.setopt(pycurl.URL, "https://www.up.ac.za/psc/pscsmpra/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL")
    c.perform()
        

    # Parse data

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(open('tmp/StudentCentre.html'))

    import re

    names = []
    for a in soup.find_all("a",id = re.compile("CLASS_NAME")):
        names.append(a.string)

    descriptions = []
    for div in soup.find_all("div",id = re.compile("DERIVED_SSS_SCL_UP_GRANTOR_DESCR")):
        descriptions.append(div.span.string)

    grades = []
    for div in soup.find_all("div",id = re.compile("DERIVED_SSS_SCL_UP_GRADE")):
        try:
            div.span.string.encode('ascii')
            grades.append(div.span.string)
        except UnicodeEncodeError:
            grades.append('')


    # check whether grades have changed
    
    if iofunctions.marks_changed(names,descriptions,grades):
        # make tab sepperated values strings
        big_string = ''
        for i, name in enumerate(names):
            big_string += name + '\t'
            big_string += descriptions[i] + '\t'
            big_string += grades[i] + '\n'

        # save
        with open('marks.txt','w') as file:
            file.write(big_string)

        # open
        import webbrowser
        webbrowser.open("marks.txt")
        
        # Email
        iofunctions.build_and_send_email(my_credentials,big_string)

        #log
        iofunctions.my_logger("successful-changes made")
        
    else:
        # log
        iofunctions.my_logger("successful-no changes")
            
except pycurl.error as e:
    # log
    print e
    print "could not connect"
    iofunctions.my_logger("unsuccessful-connection problem")
    