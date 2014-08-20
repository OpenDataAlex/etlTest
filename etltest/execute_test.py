import sys
import subprocess


class executeTest():

    def execute(self):
        #p = subprocess.Popen(['echo', 'Hello!'], stdout=subprocess.PIPE)
        p = subprocess.Popen(['python', '/home/ameadows/Documents/etlTest/output/DataMart/UsersDim.py'], stdout=subprocess.PIPE)

        print p.communicate()

if __name__ == "__main__":
    executeTest().execute()