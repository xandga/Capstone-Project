import sqlite3
from faker import Faker
import random

import os


#Do not run this again, just use the database availabe in the drive
# Specify the path to your database file
db_file_path = 'Data/users_data.db'

# Check if the file exists before attempting to delete it
if os.path.exists(db_file_path):
    os.remove(db_file_path)
    print(f"Database '{db_file_path}' deleted successfully.")
else:
    print(f"Database '{db_file_path}' does not exist or already deleted.")



fake = Faker()

# Define the path for the SQLite database
db_path = 'Data/users_data.db'

# Establish connection to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        age INTEGER,
        gender TEXT,
        fav_entertainment TEXT,
        least_fav_entertainment TEXT,
        likes TEXT,
        dislikes TEXT,
        movie_watching_freq TEXT,
        show_watching_freq TEXT,
        reading_freq TEXT
    )
''')

genres = ['Animation', 'Classics', 'Fantasy', 'Documentary', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 
          'Comedy', 'Drama', 'Action', 'Horror', 'Adventure', 'Fiction', 'History']

entertainment_types = ['Books', 'Movies', 'Tv-shows']
entertainment_types1 = ['Books', 'Movies', 'Tv-shows', 'None']

frequency = ['Never', 'Rarely', 'Daily', 'Weekly', 'Monthly']

generated_usernames = set()

# Generate and insert 10,000 unique rows of data
while len(generated_usernames) < 10000:
    username = fake.first_name() + str(random.randint(1, 9999))
    if username not in generated_usernames:
        generated_usernames.add(username)
        age = random.randint(19, 80)
        gender = random.choice(['F', 'M'])
        fav_entertainment = random.sample(entertainment_types, random.randint(1, 2))  # Multiple options for fav
        least_fav_entertainment = random.choice([fav for fav in entertainment_types1 if fav not in fav_entertainment])  # Ensure least_fav is different from fav
        likes = ', '.join(random.sample(genres, random.randint(1, 5)))
        dislikes = ', '.join(random.sample(genres, random.randint(1, 5)))
        movie_watching_freq = random.choice(frequency)
        show_watching_freq = random.choice(frequency)
        reading_freq = random.choice(frequency)

        cursor.execute('''
            INSERT INTO Users (username, age, gender, fav_entertainment, least_fav_entertainment, likes, dislikes, movie_watching_freq, show_watching_freq, reading_freq)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, age, gender, ', '.join(fav_entertainment), least_fav_entertainment, likes, dislikes, movie_watching_freq, show_watching_freq, reading_freq))

# Commit changes and close connection
conn.commit()
conn.close()
