###############################################################################################
""" Creating User Database"""
import sqlite3

# Connect to SQLite database (creates one if doesn't exist)
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

# Create a table for user profiles if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY,
        username TEXT,
        age INTEGER,
        likes TEXT,
        dislikes TEXT,
        entertainment_preference TEXT
    )
''')

# Function to insert user profile into the database
def insert_user_profile(username, age, likes, dislikes, entertainment_preference):
    try:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO user (username, age, likes, dislikes, entertainment_preference)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, age, likes, dislikes, entertainment_preference))
        
        conn.commit()
        conn.close()  # Close the connection after committing changes
        print("User profile inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting user profile: {e}")

username = "Alice"
age = 30
likes = "Music, Sci fi"
dislikes = "Rain, comedy"
entertainment_preference = "Movies"

insert_user_profile(username, age, likes, dislikes, entertainment_preference)
