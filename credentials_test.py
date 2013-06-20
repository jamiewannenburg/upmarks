import unittest
import os
import shutil
import credentials

ROOT = "test_environment"

def my_input(ret_val):
    return lambda msg: ret_val

class TestInitFirstRun(unittest.TestCase):
    def setUp(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)
                
    def tearDown(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)

    def test_make_tmp(self):
        credentials.credentials(root=ROOT)
        r = os.path.relpath(ROOT)
        p = os.path.join(r,"tmp")
        self.assertTrue(os.path.exists(p))

    def test_return(self):
        c = credentials.credentials(root=ROOT)
        self.assertEqual(c.filename, ROOT+"/tmp/.credentials")
        self.assertEqual(c.dir, ROOT+"/tmp")        
        
class TestGetFirstRun(unittest.TestCase):
    def setUp(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)
                
    def tearDown(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)

    def test_returns(self):
        c = credentials.credentials(root=ROOT)
        c.get(input_func=my_input("23958461"),pass_input_func=my_input("password"))
        self.assertEqual(c.username, "23958461")
        self.assertEqual(c.password, "password")
        self.assertEqual(c.email, "u23958461@tuks.co.za")
        
    def test_returns_with_u(self):
        c = credentials.credentials(root=ROOT)
        c.get(input_func=my_input("u23958461"),pass_input_func=my_input("password"))
        self.assertEqual(c.username, "23958461")
        self.assertEqual(c.password, "password")
        self.assertEqual(c.email, "u23958461@tuks.co.za")

    def test_returns_with_U(self):
        c = credentials.credentials(root=ROOT)
        c.get(input_func=my_input("U23958461"),pass_input_func=my_input("password"))
        self.assertEqual(c.username, "23958461")
        self.assertEqual(c.password, "password")  
        self.assertEqual(c.email, "u23958461@tuks.co.za")      

    def test_save(self):
        # check if get makes credentials file
        c = credentials.credentials(root=ROOT)
        p = os.path.relpath(c.filename)
        c.get(input_func=my_input("23958461"),pass_input_func=my_input("password"))
        self.assertTrue(os.path.exists(p))

##        # check contents of file        
##        with open(p) as f:
##            s = f.read()
##        test_s = c.encrypt("23958461") + '\n' + c.encrypt("password")
##        self.assertEqual(s,test_s)
        
class TestGet(unittest.TestCase):
    def setUp(self):
        self.c = credentials.credentials(root=ROOT)
        self.c.get(input_func=my_input("23958461"),pass_input_func=my_input("password"))
        self.username = "2847692"
        self.password = "new_password"
        self.email = "u2847692@tuks.co.za"
                
    def tearDown(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)

    def test_returns(self):
        self.c.get(input_func=my_input(self.username),pass_input_func=my_input(self.password))
        self.assertEqual(self.c.username, self.username)
        self.assertEqual(self.c.password, self.password)
        self.assertEqual(self.c.email, self.email)  

##    def test_save(self):
##        # check contents of credentials file
##        p = os.path.relpath(self.c.filename)
##        self.c.get(input_func=my_input(self.username),pass_input_func=my_input(self.password))
##        with open(p) as f:
##            s = f.read()
##        test_s = self.c.encrypt(self.username) + '\n' + self.c.encrypt(self.password)
##        self.assertEqual(s,test_s)

class TestLoadFirstRun(unittest.TestCase):
    def setUp(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)
                
    def tearDown(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)

##    def test_(self):

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.c = credentials.credentials(root=ROOT)
        self.username = "2847692"
        self.password = "password"
        self.email = "u2847692@tuks.co.za"
        self.c.get(input_func=my_input(self.username),pass_input_func=my_input(self.password))
                
    def tearDown(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)

    def test_return(self):
        self.c.load()
        self.assertEqual(self.c.username, self.username)
        self.assertEqual(self.c.password, self.password)
        self.assertEqual(self.c.email, self.email)

class TestEcryption():
    def setUp(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)
                
    def tearDown(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)
                
    def test_first_run(self):
        password = "my_crayzypasswordMMM182754"
        encrypted_password = credentials.credentials(root=ROOT).encrypt(password)
        decrypted_password = credentials.credentials(root=ROOT).decrypt(encrypted_password)
        self.assertEqual(password,decrypted_password)
        
        
if __name__=="__main__":
    # check if root exits
    d = os.path.relpath(ROOT)
    if not os.path.exists(d):
        os.makedirs(d)
    unittest.main()