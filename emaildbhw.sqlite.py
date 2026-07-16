import sqlite3
import os

DB_NAME = 'emaildbhw.sqlite'

if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

try:
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Counts (
            org TEXT PRIMARY KEY,
            count INTEGER
        )
    ''')
    conn.commit()
except sqlite3.Error as e:
    print(f"Error creating table: {e}")
    exit()

fname = input('Enter file name (or press enter for mbox.txt): ')
if len(fname) < 1: 
    fname = 'mbox.txt'

try:
    with open(fname) as fh:
        for line in fh:
            if not line.startswith('From: '):
                continue
                
            try:
                email = line.split()[1]
                org = email.split('@')[1]
                
                # Upsert operation (SQLite 3.24.0+ syntax)
                cur.execute('''
                    INSERT INTO Counts (org, count) 
                    VALUES (?, 1)
                    ON CONFLICT(org) DO UPDATE SET count = count + 1
                ''', (org,))
                
            except IndexError:
                print(f"Skipping malformed email: {line.strip()}")
                continue
        
        conn.commit()

except FileNotFoundError:
    print(f"Error: File '{fname}' not found.")
    exit()
except Exception as e:
    print(f"Unexpected error: {e}")
    exit()

# Verify the table exists and has data
try:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Counts'")
    if not cur.fetchone():
        print("Error: Counts table doesn't exist!")
        exit()
        
    cur.execute("SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10")
    results = cur.fetchall()
    
    if not results:
        print("No data found in Counts table!")
    else:
        print("\nTop 10 Organizations by Email Count:")
        for row in results:
            print(f"{row[0]}: {row[1]}")
            
except sqlite3.Error as e:
    print(f"Database error: {e}")

# Clean up
cur.close()
conn.close()