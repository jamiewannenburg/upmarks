
def my_logger(message,root=""):
    """
    log the date and the message in the file /root/tmp/log.txt
    """
    if root=="":
        filename = "tmp/log.txt"
    else:
        filename = root+'/tmp/log.txt'
    try:
        with open(filename,'r') as f:
            logs = []
            line = f.readline()
            while line != "":
                logs.append(line)
                line = f.readline()
            S=''
            for log in logs[-50:]:
                S+=log
    except IOError:
        S=''
        
    with open(filename,'w') as f:
        from datetime import datetime
        from time import time
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        S += date + '\t' + message + ' \n'
        f.write(S)

def build_and_send_email(c,marks):
    """
    build an email using MIME and send using smtplib
    """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Nuwe Punte'
    msg['From'] = c.email
    msg['To'] = c.email
    text = 'Nuwe Punte is uit!\n'+marks
    part1 = MIMEText(text.encode("UTF-8"), 'plain')
    msg.attach(part1)
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(c.email,c.password)  
    server.sendmail(c.email, c.email, msg.as_string())  
    server.quit()

def marks_changed(names,descriptions,grades,root=""):
    """
    checks whether names,decriptions and grades are the same as those saved in marks.txt
    """
    if root=="":
        filename = "marks.txt"
    else:
        filename = root+"/marks.txt"
        
    changed = False
    try:
        with open(filename) as file:
            for i, name in enumerate(names):
                line = file.readline().decode('UTF-8')
                old_name,old_description,old_grade = line.split('\t')
                if old_name != name:
                    print old_name + ' changed to ' + name + '\n'
                    changed = True
                elif old_description != descriptions[i]:
                    print old_description + ' changed to ' + descriptions[i] + '\n'
                    changed = True
                elif grades[i]==old_grade:
                    changed = False
                elif old_grade[:-1] != grades[i]:
                    print old_grade[:-1] + ' changed to ' + grades[i] + '\n'
                    changed = True
    except IOError:
        print "marks.txt does not exist/\n"
        changed = True
    except ValueError:
        print "subjects have changed\n"
        changed = True
    return changed
        
