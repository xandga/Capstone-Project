import random
from openai import OpenAI
import re
from util import local_settings
#######################################################################################################
""" Creating User Database"""
import sqlite3

# Connect to SQLite database (creates one if doesn't exist)
conn = sqlite3.connect('Data/users_data.db')
cursor = conn.cursor()
"""
# Create a table for user profiles if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
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
"""
# Function to insert user profile into the database
def insert_user_profile(username, age, gender, fav_entertainment, least_fav_entertainment, likes, dislikes, movie_watching_freq, show_watching_freq, reading_freq, CritiPersonality):
    try:
        conn = sqlite3.connect('Data/users_data.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Users (username, age, gender, fav_entertainment, least_fav_entertainment, likes, dislikes, movie_watching_freq, show_watching_freq, reading_freq, CritiPersonality)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, age, gender, fav_entertainment, least_fav_entertainment, likes, dislikes, movie_watching_freq, show_watching_freq, reading_freq, CritiPersonality))
        
        conn.commit()
        conn.close()  # Close the connection after committing changes
        print("User profile inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting user profile: {e}")

                                                          
#######################################################################################################    
#### LOADING THE DATASETS ####
                  
import pandas as pd
movies = pd.read_csv("Data/Metadata/movies.csv")
shows = pd. read_csv("Data/Metadata/tvshows.csv")
books = pd.read_csv("Data/Metadata/books.csv")


from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
#######################################################################################################
#### PDF RELATED ####

from PyPDF2 import PdfReader
#from langchain.llms import OpenAI
import langchain_openai
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import llms

import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# Function to split text into chunks based on the number of words per chunk with overlap
def split_text_by_words_with_overlap(text, words_per_chunk, overlap):
    words = word_tokenize(text)
    chunks = []
    start = 0
    while start < len(words):
        chunk = " ".join(words[start:start + words_per_chunk])
        chunks.append(chunk)
        start += words_per_chunk - overlap  # Adding overlap
    return chunks

pdf = PdfReader("About CritiVerse.pdf")
pdf_text = ""

for page in pdf.pages:
    text = page.extract_text()
    if text:
        pdf_text += text

# Define the number of words per chunk and the overlap
words_per_chunk = 500  
overlap = 100  

# Split text into chunks based on the number of words per chunk with overlap
final_data = split_text_by_words_with_overlap(pdf_text, words_per_chunk, overlap)

embeddings = langchain_openai.OpenAIEmbeddings()
document_searcher = FAISS.from_texts(final_data, embeddings)

#######################################################################################################
classifier_data = pd.read_csv('Data/classification_data.csv')
import pickle

path = "classification_model.pkl"

with open(path, 'rb') as file:
    classifier_model = pickle.load(file)



from sklearn.preprocessing import MinMaxScaler ## we should use the minmaxscale since mostly are binary
# Scaling the feature 'age', since the model expects it
feat_scaler = MinMaxScaler()
data_scaled = feat_scaler.fit_transform(classifier_data[['age']])  #it can be done like this because in this case, what matters is the range of the age, and that did not vary between the train and validation data used in the model

def apply_preproc_steps(data):
    # Extracting age and gender from the input data
    user_age = int(data[1])  # Extracting age from the input
    user_age = feat_scaler.transform([[user_age]])[0][0]
    column_names = ['username','age','gender','fav_entertainment','least_fav_entertainment','likes', 'dislikes', 
                    'movie_watching_freq', 'show_watching_freq', 'reading_freq']

    # Create a DataFrame from the list with the specified column names
    data = pd.DataFrame([data], columns=column_names)
    # Mapping the user's preferences to the specific columns expected by the model
    pref_columns = ['dislikes_Comedy',
                    'fav_Tv-shows',
                    'dislikes_Thriller',
                    'dislikes_Animation',
                    'fav_Books',
                    'dislikes_Drama',
                    'likes_Biography',
                    'likes_Documentary',
                    'likes_Mystery',
                    'dislikes_Mystery',
                    'likes_Thriller',
                    'dislikes_Documentary']
 
    # Preprocess the columns to standardize the combinations
    # Preprocess the columns to standardize the combinations
    data['fav_entertainment'] = data['fav_entertainment'].apply(lambda x: ', '.join(sorted(x.split(', '))))
    data['least_fav_entertainment'] = data['least_fav_entertainment'].apply(lambda x: ', '.join(sorted(x.split(', '))))

    # One-hot encode 'fav_entertainment' column
    fav_encoded = data['fav_entertainment'].str.get_dummies(', ').add_prefix('fav_')

    # One-hot encode 'least_fav_entertainment' column
    least_fav_encoded = data['least_fav_entertainment'].str.get_dummies(', ').add_prefix('least_fav_')

    # Concatenate the new one-hot encoded columns with the original DataFrame
    data = pd.concat([data, fav_encoded, least_fav_encoded], axis=1)

    # Drop the original columns if needed
    data.drop(['fav_entertainment', 'least_fav_entertainment'], axis=1, inplace=True)

    
    data['likes'] = data['likes'].apply(lambda x: ', '.join(sorted(x.split(', '))))
    data['dislikes'] = data['dislikes'].apply(lambda x: ', '.join(sorted(x.split(', '))))

    # One-hot encode 'likes' column
    likes_encoded = data['likes'].str.get_dummies(', ').add_prefix('likes_')

    # One-hot encode 'dislikes' column
    dislikes_encoded = data['dislikes'].str.get_dummies(', ').add_prefix('dislikes_')

    # Concatenate the new one-hot encoded columns with the original DataFrame
    data = pd.concat([data, likes_encoded, dislikes_encoded], axis=1)

    # Drop the original columns if needed
    #users_encoded.drop(['likes', 'dislikes'], axis=1, inplace=True)


    # Create a dictionary to track user preferences mapped to model columns
    user_prefs = {col: 0 for col in pref_columns}
    
    # Assuming user's preferences start from the 4th element in the data list
    for pref in data[3:]:
        if pref in user_prefs:
            user_prefs[pref] = 1
    
    
    # Constructing the encoded data array in the specific order
    encoded_data = list(user_prefs.values()) + [user_age]
    
    return encoded_data


#######################################################################################################
####
#### ChatBot classes ####
####
def extract_user_details(response):
    user_info = {
        "username": "",
        "age": "",
        "gender": "",
        "fav_entertainment": "",
        "least_fav_entertainment": "",
        "likes": "",
        "dislikes": "",
        "movie_watching_freq":"",
        "show_watching_freq":"",
        "reading_freq":""
    }

    try:
        # Define keywords and their corresponding indices
        details_mapping = {
            "username": "Username:",
            "age": "Age:",
            "gender": "Gender:",
            "fav_entertainment": "Preferred entertainment method:",
            "least_fav_entertainment": "Least favorite entertainment method:",
            "likes": "Likes:",
            "dislikes": "Dislikes:",
            "movie_watching_freq": "Watching Frequency:" ,
            "show_watching_freq": "Watching Frequency:",
            "reading_freq": "Reading Frequency:"
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
    
def extract_user_details_from_database(username):
    try:
        conn = sqlite3.connect('Data/users_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT username, age, gender,fav_entertainment, least_fav_entertainment, likes, dislikes, movie_watching_freq, show_watching_freq, reading_freq, CritiPersonality
            FROM Users
            WHERE username=?
        ''', (username,))
        user_data = cursor.fetchone()
        conn.close()

        return user_data  # Returns a tuple with the user variables in order

    except sqlite3.Error as e:
        print(f"Error fetching user data from the database: {e}")
        return None


def extract_username_from_response(sentence):
    pattern = r"Username: ?([\w]+)?"
    match = re.search(pattern, sentence)
    if match:
        return match.group(1)
    else:
        return None
    
def extract_movie_titles(text):
    pattern = r'^- "(.*?)":'  # Adjusted pattern to match movie/tv show titles in the specified format
    movie_titles = re.findall(pattern, text, re.MULTILINE)
    return movie_titles

def extract_book_titles(text):
    pattern = r'"(.*?)" by'  # Updated pattern to capture book titles only
    book_titles = re.findall(pattern, text)
    return book_titles

    
def get_rating(data, data_column, title):
    # Convert the titles to lowercase for better matching
    data_column = data_column.str.lower()
    title = title.lower()

    # Vectorize the movie titles
    vectorizer = CountVectorizer().fit(data_column)
    data_vector = vectorizer.transform([title])

    # Compute cosine similarity between the input title and all titles in the dataset
    cosine_similarities = cosine_similarity(data_vector, vectorizer.transform(data_column))

    # Find the maximum similarity score
    max_similarity = cosine_similarities.max()

    # Compare the maximum similarity score with the threshold
    if max_similarity > 0.6:
        # Get the index of the content with the maximum similarity score
        index = cosine_similarities.argmax()
        # Get the corresponding rating
        return data.iloc[index]['CritiScore']
    else:
        return "Not Available"
#######################################################################################################
#                                                                                            
# OpenAI API                                                                                 
#                                                                                             

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

    # get completion from the model             
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
#######################################################################################################
#                                                                                     
# CritiBot                                                                            
#    
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
        
                  
    def generate_response(self, message: str):
        response = self.engine.get_completion(message)

        NEW_USER_ON = False
        OLD_USER_ON = False
        MOVIES_ON = False
        SHOWS_ON = False
        BOOKS_ON = False
        PDF_READER = False

        # Searhing for markers
        if "NEW_USER_ON" in response:
            NEW_USER_ON = True
            
        elif "OLD_USER_ON" in response:
            OLD_USER_ON = True

        elif "MOVIES_ON" in response:
            MOVIES_ON = True

        elif "SHOWS_ON" in response:
            SHOWS_ON = True

        elif "BOOKS_ON" in response:
            BOOKS_ON = True
        elif "PDF_READER" in response:
            PDF_READER = True

        ##################################################################
        if NEW_USER_ON:

            user_details = extract_user_details(response)  #this returns a tuple
            if user_details:

                print(response)

                #Classifying the type of user
                data_for_model = list(user_details)

                print(data_for_model)
                observation_to_predict = apply_preproc_steps(data_for_model)

                prediction = classifier_model.predict([observation_to_predict])
                print(prediction)

                old_user_messages = self.engine.messages.copy()  # Make a copy of current messages
                user_data_message = f"This is your CritiPersonality: {prediction[0]}"
                self.engine.messages = old_user_messages + [{"role": "assistant", "content": user_data_message}]
                
                NEW_USER_ON = False

                insert_user_profile(user_details[0], user_details[1], user_details[2], user_details[3], user_details[4], user_details[5], user_details[6], user_details[7], user_details[8], user_details[9], prediction[0])

                return user_data_message
            
        #################################################################
        """if OLD_USER_ON:
            print("OLD_USER_ON")
            old_username = extract_username_from_response(response)  # Extract old username from response

            old_user_data = extract_user_details_from_database(old_username)
            print(old_username)
            old_user_messages = self.engine.messages.copy()  # Make a copy of current messages
            user_data_message = f"This is your user data: {old_user_data}"
            self.engine.messages = old_user_messages + [{"role": "assistant", "content": user_data_message}]

            OLD_USER_ON = False 

            return user_data_message"""
            
        if OLD_USER_ON:
            print("OLD_USER_ON")
            old_username = extract_username_from_response(response)  # Extract old username from response

            print(f"Old Username extracted: {old_username}")  # Check if the username is correctly extracted

            old_user_data = extract_user_details_from_database(old_username)
            print(f"Old User Data: {old_user_data}")  # Check if old user data is retrieved from the database

            if old_user_data:
                old_user_messages = self.engine.messages.copy()  # Make a copy of current messages
                user_data_message = f"This is your user data: {old_user_data}"
                self.engine.messages = old_user_messages + [{"role": "assistant", "content": user_data_message}]

                OLD_USER_ON = False
                return user_data_message
            else:
                print("Old User Data not found in the database.")
                return "Your data was not found. Please create a new account or try again."

        
        ##################################################################
        if MOVIES_ON:
            titles = extract_movie_titles(response)
            scores = []

            for title in titles:
                score = get_rating(movies, movies["title"], title)
                scores.append(f"{title}: {score}\n\n")  # Append each movie title and score with an extra newline for paragraph spacing

            # Construct a message with movie titles and scores
            scores_message = "\n".join(scores)  # Join all titles and scores with paragraph spaces

            old_user_messages = self.engine.messages.copy()  # Make a copy of current messages
            user_data_message = f"These are the movie ratings:\n\n{scores_message}"  # Add additional newline for spacing before the movie ratings
            self.engine.messages = old_user_messages + [{"role": "assistant", "content": user_data_message}]

            MOVIES_ON = False

            return user_data_message
        
        ##################################################################
        if SHOWS_ON:
            titles = extract_movie_titles(response)
            scores = []
            
            for title in titles:
                score = get_rating(shows, shows["Series_title"],title)
                scores.append(f"{title}: {score}\n\n")  

            scores_message = "\n".join(scores)  # Join all titles and scores with paragraph spaces

            old_user_messages = self.engine.messages.copy()  # Make a copy of current messages
            user_data_message = f"These are the TV Show ratings:\n\n{scores_message}"  # Add additional newline for spacing before the ratings
            self.engine.messages = old_user_messages + [{"role": "assistant", "content": user_data_message}]

            SHOWS_ON = False

            return user_data_message

        ##################################################################
        if BOOKS_ON:
            titles = extract_book_titles(response)
            scores = []

            for title in titles:
                score = get_rating(books, books["title"], title)
                scores.append(f"{title}: {score}\n\n")  

            scores_message = "\n".join(scores)  # Join all titles and scores with paragraph spaces

            old_user_messages = self.engine.messages.copy()  # Make a copy of current messages
            user_data_message = f"These are the book ratings:\n\n{scores_message}"  # Add additional newline for spacing before the ratings
            self.engine.messages = old_user_messages + [{"role": "assistant", "content": user_data_message}]

            BOOKS_ON = False

            return user_data_message
        
        if PDF_READER:
            print('PDF_READER')

            docs =  document_searcher.similarity_search(response)

            chain = load_qa_chain(llms.OpenAI(), chain_type="stuff")

            user_data_message = chain.run(input_documents=docs, question=response)

            old_user_messages = self.engine.messages.copy()  # Make a copy of current messages
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
        

