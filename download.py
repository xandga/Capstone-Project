from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
import os
from drive import service

# Path where you want to save the downloaded files
import os

# Specify the path for the new folder
new_folder_path = 'Data'

# Check if the folder doesn't exist, then create it
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
    print(f"Folder '{new_folder_path}' created successfully.")
else:
    print(f"Folder '{new_folder_path}' already exists.")

download_folder = 'Data'

'''def authenticate_google_drive():
    # Load credentials from a previously saved token.json file or use any other authentication flow
    creds = Credentials.from_authorized_user_file('credentials.json')  

    # Build the Drive service
    service = build('drive', 'v3', credentials=creds)
    return service'''

def download_files_from_drive(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    # Download the file
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    # Save the downloaded file to the specified folder
    with open(os.path.join(download_folder, file_name), 'wb') as f:
        fh.seek(0)
        f.write(fh.read())

def main():
    #service = authenticate_google_drive()

    # Replace with your file IDs and corresponding file names
    files_to_download = [
        {'id': '1zNel2pa4_d2o2nRT4xYhAKknzii-mTfl', 'name': 'Tv_show_files.zip'},
        {'id': '1FaE2PAI1RDZXP4v-ou99JEDQvdRIUzzQ', 'name': 'Movie_files.zip'},
        {'id': '1WpCfMac70-I_eUlbUDQoRCNDDTuV6XEa', 'name': 'Book_files.zip'}
    ]

    for file_info in files_to_download:
        file_id = file_info['id']
        file_name = file_info['name']
        download_files_from_drive(service, file_id, file_name)


if __name__ == "__main__":
    main()


import zipfile
import os

# Function to unzip files
def unzip_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(root)
                os.remove(file_path)  # Remove the zip file after extraction



# Unzip the downloaded files
unzip_files(download_folder)
