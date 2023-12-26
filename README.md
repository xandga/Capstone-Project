# Capstone-Project
Capstone Project  

**1st**: Create environment with 'python -m venv env' <br>
**2nd**: Activate environment with 'env\Scripts\activate' <br>
**3rd**: Run 'pip install -r requirements.txt' <br>
- The instructions above are to be run in the terminal. <br>

**Note:** Always select the correct environment while running the notebooks, it's important. The option for env should appear at the top of the page, after trying to run a cell in the notebooks.

## **To access the drive files:**
**1st:** Add file 'credentials.json' to repository (it's already added to gitignore, so don't worry, it won't be tracked) <br>
**2nd:** Run 'download.py' to create the data files in the proper directory. They should appear in a directory called "Data".

Note: The files drive.py, Google.py and 'token_drive_v3.pickle' are just for setting up the Google Drive API.

## **To run the chat_app:**
- Add '.env' file, with the open ai key. The key must be added to a variable called 'OPENAI_API_KEY'

## **To save and push progress to main rep:**
>1.To check what hasn't been tracked yet

git status 

>2.To add everything 

git add .       

>3.To commit the changes 

git commit -m "NAME_OF_COMMIT"    

>4.To push changes to main repository (so that everyone has access to the changes)´

git push -u origin main      