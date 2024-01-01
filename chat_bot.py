###############################################################################################
""" Creating User Database"""
import sqlite3

# Connect to SQLite database (creates one if doesn't exist)
conn = sqlite3.connect('user_profiles.db')
cursor = conn.cursor()

# Create a table for user profiles if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles(
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
        conn = sqlite3.connect('user_profiles.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO user_profiles (username, age, likes, dislikes, entertainment_preference)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, age, likes, dislikes, entertainment_preference))
        
        conn.commit()
        conn.close()  # Close the connection after committing changes
        print("User profile inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting user profile: {e}")
###############################################################################################

"""
ChatBot classes
"""

import random
from openai import OpenAI
import re
from util import local_settings

# [i]                                                                                            #
# [i] OpenAI API                                                                                 #
# [i]                                                                                            #

class GPT_Helper:
    def __init__(self, OPENAI_API_KEY: str, system_behavior: str="", model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = []
        self.model = model

        if system_behavior:
            self.messages.append({
                "role": "system",
                "content": system_behavior
            })

    # [i] get completion from the model             #
    def get_completion(self, prompt, temperature=0):

        self.messages.append({"role": "user", "content": prompt})

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=temperature,
        )

        self.messages.append(
            {
                "role": "assistant",
                "content": completion.choices[0].message.content
            }
        )

        return completion.choices[0].message.content

# [i]                                                                                            #
# [i] CritiBot                                                                               #
# [i]                                                                                            #

class CritiBot:
    """
    Generate a response by using LLMs.
    """

    def __init__(self, system_behavior: str):
        self.__system_behavior = system_behavior

        self.engine = GPT_Helper(
            OPENAI_API_KEY=local_settings.OPENAI_API_KEY,
            system_behavior=system_behavior
        )
    '''
        # Add a method in your CritiBot class to extract user details
    def extract_user_details(self, response):
        user_info = {
            "username": "",
            "age": "",
            "likes": "",
            "dislikes": "",
            "entertainment_preference": ""
        }

        # Example extraction logic assuming response is structured
        for key in user_info:
            if key in response:
                start_index = response.find(key) + len(key) + 1
                end_index = response.find("\n", start_index)
                user_info[key] = response[start_index:end_index].strip()

        return tuple(user_info.values())'''
        
    def extract_user_details(self, response):
        user_info = {
            "username": "",
            "age": "",
            "likes": "",
            "dislikes": "",
            "entertainment_preference": ""
        }

        try:
            # Define keywords and their corresponding indices
            details_mapping = {
                "username": "Username:",
                "age": "Age:",
                "likes": "Likes:",
                "dislikes": "Dislikes:",
                "entertainment_preference": "Preferred entertainment method:"
            }

            # Extract each user detail based on keywords
            for key, keyword in details_mapping.items():
                if keyword in response:
                    detail_start = response.find(keyword) + len(keyword)
                    detail_end = response.find("\n", detail_start)
                    user_info[key] = response[detail_start:detail_end].strip()

        except Exception as e:
            print(f"Error extracting user details: {e}")

        return tuple(user_info.values())
    
    def extract_user_details_from_database(self, username):
        try:
            conn = sqlite3.connect('user_profiles.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT username, age, likes, dislikes, entertainment_preference 
                FROM user_profiles 
                WHERE username=?
            ''', (username,))
            user_data = cursor.fetchone()
            conn.close()

            return user_data  # Returns a tuple (username, age, likes, dislikes, entertainment_preference)

        except sqlite3.Error as e:
            print(f"Error fetching user data from the database: {e}")
            return None
        
    
    def extract_username_from_response(self, sentence):
        pattern = r'Username: (\w+)\.'
        match = re.search(pattern, sentence)
        if match:
            return match.group(1)
        else:
            return None


    def generate_response(self, message: str):
        response = self.engine.get_completion(message)

        NEW_USER_ON = False
        OLD_USER_ON = False

        # Check if new or old user
        if "NEW_USER_ON" in response:
            NEW_USER_ON = True
            
        elif "OLD_USER_ON" in response:
            OLD_USER_ON = True

        if NEW_USER_ON:

            # Assuming the response contains user details in a structured format
            user_details = self.extract_user_details(response)
            if user_details:
                insert_user_profile(user_details[0], user_details[1], user_details[2], user_details[3], user_details[4])
                return "User profile inserted successfully."
                    

        if OLD_USER_ON:
            old_username = self.extract_username_from_response(response)  # Extract old username from response
            # Assuming the response contains user details in a structured format
            old_user_data = self.extract_user_details_from_database(old_username)

            formatted_data = f"This is your user data: {old_user_data}"
            print("The username is", old_username)
            old_user_messages = self.engine.messages.copy()  # Make a copy of current messages
            user_data_message = f"This is your user data: {old_user_data}"
            self.engine.messages = old_user_messages + [{"role": "assistant", "content": user_data_message}]

            return user_data_message

        return response

    def __str__(self):
        shift = "   "
        class_name = str(type(self)).split('.')[-1].replace("'>", "")

        return f"🤖 {class_name}."

    def reset(self):
        ...

    @property
    def memory(self):
        return self.engine.messages

    @property
    def system_behavior(self):
        return self.__system_config

    @system_behavior.setter
    def system_behavior(self, system_config : str):
        self.__system_behavior = system_config
        
        
# Creating an instance of CritiBot
criti_bot_instance = CritiBot(system_behavior='your_behavior_string')

