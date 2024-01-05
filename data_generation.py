import sqlite3
from faker import Faker
import random
import os

fake = Faker()

# Specify the path to your database file
db_file_path = 'Data/users_data.db'

# Check if the file exists before attempting to delete it
if os.path.exists(db_file_path):
    os.remove(db_file_path)
    print(f"Database '{db_file_path}' deleted successfully.")
else:
    print(f"Database '{db_file_path}' does not exist or already deleted.")

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
          'Comedy', 'Drama', 'Action', 'Horror', 'Adventure', 'History']

entertainment_types = ['Books', 'Movies', 'Tv-shows']
entertainment_types1 = ['Books', 'Movies', 'Tv-shows', 'None']

frequency = ['Never', 'Rarely', 'Daily', 'Weekly', 'Monthly']

generated_usernames = set()

# Define functions for realistic data generation
def generate_age():
    # Create a more realistic age distribution
    # Adjust weightage as per real-world demographics
    age_weights = [5, 10, 20, 25, 30, 40, 45, 50, 50, 50, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5,  # Ages 18-38
               5, 5, 5, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # Ages 39-80 # Ages 39-80
    age_population = list(range(18, 81))
    return random.choices(age_population, weights=age_weights)[0]

def generate_gender():
    # Simulate real-world gender distribution (adjust ratios as needed)
    gender_choices = ['F', 'M']
    gender_weights = [38, 62]  # Example gender ratio, adjust as needed
    return random.choices(gender_choices, weights=gender_weights)[0]

def generate_entertainment_preferences(age):
    # Correlate entertainment preferences with age groups
    if age <= 25:
        return random.sample(['Movies', 'Tv-shows'], random.randint(1, 2))
    elif age <= 40:
        return random.sample(['Movies', 'Books'], random.randint(1, 2))
    else:
        return random.sample(['Books', 'Tv-shows'], random.randint(1, 2))

def generate_likes_dislikes(age, gender):
    
    gender_based_likes = {
        'F': ['Romance', 'Fantasy', 'Animation', 'Comedy', 'Drama'],
        'M': ['Horror', 'Action', 'Sci-Fi', 'Adventure', 'War']
    }

    age_based_likes = {
        '18-25': ['Action', 'Comedy', 'Sci-Fi', 'Adventure', 'Horror', 'Animation'],
        '26-40': ['Drama', 'Mystery', 'Thriller', 'Documentary'],
        '41+': ['History', 'Biography', 'Classics', 'War']
    }

    age_category = '41+' if age > 40 else ('26-40' if age > 25 else '18-25')
    likes = gender_based_likes[gender] + age_based_likes[age_category]
    
    # Randomly shuffle likes and dislikes
    random.shuffle(likes)
    dislikes = [genre for genre in genres if genre not in likes]
    random.shuffle(dislikes)
    
    return likes[:random.randint(1, 5)], dislikes[:random.randint(1, 5)]

def generate_show_movie_reading_freq(fav_entertainment, least_fav_entertainment):
    show_watching_freq = random.choice(frequency)
    movie_watching_freq = random.choice(frequency)
    reading_freq = random.choice(frequency)

    if 'Movies' in fav_entertainment:
        movie_watching_freq = random.choice(['Daily', 'Weekly', 'Monthly'])
    if 'Tv-shows' in fav_entertainment:
        show_watching_freq = random.choice(['Daily', 'Weekly', 'Monthly'])
    if 'Books' in fav_entertainment:
        reading_freq = random.choice(['Daily', 'Weekly', 'Monthly'])

    if least_fav_entertainment == 'Movies':
        movie_watching_freq = random.choice(['Rarely', 'Never'])
    if least_fav_entertainment == 'Tv-shows':
        show_watching_freq = random.choice(['Rarely', 'Never'])
    if least_fav_entertainment == 'Books':
        reading_freq = random.choice(['Rarely', 'Never'])

    return movie_watching_freq, show_watching_freq, reading_freq

# Generate and insert 10,000 unique rows of data
while len(generated_usernames) < 10000:
    username = fake.first_name() + str(random.randint(1, 9999))
    if username not in generated_usernames:
        generated_usernames.add(username)
        age = generate_age()
        gender = generate_gender()
        fav_entertainment = generate_entertainment_preferences(age)

        least_fav_entertainment = random.choice([fav for fav in entertainment_types1 if fav not in fav_entertainment])  # Ensure least_fav is different from fav
        likes, dislikes = generate_likes_dislikes(age, gender)
        movie_watching_freq, show_watching_freq, reading_freq = generate_show_movie_reading_freq(fav_entertainment, least_fav_entertainment)

        # Convert lists to strings before insertion
        fav_entertainment_str = ', '.join(fav_entertainment)
        likes_str = ', '.join(likes)
        dislikes_str = ', '.join(dislikes)

        cursor.execute('''
            INSERT INTO Users (username, age, gender, fav_entertainment, least_fav_entertainment, likes, dislikes, movie_watching_freq, show_watching_freq, reading_freq)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, age, gender, fav_entertainment_str, least_fav_entertainment, likes_str, dislikes_str, movie_watching_freq, show_watching_freq, reading_freq))

# Commit changes and close connection
conn.commit()
conn.close()
