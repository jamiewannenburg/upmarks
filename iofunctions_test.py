import unittest
import os
import shutil
import iofunctions

ROOT = "test_environment"

class TestMyLoggerFirstRun(unittest.TestCase):
    def setUp(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)
        d = os.path.relpath(ROOT)
        p = os.path.join(d,'tmp')
        self.p = os.path.join(p,'log.txt')
        os.makedirs(p)
        self.filename = ROOT+'/tmp/log.txt'
                
    def tearDown(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)

    def test_save(self):
        # check if makes credentials file
        test_s = "testing"
        iofunctions.my_logger(test_s,root=ROOT)
        self.assertTrue(os.path.exists(self.p))

        # check contents of file        
        with open(self.filename) as f:
            s = f.readline().split('\t')
        
        self.assertEqual(s[1],test_s+' \n')
                
class TestMyLogger(unittest.TestCase):
    def setUp(self):
        d = os.path.relpath(ROOT)
        p = os.path.join(d,'tmp')
        self.p = os.path.join(p,'log.txt')
        os.makedirs(p)
        self.filename = ROOT+'/tmp/log.txt'
                
    def tearDown(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)

    def test_save_4_logs(self):
        # check if makes credentials file
            
        test_s = "testing"
        iofunctions.my_logger(test_s,root=ROOT)
        iofunctions.my_logger(test_s,root=ROOT)
        iofunctions.my_logger(test_s,root=ROOT)
        iofunctions.my_logger(test_s,root=ROOT)
        self.assertTrue(os.path.exists(self.p))

        # check contents of file        
        with open(self.filename) as f:
            line = f.readline()
            s = []
            while line!= "":
                s.append(line.split('\t')[1])
                line = f.readline()
                
        self.assertEqual(s,[test_s+' \n' for i in range(4)])                

    def test_save_30_logs(self):
        # check if makes credentials file
        longstr = ''
        for i in range(30):
            longstr += str(i) + ' ' + str(i) +'\n'
        with open(self.filename,'w') as f:
            f.write(longstr)
            
        test_s = "testing"
        iofunctions.my_logger(test_s,root=ROOT)
        self.assertTrue(os.path.exists(self.p))

        # check contents of file        
        with open(self.filename) as f:
            line = f.readline()
            while line!= "":
                s = line.split('\t')
                line = f.readline()
                
        self.assertEqual(s[1],test_s+' \n')
        
    def test_save_60_logs(self):
        # check if makes credentials file
        longstr = ''
        for i in range(60):
            longstr += str(i) + ' ' + str(i) +'\n'
        with open(self.filename,'w') as f:
            f.write(longstr)
            
        test_s = "testing"
        iofunctions.my_logger(test_s,root=ROOT)
        self.assertTrue(os.path.exists(self.p))

        # check contents of file        
        with open(self.filename) as f:
            line = f.readline()
            count = 0
            while line!= "":
                s = line.split('\t')
                line = f.readline()
                count = count+1
                
        self.assertEqual(s[1],test_s+' \n')
        self.assertEqual(count,51)

class TestMarksChanged(unittest.TestCase):
    def setUp(self):
        p = os.path.relpath(ROOT)
        self.p = os.path.join(p,'marks.txt')
        self.filename = ROOT+'/marks.txt'
                
    def tearDown(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)

    def test_first_run(self):
        self.assertTrue(iofunctions.marks_changed(["maths","science"],["pass","pass"],["60","5"],root=ROOT))

    def test_true(self):
        with open(self.filename,'w') as f:
            f.write("maths\tpass\t60\nscience\tpass\t5\n")
        self.assertFalse(iofunctions.marks_changed(["maths","science"],["pass","pass"],["60","5"],root=ROOT))

    def test_false(self):
        with open(self.filename,'w') as f:
            f.write("maths\tpass\t60\nscience\tpass\t5\n")
        self.assertTrue(iofunctions.marks_changed(["maths","science"],["pass","fail"],["60","5"],root=ROOT))
        
    
if __name__=="__main__":
    # check if root exits
    d = os.path.relpath(ROOT)
    if not os.path.exists(d):
        os.makedirs(d)
    unittest.main()