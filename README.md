# Capstone Project

# Table of Contents

1. [Instalation Instructions](#installation-instructions)
    - 1.1. [To access the drive files](#access-drive-files)
    - 1.2. [To run the chat_app](#run-chat-app)
    - 1.3. [To save and push progress to main rep](#save-and-push-progress)
2. [File Information](#file-information)

---

## 1. Instalation Instructions <a name="installation-instructions"></a>

- Create environment with 'python -m venv env' <br>
- Activate environment with 'env\Scripts\activate' <br>
- Run 'pip install -r requirements.txt' <br>

 The instructions above are to be run in the terminal. <br>

**Note:** Always select the correct environment while running the notebooks, it's important. The option for env should appear at the top of the page, after trying to run a cell in the notebooks.

### 1.1. To access the drive files <a name="access-drive-files"></a>

**1st:** Add file 'credentials.json' to repository (it's already added to gitignore, so don't worry, it won't be tracked) <br>
**2nd:** Run 'download.py' to create the data files in the proper directory. They should appear in a directory called "Data".

Note: The files drive.py, Google.py and 'token_drive_v3.pickle' are just for setting up the Google Drive API.

### 1.2. To run the chat_app <a name="run-chat-app"></a>

- Add '.env' file, with the open ai key. 

The key must be added to a variable called 'OPENAI_API_KEY'

### 1.3. To save and push progress to main rep <a name="save-and-push-progress"></a>

>1.To check what hasn't been tracked yet

git status 

>2.To add everything 

git add .       

>3.To commit the changes 

git commit -m "NAME_OF_COMMIT"    

>4.To push changes to main repository (so that everyone has access to the changes)

git push -u origin main      


## 2. File Information <a name="file-information"></a>

We use Google Drive API to download our files directly from our personal drive, into a folder that is ignored by git, and that does not take too long to run. In any case, the files are only needed


### Needed Extensions (from Visual Studio Code):
- SQLite <br>
- SQLite3 Editor


The needed packages are in the requirements file. Use "pip install -r requirements.txt" in the terminal.


### Organizar por pastas depois:

>**Metadata:** <br>
- Metadata_Books.ipynb <br>
- Metadata_Movies.ipynb <br>
- Metadata_TV_Shows.ipynb <br
Mudar o nome destes ficheiros e criar um md com a descrição de cada feature em cada um deles.

>**Google api and downloads:** <br>
- Google.py <br>
- token_drive_v3.pickle (confirmar se dá) <br>
- drive.py <br>
- download.py 

>**Data (folder created after running download.py):** <br>
- Book_files <br>
- Movie_files <br>
- Tv_shows_files <br>
- users_data.db <br>
... 

>**Models:** <br>
- Cluster Model <br>
- Classifier Model <br>

>**Text Data:** <br>
- PDF file (or Vector DB) <br>


To run the app directly from the repository, you need to use the code "streamplit run chat_app.py"
>**The files related to the app are:** <br>
- chat_bot.py <br>
- chat_app.py <br>
- prompt_list.py <br>


>For now, our **test files** are (prob will be deleted): <br>
- user_data.db <br>
- user_profiles.db <br>
- test.py <br>
The user_data and user_profiles were used to test if the new user and old user attempts in the chat worked.


