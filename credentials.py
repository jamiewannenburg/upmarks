import os
import getpass

class credentials:
    """
    The credentials class handles the user's credentials. It has two attributes, namely: username and password.
    Also handles encryption and decryption of password.
    """
    def __init__(self,root=""):
        if root == "":
            self.dir = "tmp"
            self.root=""
        else:
            self.dir = root + "/tmp"
            self.root = root + "/"
        
        self.filename = self.dir + "/.credentials"
        self.username = ""
        self.password = ""
        self.email = ""
        
        # check if tmp exits
        d = os.path.relpath(self.dir)
        
        if not os.path.exists(d):
            os.makedirs(d)

    def get(self,input_func=raw_input,pass_input_func=getpass.getpass):
        """ Checks if file exitst. If it does it loads that info. If
        not: ask user for username and password. Encrypt password.
        Save these credentials in file (with write permitions). """
        # print disclaimer
        with open(self.root+"text/disclaimer.txt","r") as f:
            print f.read()
            
        # get user credentials
        username = input_func("Please type in your username: ")
        # format username
        if username[0] == 'u' or username[0] == 'U':
            username = username[1:]

        # encrypt password
        password_encrypted = self.encrypt(pass_input_func("Please type in your password: "))
        
        # save in file
        with open(self.filename,'w') as f:
            f.write(self.encrypt(username)+'\n'+password_encrypted)
        
        
        # load attributes
        self.username = username
        self.password = self.decrypt(password_encrypted)
        self.email = 'u' + self.username + '@tuks.co.za'
                    
    def load(self):
        """
        Load credentials from file. (Decrypring the password as well using decrypt())
        """
        
        # try to load the file else prompt user and save the file with get.
        try:
            with open(self.filename,"rb") as f:
                username = f.readline()[:-2]
                password = f.readline()
                self.username = self.decrypt(username)
                self.password = self.decrypt(password)
                self.email = "u"+self.username+"@tuks.co.za"
        except IOError:
            self.get()
        
    def decrypt(self,password):
        """
        Decrypt password and save as attribute.
        """
        from keyczar import keyczar
        from keyczar import keyczart
        location = self.dir + '/kz'
        d = os.path.relpath(location)
        if not os.path.exists(d):
            os.mkdir(d)
            s1='create --location=/'+location+' --purpose=crypt'
            s2 = 'addkey --location=/'+location+' --status=primary'
            keyczart.main(s1)
            keyczart.main(s1)
        crypter = keyczar.Crypter.Read(d)
        decrypted_password = crypter.Decrypt(password)
        return decrypted_password

    def encrypt(self,password):
        """
        Encrypt password and return encrypted password.
        """
        from keyczar import keyczar
        from keyczar import keyczart
        location = self.dir + '/kz'
        d = os.path.relpath(location)
        if not os.path.exists(d):
            os.mkdir(d)
            s1=['create', '--location='+d, '--purpose=crypt']
            s2 = ['addkey', '--location='+d, '--status=primary']
            keyczart.main(s1)
            keyczart.main(s2)
        crypter = keyczar.Crypter.Read(d)
        return crypter.Encrypt(password)

