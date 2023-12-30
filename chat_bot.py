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

        # Add a method in your CritiBot class to extract user details

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
            template = """
        Extract the username, age, likes, dislikes, and preferred entertainment method. 
        Please adapt the way the user is providing the information.

        TEXT: {response}

        EXAMPLE:
        - username: Ilona08
        - age: 25
        - likes: Movies, Music
        - dislikes: Spiders, Math
        - entertainment_preference: Movies

        OUTPUT: a list in the following format (which has to be able to be added to an SQLite database):
        username TEXT,
        age INTEGER,
        likes TEXT,
        dislikes TEXT,
        entertainment_preference TEXT
        """
            # Assuming the response contains user details in a structured format
            user_details = self.extract_user_details(response)
            if user_details:
                insert_user_profile(*user_details)
                return "User profile inserted successfully."

        return response

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

        return tuple(user_info.values())
    
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






