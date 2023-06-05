# azure_blob_test
# This script was written to test connection and file manipulating on azure storage blob.
# Program steps:
# Step 1: Create JSON file with data and save on local disk
# Step 2: Upload created JSON file to Azure storage
# Step 3: Removing JSON file from local drive
# Step 4: Download created JSON file from Azure storage and write to local disk
# Step 5: Tranfer data from json file to csv file and saving on local disk
# Step 6: Uploading file to Azure storage
# Step 7: Removing csv file from local drive
# Step 8: Downloading file from azure storage

import json
import csv

# Azure library to upload / download files
from azure.storage.blob import BlobServiceClient, BlobClient
import os

# Credentials for Azure storage
storage_account_key = "write storage_account_key here"
storage_account_name = "write storage_account_name here"
connection_string = "write connection_string here"
container_name = "write blob_container_name here"

# Files names
json_file_name = "user_list_objects_json.json"
csv_file_name = "user_list_object_csv.csv"
files_path = 'write file_path here'

# Example of user class
class User:
    def __init__(self, name, email, status):
        self.name = name
        self.email = email
        self.status = status

# init list of User objects with initial data and add it to list
users_list = [
    User("Lukasz", "lu.wp.pl", "admin"),
    User("Andrzej", "an.wp.pl", "technolog"),
    User("Pawel", "pa.wp.pl", "quality"),
    User("Ania", "an.wp.pl", "standard"),
    User("Basia", "ba.wp.pl", "standard"),
    User("Gabrysia", "ga.wp.pl", "standard"),
    User("Antos", "ant.wp.pl", "technolog"),
    User("Szymon", "sz.wp.pl", "standard"),
    User("Piotr", "pi.wp.pl", "quality"),
    User("Kamil", "ka.wp.pl", "standard")
 ]


# Upload file to Azure storage
def upload_to_blob_storage(file_path, file_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
    print(f"Uploaded file: {file_name} to azure storage.")

# Download file to Azure storage
def download_from_blob_storage(file_path, file_name):
    blob_client = BlobClient.from_connection_string(connection_string, container_name, file_name)
    with open(file_name, "wb") as sample_blob:
        blob_data = blob_client.download_blob()
        blob_data.readinto(sample_blob)
    print(F"File {file_name} downloaded from Azure and saved to local disk.")

# Delete file from local disk
def delete_file(file_name):
    os.remove(files_path + file_name)
    print(f"File {file_name} deleted from local drive.")


# Step 1: Create JSON file with data and save on local disk
# Convert User objects list to JSON format
json_data = json.dumps([obj.__dict__ for obj in users_list], indent=4)
print("List with objects dumped to JSON format.")
# Save object to json file
with open(json_file_name, 'w') as file:
    file.write(json_data)
print("List with objects saved to JSON file.")

# Step 2: Upload created JSON file to Azure storage
upload_to_blob_storage(files_path + json_file_name ,json_file_name )

# Step 3: Removing JSON file from local drive
delete_file(json_file_name)

# Step 4: Download created JSON file from Azure storage and write to local disk
download_from_blob_storage(files_path + json_file_name ,json_file_name )

# Step 5:Tranfer data from json file to csv file and saving on local disk
# Extract data from json file
with open(json_file_name, 'r') as file:
    json_data_from_file = json.load(file)
# Convert json to list of objects
user_object_list = []
for item in json_data_from_file:
    user_object_list.append(User(item['name'], item['email'], item['status'])) 
# saving list of users object to csv file
with open(csv_file_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Email", "Status"])
    for obj in user_object_list:
        writer.writerow([obj.name, obj.email, obj.status])
print("Data converted to csv and saved on disk.")

# Step 6: Uploading file to Azure storage
upload_to_blob_storage(files_path + csv_file_name, csv_file_name)

# Step 7: Removing csv file from local drive
delete_file(csv_file_name)

# Step 8: Downloading file from azure storage
download_from_blob_storage(files_path + csv_file_name ,csv_file_name )