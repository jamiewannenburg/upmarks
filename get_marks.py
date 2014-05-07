# change directory
import os
root = "C:/Users/Vincent/Programming/UPMarks"
os.chdir(root)

import time
from datetime import timedelta, datetime

# load or get user credentials

import credentials 
my_credentials = credentials.credentials()
my_credentials.load()

import iofunctions

# post data

import urllib

# Fetch data
from bs4 import BeautifulSoup
import re

try:
    import pycurl
    
    #### load login form
    #pycurl.global_init(pycurl.GLOBAL_SSL)
    f = open('tmp/StudentCentre.html','w')
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEDATA, f)
    c.setopt(pycurl.SSLVERSION, 3)
    c.setopt(pycurl.SSL_VERIFYPEER, True)
    #c.setopt(pycurl.SSL_VERIFYHOST, 1)
    #c.setopt(c.VERBOSE, True)
    c.setopt(pycurl.CAINFO, "assets/cacert.pem")
    c.setopt(pycurl.COOKIEFILE, "tmp/cookies.txt")
    c.setopt(pycurl.COOKIEJAR, "tmp/cookies.txt")
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (compatible; MSIE 7.01; Windows NT 5.0)")
    c.setopt(pycurl.URL, "https://www1.up.ac.za/uplogin/faces/login.jspx?")
    c.perform()
    f.close()

    soup = BeautifulSoup(open('tmp/StudentCentre.html','rb'))

    ##### check if I am still logged in
    if (str(soup.find('title')) == "<title>UP Login</title>" ):

        referer =  c.getinfo(c.EFFECTIVE_URL)

        #### do "javascript" validation and send request
        
        params = {"useridtest" : '',
                    "userid_test" : 'u'+my_credentials.username,
                    "foilautofill" : '',
                    'password' : my_credentials.password}

        # find hidden fields and add to data
        for i in soup.find_all("input",type = "hidden"):
            params[i['name']] = i['value']
        params['username'] = 'U'+my_credentials.username # javascript does this

        js = soup.find('head').find('script')
        request_id = eval(re.findall('request_id = [0-9+-]*;',str(js))[0][13:-1])
        usernamelookup = "https://www1.up.ac.za:443/uplogin/usernamelookup?request_id="+str(request_id)+"&username="+params['userid_test']

        header = ['User-Agent: XMLHTTP/1.0']

        #### get xml
        f = open('tmp/StudentCentre.html','w')
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEDATA, f)
        c.setopt(pycurl.SSLVERSION, 3)
        c.setopt(pycurl.SSL_VERIFYPEER, True)
        # c.setopt(pycurl.SSL_VERIFYHOST, 1)
        #c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.CAINFO, "assets/cacert.pem")
        c.setopt(pycurl.COOKIEFILE, "tmp/cookies.txt")
        c.setopt(pycurl.COOKIEJAR, "tmp/cookies.txt")
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.HTTPHEADER, header)
        c.setopt(pycurl.URL, usernamelookup)
        c.perform()
        f.close()

        params['username'] = my_credentials.username # javascript does this

        data = urllib.urlencode(params)
        # print data

        header = ['Content-type: application/x-www-form-urlencoded',
                    'Origin: https://www1.up.ac.za'
                    ]

        #### send login form
        f = open('tmp/StudentCentre.html','w')
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEDATA, f)
        c.setopt(pycurl.SSLVERSION, 3)
        c.setopt(pycurl.SSL_VERIFYPEER, True)
        # c.setopt(pycurl.SSL_VERIFYHOST, 1)
        # c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.CAINFO, "assets/cacert.pem")
        c.setopt(pycurl.COOKIEFILE, "tmp/cookies.txt")
        c.setopt(pycurl.COOKIEJAR, "tmp/cookies.txt")
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(pycurl.POST,1)
        c.setopt(pycurl.HTTPHEADER, header)
        c.setopt(pycurl.REFERER, referer)
        c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (compatible; MSIE 7.01; Windows NT 5.0)")
        c.setopt(pycurl.URL, "https://www1.up.ac.za/oam/server/auth_cred_submit")
        c.perform()
        f.close()

        soup = BeautifulSoup(open('tmp/StudentCentre.html','rb'))
    ### I am now logged in, but need to change query from javascript
    ###### first javascript redirect
    js = str(soup.find('script'))

    # get afrLoop var
    afrLoop = re.findall('"_afrLoop=\S*";',js)[0][10:-2]
    data = '_afrLoop=' + afrLoop
    data += '&_afrWindowMode=' + '0'
    data += '&_afrWindowId=' + '10e6wa3xcl_6'

    WCPORTALSESSIONID = re.findall('var sess = "\S*";',js)[0][12:-2]
    #re.findall('";WCPORTALSESSIONID=\S*";',js)[0][20:-2]
    url = "https://www1.up.ac.za/wcportal/faces/sso"+WCPORTALSESSIONID+"?"+data
    # print url

    f = open('tmp/StudentCentre.html','w')
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEDATA, f)
    c.setopt(pycurl.SSLVERSION, 3)
    c.setopt(pycurl.SSL_VERIFYPEER, True)
    # c.setopt(pycurl.SSL_VERIFYHOST, 1)
    # c.setopt(c.VERBOSE, True)
    c.setopt(pycurl.CAINFO, "assets/cacert.pem")
    c.setopt(pycurl.COOKIEFILE, "tmp/cookies.txt")
    c.setopt(pycurl.COOKIEJAR, "tmp/cookies.txt")
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (compatible; MSIE 7.01; Windows NT 5.0)")
    c.setopt(pycurl.URL, url)
    c.perform()
    f.close()

    ###### second javascript redirect
    soup = BeautifulSoup(open('tmp/StudentCentre.html','rb'))
    ### I am now logged in, but need to change query from javascript
    js = str(soup.find('script'))

    # get afrLoop var
    afrLoop = re.findall('"_afrLoop=\S*";',js)[0][10:-2]
    data = '_afrLoop=' + afrLoop
    data += '&_afrWindowMode=' + '0'
    data += '&_afrWindowId=' + '10e6wa3xcl_6'

    url = "https://www1.up.ac.za/wcportal/faces/student.jspx?"+data
    # print url

    f = open('tmp/StudentCentre.html','w')
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEDATA, f)
    c.setopt(pycurl.SSLVERSION, 3)
    c.setopt(pycurl.SSL_VERIFYPEER, True)
    # c.setopt(pycurl.SSL_VERIFYHOST, 1)
    # c.setopt(c.VERBOSE, True)
    c.setopt(pycurl.CAINFO, "assets/cacert.pem")
    c.setopt(pycurl.COOKIEFILE, "tmp/cookies.txt")
    c.setopt(pycurl.COOKIEJAR, "tmp/cookies.txt")
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (compatible; MSIE 7.01; Windows NT 5.0)")
    c.setopt(pycurl.URL, url)
    c.perform()
    f.close()

    #### get link to student centre
    soup = BeautifulSoup(open('tmp/StudentCentre.html','rb'))
    ss_element = soup.find('a',id="goLink52")
    url =  str(ss_element['href'])
    referer = url

    f = open('tmp/StudentCentre.html','w')
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEDATA, f)
    c.setopt(pycurl.SSLVERSION, 3)
    c.setopt(pycurl.SSL_VERIFYPEER, True)
    # c.setopt(pycurl.SSL_VERIFYHOST, 1)
    # c.setopt(c.VERBOSE, True)
    c.setopt(pycurl.CAINFO, "assets/cacert.pem")
    c.setopt(pycurl.COOKIEFILE, "tmp/cookies.txt")
    c.setopt(pycurl.COOKIEJAR, "tmp/cookies.txt")
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (compatible; MSIE 7.01; Windows NT 5.0)")
    c.setopt(pycurl.URL, url)
    c.perform()
    f.close()

    ##### load iframe
    soup = BeautifulSoup(open('tmp/StudentCentre.html','rb'))
    if_element = soup.find('iframe',id="ptifrmtgtframe")
    url =  str(if_element['src'])

    f = open('tmp/StudentCentre.html','w')
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEDATA, f)
    c.setopt(pycurl.SSLVERSION, 3)
    c.setopt(pycurl.SSL_VERIFYPEER, True)
    # c.setopt(pycurl.SSL_VERIFYHOST, 1)
    # c.setopt(c.VERBOSE, True)
    c.setopt(pycurl.CAINFO, "assets/cacert.pem")
    c.setopt(pycurl.COOKIEFILE, "tmp/cookies.txt")
    c.setopt(pycurl.COOKIEJAR, "tmp/cookies.txt")
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (compatible; MSIE 7.01; Windows NT 5.0)")
    c.setopt(pycurl.URL, url)
    c.perform()
    f.close()

    ##### make ajax request

    header = ['Content-type: application/x-www-form-urlencoded',
                    'Origin: http://upnet.up.ac.za'
                    ]

    soup = BeautifulSoup(open('tmp/StudentCentre.html'))
    hidden_fields = {}
    for i in soup.find_all("input",type = "hidden"):
        hidden_fields[i['name']] = i['value']
    hidden_fields['ICAction'] = 'UP_DERIVED_SSR_SS_ENRL_APP_LINK'
    hidden_fields['ICType'] = 'Panel'
    hidden_fields['ICAJAX'] = '1'
    hidden_fields['ICNAVTYPEDROPDOWN'] = '1'
    hidden_fields['ICStateNum'] = hidden_fields['ICStateNum']#str(int(hidden_fields['ICStateNum']) + 1)
    hidden_fields['ICChanged'] = '0'
    # print hidden_fields
    data = urllib.urlencode(hidden_fields)

    f = open('tmp/StudentCentre.html','w')
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEDATA, f)
    # c.setopt(c.VERBOSE, True)
    c.setopt(pycurl.COOKIEFILE, "tmp/cookies.txt")
    c.setopt(pycurl.COOKIEJAR, "tmp/cookies.txt")
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.POSTFIELDS, data)
    c.setopt(pycurl.POST,1)
    c.setopt(pycurl.HTTPHEADER, header)
    c.setopt(pycurl.REFERER, referer)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (compatible; MSIE 7.01; Windows NT 5.0)")
    c.setopt(pycurl.URL, "http://upnet.up.ac.za/psc/pscsmpra/EMPLOYEE/HRMS/c/UP_SS_MENU.UP_SS_STUDENT.GBL")
    c.perform()
    f.close()

    with open('tmp/cookies.txt','w') as f:
        f.write('')
    
    # Parse data

    
    

    soup = BeautifulSoup(open('tmp/StudentCentre.html'))

    

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
        with open(root+'/marks.txt','w') as file:
            file.write(big_string)

        # open
        import webbrowser
        webbrowser.open(root+"/marks.txt")
        
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
    
