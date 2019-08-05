# The existing script was for DBX for Business. Creating single DBX export. 

import csv
import dropbox
import os.path

from os import path

token_file = "token.txt"
save_location = "junk"

def get_token():
	token = ""
	with open(token_file) as f:
		token = f.readline()
	return token


def confirm_api():
	current = dbx.users_get_current_account()
	print("Logged in to account: {}".format(current.name.display_name))


def get_all_files(folder='', recursive=False):
	all_files = []
	folder_content = dbx.files_list_folder(folder).entries
	for entry in folder_content:
		if type(entry) is dropbox.files.FolderMetadata:
			print("{}".format(entry.path_lower))
			if recursive:
				get_all_files(folder=entry.path_lower, recursive=recursive)
		elif type(entry) is dropbox.files.FileMetadata:
			print("{} [{}]".format(entry.path_lower, entry.content_hash))
			all_files.append(entry)
	return all_files


def save_file(dbx_path, local_path):
	local_file = open(local_path, 'wb')
	metadata, f = dbx.files_download(dbx_path)
	local_file.write(f.content)
	local_file.close()


def save_all_files(folder=""):
	content_list = get_all_files(folder)
	for item in content_list:
		if type(item) is dropbox.files.FileMetadata and item.is_downloadable:
			if not path.exists(save_location + item.path_lower):
				print("Downloading {}".format(item.name))
				save_file(item.path_lower, save_location + item.path_lower)


def save_csv(file_list, destination="junk"):
	with open(destination + "/out.csv", 'w', newline='') as of:
		csvwriter = csv.writer(of, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for f in file_list:
			csvwriter.writerow([f.path_lower, f.content_hash])


dbx = dropbox.Dropbox(get_token())
confirm_api()
all_files = get_all_files(recursive=True)
save_csv(all_files)
