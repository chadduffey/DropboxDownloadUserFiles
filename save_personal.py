# The existing script was for DBX for Business. Creating single DBX export. 

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


def list_folder(folder='', recursive=False):
	folder_list = dbx.files_list_folder(folder).entries
	for entry in folder_list:
		if type(entry) is dropbox.files.FolderMetadata:
			print("{}".format(entry.path_lower))
			if recursive:
				list_folder(folder=entry.path_lower, recursive=recursive)
		elif type(entry) is dropbox.files.FileMetadata:
			print("{} [{}]".format(entry.path_lower, entry.content_hash))
	return folder_list


def save_file(dbx_path, local_path):
	local_file = open(local_path, 'wb')
	metadata, f = dbx.files_download(dbx_path)
	local_file.write(f.content)
	local_file.close()


def save_all_files(folder=""):
	content_list = list_folder(folder)
	for item in content_list:
		if type(item) is dropbox.files.FileMetadata and item.is_downloadable:
			if not path.exists(save_location + item.path_lower):
				print("Downloading {}".format(item.name))
				save_file(item.path_lower, save_location + item.path_lower)	


dbx = dropbox.Dropbox(get_token())
confirm_api()
list_folder(recursive=True)
save_all_files()
