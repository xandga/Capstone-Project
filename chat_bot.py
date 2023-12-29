###############################################################################################
""" Creating User Database"""
import sqlite3

# Connect to SQLite database (creates one if doesn't exist)
conn = sqlite3.connect('user_profiles.db')
cursor = conn.cursor()

# Create a table for user profiles if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
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
    cursor.execute('''
        INSERT INTO users (username, age, likes, dislikes, entertainment_preference)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, age, likes, dislikes, entertainment_preference))
    conn.commit()

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
    def __init__(self,
        OPENAI_API_KEY: str,
        system_behavior: str="",
        model="gpt-3.5-turbo",
    ):
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
    def extract_user_details(self, r2):
        # Extract user details using your logic based on the response
        # This logic should parse the response and extract the necessary user details
        username = r2[0]
        age = r2[1]  # Extracted age
        likes = r2[2]
        dislikes = r2[3]
        entertainment_preference = r2[4]

        return username, age, likes, dislikes, entertainment_preference
    
    def generate_response(self, message: str):
        response = self.engine.get_completion(message)

        NEW_USER_ON = False
        # if the command is identified
        if response.find("NEW_USER_ON") >= 0 :
            NEW_USER_ON = True
            

        if NEW_USER_ON:
            template = f"""
            Extract the username, age, likes, dislikes and preferred entertainment method.

            TEXT: {response}

            EXAMPLE:
            - username: Ilona08
            - petal length (cm): 1.2
            - petal width (cm): 0.2

            OUTPUT: a list in the following format (which has to be able to be added to an sqllite database):
            username TEXT,
            age INTEGER,
            likes TEXT,
            dislikes TEXT,
            entertainment_preference TEXT
            """
            r2 = self.engine.get_completion(template, temperature=1,)

            #insert_user_profile(r2[0], r2[1], r2[2], r2[3], r2[4])


            user_details = self.extract_user_details(r2)  # Extract user details
            if user_details:  # Ensure user_details is not empty
                insert_user_profile(*user_details)  # Insert user details into the database


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



