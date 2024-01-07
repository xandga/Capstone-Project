# Capstone Project

# Table of Contents

1. [Instalation Instructions](#installation-instructions)
    - 1.1. [To access the drive files](#access-drive-files)
    - 1.2. [To run the chat_app](#run-chat-app)
    - 1.3. [Extensions](#extensions)
    - 1.4. [Libraries Instalation](#libraries)
2. [File Information](#file-information)

---

# 1. Instalation Instructions <a name="installation-instructions"></a>

- Create environment with 'python -m venv env' <br>
- Activate environment with 'env\Scripts\activate' <br>
- Run 'pip install -r requirements.txt' <br>

 The instructions above are to be run in the terminal. <br>

**Note:** Always select the correct environment while running the notebooks, it's important. The option for env should appear at the top of the page, after trying to run a cell in the notebooks.

## 1.1. To access the drive files <a name="access-drive-files"></a>
We use Google Drive API to download our files directly from our personal drive, into a folder that is ignored by git, and that does not take too long to run. In any case, the files are only needed.
- Add file 'credentials.json' (provided in the email) to repository (it's already added to gitignore, so don't worry, it won't be tracked), to the general folder, where the 1. Download.py file is <br>
- Run '1. Download.py' to create the data files in the proper directory. They should appear in a directory called "Data".

**Note:** The files drive.py, Google.py and 'token_drive_v3.pickle', present in the folder Google_Drive_API are just for setting up the Google Drive API.

The file credentials.json (provided in the email) must be added to the general folder, where the file download.py is, otherwise it will not be recognized.

>The Drive API should not redirect you to an authorization page, but in case it does and a warning that it is unsafe appears, click on "Advanced" and "Continue" (option that appears bellow the email) to proceed. 
In the unlikely case that this does not work, the files can be downloaded and moved manually into a folder called Data, the link is in the email. In that case, the zipped files will also need to be unzipped manually. This procedure is not expected to be needed, though, as simply running the '1.Download.py' file should work well and accomplish this.

## 1.2. To run the chat_app <a name="run-chat-app"></a>
It should be possible to access the chat app, CritiBot, through the link present in the website. But in case that, for some reason, that is not possible, it can also be done through the following steps: 
- Add '.env' file, with the open ai key. 
The key must be added to a variable called 'OPENAI_API_KEY'
- Run the files that start with "Metadata_" (files 2. ,3. and 4.) to obtain the preprocessed movie, shows and books datasets, with custom rating scores (CritiScores). The 2. Metadata_Movies.ipynb needs to be run first.
- Run chat_bot.py 
- Run 'streamlit run chat_app.py' in the terminal
   

## 1.3. Extensions (from Visual Studio Code): <a name="extensions"></a>
- SQLite <br>
- SQLite3 Editor

## 1.4. Libraries Instalation <a name="libraries"></a>
The needed packages are in the requirements file. Use "pip install -r requirements.txt" in the terminal.

# 2. File Information <a name="file-information"></a>
## Files

>**.streamlit** <br>
Has the theme used for the chat app. We decided to change a few of the colors from the base theme, in order to make the app more related to our company.

>**Data Folder:** (Appears after 1. Download.py runs)
- Book_files
- Metadata (only after notebooks 2, 3 and 4 run)
- Movie_files
- Tv_show_files
- classification_data.csv
- users_data.csv

>**Google_Drive_API:** <br>
Folder with files needed to run 1. Download.py, meaning that they have all the set up for the Google Drive API.
- Google.py <br>
- token_drive_v3.pickle <br>
- drive.py <br>

>**Prompts Folder:** <br>
Has the prompts used throughout the project.

>**Use Cases Images Folder:** <br>
Has the images used in the file Use_Cases.md, to showcase the uses of our chat app.

>**General Folder Files:** <br>
- **1.Download.py** <br>
It downloads the needed files from our drive, removing the need to do it manually.
- **2.Metadata_Movies.ipynb** <br>
Preprocessing datasets of movies in a format suited to us.
In case you want to run the metadata files again, this one needs to be ran first, since it's the one that creates the folder Metadata inside the Data folder.
- **3.Metadata_TV_Shows.ipynb** <br>
Preprocessing datasets of tv-shows in a format suited to us.
- **4.Metadata_Books.ipynb** <br>
Preprocessing datasets of books in a format suited to us.
- **5.Data_Generation.py** <br>
In this file, the 'users_data.db' was first created. We generated 10000 of user data randomly, with a few needed distributions of certain variables, that we could then use in our models.
- **6.Clustering.ipynb** <br>
Noteboook where we cluster our clients and create the CritiPersonalities. The output of this is the dataset classification_data.csv (which is in the folder Data, after running 1.Download.py). <br>
If the notebook is ran again, some outputs may change, as well as the dataset.
- **7.Classificaton model.ipynb** <br>
Noteboook where we train a classification model, that predicts the CritiPersonalities of our clients, so that we can classify new users based on their tastes. The output of this is the model classification_model.pkl (which is already in this folder). <br>
If the notebook is ran again, some outputs may change, as well as the selected features used in the model.
- **About Critiverse.pdf** <br>
PDF file that our chat bot will use to extract information about our company, Critiverse.
- **chat_app.py** <br>
Our chat app, CritiBot, is initialized there. We use streamlit in order to have a nice user interface for interacting with the CritiBot.
- **chat_bot.py** <br>
All the needed aspects that make the chat bot run and function are in this file. <br>
It needs to be Run, in case the case that the provided link does not work or a sort of test is needed, before running the chat_app.py file.
- **classification_model.pkl** <br>
Our model, that is called in the chat_bot.py, to be able to classify users into different types, created in the file 7.Classification_Model.ipynp
- **credentials.jsn** <br>
Credentials needed to access the Drive files, through Google Drive API.
- **logo.png** <br>
Image needed for the chat_app.py file, so that we can display our logo in the app.
- **prompt_list.py** <br>
File with the prompt we used to give our chat bot direction
- **README.md** <br>
Current file. Has instructions and explanations on the repository and its files.
- **requirements.txt** <br>
Needed packages to be able to run everything smoothly.
In order to run it, use, in the terminal, "pip install -r requirements.txt"
- **Use_Cases.md** <br>
This file has explanations and examples on how to approach and use the chat bot, for it to provide the best possible answers. It explains the uses of CritiBot, what information it can provide, and the best conversation steps to obtain them.
- **util.py** <br>
It accesses the openai_api_key and makes it possible to use it in the proper files.

**Note:** <br>
Some parts of our code, especially in the chat_app.py and chat_bot.py are from the classes. We added quite a bit, and changed what we needed, but the base is from the classes. 