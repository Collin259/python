import sqlite3
import os 

print("Database saved at:", os.path.abspath("emaild.sqlite"))

conn = sqlite3.connect('emaild.sqlite')#it creates the file when it runs
cur = conn.cursor()#send the commands to the cursor

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = '/Users/collinchimene/Desktop/Class/code3/mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    email = line.split()[1]
    org = email.split('@')[1]  # Extract domain (e.g., 'example.com')  
    #dictionary part
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))# ?is a placeholder, and it make sure that we dont allow sqlinjection
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))#in databases is always better to do an update because there might be multiple applications
        #talking to this database at the same time
conn.commit()#commit forces everything to be written to disk and its the slowest part.Sometimes we do things like commit 
    #every 10th record or every 100th record
    #but when is a online screen you have to commint at the end of every sort of screen thing

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
conn.close()
