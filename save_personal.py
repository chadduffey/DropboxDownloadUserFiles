# The existing script was for DBX for Business. Creating single DBX export. 

import dropbox

token_file = "token.txt"


def get_token():
	token = ""
	with open(token_file) as f:
		token = f.readline()
	return token


def confirm_api():
	current = dbx.users_get_current_account()
	print("Logged in to account: {}".format(current.name.display_name))


def list_folder(folder=''):
	for entry in dbx.files_list_folder(folder).entries:
		print(entry.name)

def save_file(dbx_path, local_path):
	local_file = open(local_path, 'w')
	metadata, f = dbx.files_download(dbx_path)
	local_file.write(f.content)
	local_file.close()


dbx = dropbox.Dropbox(get_token())
confirm_api()
list_folder()
# {not ready} save_file("badchars.PNG", "junk/badchars.PNG")