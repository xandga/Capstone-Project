import sqlite3
from faker import Faker
import random

#Do not run this again, just use the database availabe in the drive

fake = Faker()

# Define the path for the SQLite database
db_path = 'Data/users_data.db'  # Replace 'your_desired_path' with your desired path

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
        location TEXT,
        fav_entertainment TEXT,
        least_fav_entertainment TEXT,
        likes TEXT,
        dislikes TEXT,
        movie_watching_freq TEXT,
        show_watching_freq TEXT,
        reading_freq TEXT
    )
''')

genres = ['Animation', 'Classics','Fantasy','Documentary', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 
          'Comedy', 'Drama', 'Action', 'Horror', 'Adventure', 'Fiction', 'History']

entertainment_types = ['Books', 'Movies', 'Tv-shows']
frequency = ['Never','Rarely','Daily', 'Weekly', 'Monthly']

generated_usernames = set()

# Generate and insert 10,000 unique rows of data
while len(generated_usernames) < 10000:
    username = fake.first_name() + str(random.randint(1, 9999))
    if username not in generated_usernames:
        generated_usernames.add(username)
        age = random.randint(19, 70)
        gender = random.choice(['F', 'M'])
        location = fake.country()
        fav_entertainment = random.choice(entertainment_types)
        least_fav_entertainment = random.choice(['Books', 'Movies', 'Tv-shows', 'None'])
        likes = ', '.join(random.sample(genres, random.randint(1, 5)))
        dislikes = ', '.join(random.sample(genres, random.randint(1, 5)))
        movie_watching_freq = random.choice(frequency)
        show_watching_freq = random.choice(frequency)
        reading_freq = random.choice(frequency)

        cursor.execute('''
            INSERT INTO Users (username, age, gender, location, fav_entertainment, least_fav_entertainment, likes, dislikes, movie_watching_freq, show_watching_freq, reading_freq)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, age, gender, location, fav_entertainment, least_fav_entertainment, likes, dislikes, movie_watching_freq, show_watching_freq, reading_freq))

# Commit changes and close connection
conn.commit()
conn.close()


#Do not run this again, just use the database availabe in the drive