import json
import sys
import urllib2
import requests

import os

token = 'Bearer 5Ptoken'


gbl_file_success = 0
gbl_file_fail = 0
gbl_directory = 0

#----------------------------------------------------------------------------------------
# Functions
#----------------------------------------------------------------------------------------

def argument_error():
	#Clear the screen
	os.system('cls' if os.name == 'nt' else 'clear')
	print ""
	print 'WRONG number of arguments | Usage: save_data.py username@domain.com'
	print ""


def menu_screen():
	#Clear the screen
	choice = 0
	while choice < 1 or choice > 3: 
		os.system('cls' if os.name == 'nt' else 'clear')
		print "Options:"
		print "(1) List Files for " + sys.argv[1]
		print "(2) Download Files for " + sys.argv[1]
		print "(3) Quit"
		try:
			choice = input("$: ")
		except:
			pass
	return choice


def getAllDfBUsers():
	try:
		request = urllib2.Request('https://api.dropbox.com/1/team/members/list')
		request.add_header('Content-type', 'application/json')
		request.add_header('Authorization', token)
		body = str('{}')
		request.add_data(body)
		response = urllib2.urlopen(request)
		data = response.read()
		converted_data = json.loads(data)
		allmembers = [item["profile"] for item in converted_data["members"]]
		return allmembers
	except:
		return "Error in getAllDfBUsers()"


def getMemberIdFromEmail(all_members, email_to_find):
	for member in all_members:
		if member["email"] == email_to_find:
			return {"member_id":member["member_id"], "email":member["email"]}
		else:
			return "not_found"


def printFileList(path, dfb_member_id):
    if path is "":
        print "Empty path in GetFileList()"

    else:
        path = 'https://api.dropbox.com/1/metadata/auto' + path
        grequest = urllib2.Request(path)
        grequest.add_header('Content-type', 'application/json')
        grequest.add_header('X-Dropbox-Perform-As-Team-Member', dfb_member_id)
        grequest.add_header('Authorization', token)
        gresponse = urllib2.urlopen(grequest)
        gdata = gresponse.read()
        g_converted_data = json.loads(gdata)

        for item in g_converted_data["contents"]:
            if item["is_dir"] == True:
                print item["path"]
                try:
    				printFileList(str(item["path"]), dfb_member_id)
                except:
    				pass

            if item["is_dir"] == False:
            	print item["path"]

def saveFiles(dfb_member_email, dfb_member_id, path):

    directory = dfb_member_email

    if path is "":
        print "Empty path in GetFileList()"

    else:
        path = 'https://api.dropbox.com/1/metadata/auto' + path
        grequest = urllib2.Request(path)
        grequest.add_header('Content-type', 'application/json')
        grequest.add_header('X-Dropbox-Perform-As-Team-Member', dfb_member_id)
        grequest.add_header('Authorization', token)
        gresponse = urllib2.urlopen(grequest)
        gdata = gresponse.read()
        g_converted_data = json.loads(gdata)

        for item in g_converted_data["contents"]:
            if item["is_dir"] == True:
                global gbl_directory 
                gbl_directory= gbl_directory + 1
                print "[*] " + item["path"]
                if not os.path.exists(directory + item["path"]):
                    os.makedirs(directory + item["path"])
                try:
    				saveFiles(dfb_member_email, dfb_member_id, str(item["path"]))
                except:
    				pass

            if item["is_dir"] == False:
            	print "\t[+] " + item["path"]
            	download_target = item["path"]
            	try:
            	    print "\t\t[fetching]"
            	    file = dfbGet(download_target, dfb_member_id)
                    print "\t\t[content downloaded]"
                    outfile = open(directory + download_target, 'w+') #note: using download_target as file name for output also.
                    outfile.write(file)
                    print "\t\t[Written to disk]"
                    print "\t\t[SUCCESS]"
                    outfile.close()
                    global gbl_file_success 
                    gbl_file_success = gbl_file_success + 1
                except:
                	e = sys.exc_info()[0]
                	print "\t\t[FAILED]"
                	global gbl_file_fail 
                	gbl_file_fail = gbl_file_fail + 1


def dfbGet(path, dfb_member_id):
    path = 'https://content.dropboxapi.com/1/files/auto' + path
    #grequest = urllib2.Request(path)
    #grequest.add_header('X-Dropbox-Perform-As-Team-Member', dfb_member_id)
    #grequest.add_header('Authorization', token)
    #gresponse = urllib2.urlopen(grequest)
    #gdata = gresponse.read()
    #return gdata


    result = requests.get(path, 
              headers={'X-Dropbox-Perform-As-Team-Member': dfb_member_id, 'Authorization': token})

    return result.content

def finalOutput():
    print ""
    print ""
    print "User: " + target_user["email"]
    print "File Copy Success: " + str(gbl_file_success)
    print "File Copy Failure: " + str(gbl_file_fail)
    print "Directories parsed: " + str(gbl_directory)
    print ""
    print ""

#----------------------------------------------------------------------------------------
# Main Loop
#----------------------------------------------------------------------------------------

#Clear the screen
os.system('cls' if os.name == 'nt' else 'clear')

if len(sys.argv) == 2:
	
	# [-] Obtain the full member listing
	all_members = getAllDfBUsers()
	if all_members == "Error in getAllDfBUsers()":
		print all_members
		sys.exit()

	# [-] Locate the specified user
	target_user = getMemberIdFromEmail(all_members, sys.argv[1])
	if target_user == "not_found":
		print "Error in getMemberIdFromEmail(), User: " + target_user
		sys.exit()

	choice = menu_screen()
	# [Option 1] Promt the user to list out the files of the user:
	if choice == 1:
		print "Listing files for " + target_user["email"]
		printFileList('/', target_user["member_id"])

	# [Option 2] Create a directory and dump the files if the user says yes
	if choice == 2:
		print "Saving files for " + target_user["email"]
		saveFiles(target_user["email"], target_user["member_id"], "/")
		finalOutput()

else:
	argument_error()










