
import urllib.request
import PyPDF2
import tempfile
import io
import re
import sqlite3
from pathlib import Path
import os

import re
from PyPDF2 import PdfFileReader


def fetchincidents(url):
    urllib.request.urlretrieve(url,'test.pdf')

    # data = urllib.request.urlopen(url).read()
    #data = io.BytesIO(data)
    #fp = tempfile.TemporaryFile()
    # Write the pdf data to a temp file
    #fp.write(data)
    # Set the curser of the file back to the begining
    #fp.seek(0)
    # Read the PDF

def extractincidents():
    file = open("test.pdf","rb")
    list = []
    pdfReader = PdfFileReader(file)
    # print(pdfReader)
    NoofPages = pdfReader.getNumPages()
    # print(NoofPages)
    # Get the first page

    page1 = (pdfReader.getPage(0).extractText())
    #print(page1)
    clear = re.compile("(cer)")
    list = clear.split(page1)
    # print(list)

    page1.split(";")
    list.append(page1[2])
    # print(list)
    list = [l.replace('-\n', '-') for l in list]
    list = [l.replace(' \n', ' ') for l in list]
    list = [l.replace(' / ', '/') for l in list]

    ListNew = (list[2].split(';'))
    FinalList = []
    FinalList = ListNew
    
    #print(FinalList)
    dblist = []
    for item in FinalList[:len(FinalList)-1]:
        item = item.split('\n')
        if(len(item) != 13):
            item.insert(7, 'N/A')
        item[7:11] = [' '.join(item[7:11])]
        dblist.append(item[1:])
    for lis in dblist:
        lis[6] = lis[6].replace('N/A', '')
        #print(lis, len(lis))

    return dblist

def createdb():
    my_file =Path("normanpd.db")
    if my_file.exists():
        os.remove("normanpd.db")

    conn = sqlite3.connect('normanpd.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE arrests (arrest_time TEXT,case_number TEXT,arrest_location TEXT,offense TEXT,
    arrestee_name TEXT, arrestee_birthday TEXT,arrestee_address TEXT,status TEXT,officer TEXT)''')
    pass
#Insert Data
def populatedb(incidents):
    #print(incidents)
    conn = sqlite3.connect('normanpd.db')
    c = conn.cursor()
    for item in incidents:
        c.execute('insert into arrests values (?,?,?,?,?,?,?,?,?)', item)
    conn.commit()
    pass

def status(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute('select * from arrests order by random() limit 5')
    print("Random five rows are :")
    #print(c)
    for row in c:
        a = ''
        for r in row:
            a = a + '"' + r + '"' + '$'
        print(a[:len(a)-1])



    rows = c.execute('select * from arrests')
    count = len(rows.fetchall())
    #print("The Number of rows are :", count)
