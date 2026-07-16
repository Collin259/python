import sqlite3
import csv
import os

# Connect to the database (or create it)
conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Clear old tables if they exist
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title   TEXT UNIQUE,
    artist_id  INTEGER
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

# Ask user for filename
fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "tracks.csv"

# Debug: Show full path it's trying to open
print("Trying to open:", os.path.abspath(fname))

# Open the CSV file
try:
    with open(fname, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row

        for row in reader:
            if len(row) < 7:
                continue  # Skip bad rows

            # Pull needed fields from row
            name = row[0]
            artist = row[1]
            album = row[2]
            genre = row[3]
            length = row[4]
            rating = row[5]
            count = row[6]

            if not name or not artist or not album or not genre:
                continue  # Skip if anything important is missing

            # Insert Artist
            cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES ( ? )', (artist,))
            cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist,))
            artist_row = cur.fetchone()
            if artist_row is None:
                print("Skipping artist:", artist)
                continue
            artist_id = artist_row[0]

            # Insert Genre
            cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES ( ? )', (genre,))
            cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre,))
            genre_row = cur.fetchone()
            if genre_row is None:
                print("Skipping genre:", genre)
                continue
            genre_id = genre_row[0]

            # Insert Album
            cur.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES ( ?, ? )', (album, artist_id))
            cur.execute('SELECT id FROM Album WHERE title = ? ', (album,))
            album_row = cur.fetchone()
            if album_row is None:
                print("Skipping album:", album)
                continue
            album_id = album_row[0]

            # Insert or Replace Track
            cur.execute('''INSERT OR REPLACE INTO Track
                (title, album_id, genre_id, len, rating, count)
                VALUES (?, ?, ?, ?, ?, ?)''',
                (name, album_id, genre_id, length, rating, count))

except FileNotFoundError:
    print(f"Error: File '{fname}' not found.")
    exit()

conn.commit()
cur.close()
print("✅ Database 'trackdb.sqlite' created successfully.")
