from zoomus import ZoomClient
from decouple import config
import requests
from datetime import date, datetime
from dateutil.parser import parse
import os
import json
import re
from unicodedata import normalize

def save_log(message,running_start_time):
    log_file_path = config('log_dir_path')+'/downloads-'+running_start_time.strftime("%Y-%m-%d-%H-%M-%S")+".log"
    with open(log_file_path, "a") as myfile:
	    myfile.write(str(message)+ "\n")

def download_file(running_start_time, url, download_file_path, file_size_expected):
    download=False
    expired = False
    #File exists?
    if os.path.exists(download_file_path):
        #File size is correct?
        real_file_size = os.path.getsize(download_file_path)
        if real_file_size != file_size_expected:
            download=True
            #Error
            save_log("Exists but... file size expected: "+str(file_size_expected)+" <> obtained file size: "+str(real_file_size),running_start_time)
    else:
        download=True

    if download:
        #Download
        save_log("Downloading...",running_start_time)
        resp = requests.get(url, stream=True, allow_redirects=True)
        with open(download_file_path, 'wb') as f:
            for chunk in resp.iter_content(1024):
                if not chunk:
                    break
                f.write(chunk)                        

        #File size is correct?
        real_file_size = os.path.getsize(download_file_path)
        if real_file_size != file_size_expected:
            #Error
            save_log("File downloaded but... file size expected: "+str(file_size_expected)+" <> obtained file size: "+str(real_file_size),running_start_time)
            #Token Expired Check
            try:
                expired = False
                #it's a small file?
                if real_file_size < 300:
                    with open(download_file_path) as f:
                        file_content = f.read()
                    response_objects = json.loads(file_content)
                    if response_objects['errorMessage']=="Forbidden":
                        save_log("Token expired",running_start_time)
                        expired = True
            except:
                expired = False
    return not expired

def download_all_files(files_to_download, access_token, running_start_time):
    API_KEY = config('API_KEY')
    API_SECRET = config('API_SECRET')
    save_log("*** Start downloading all files ***",running_start_time)    
    for ftd in files_to_download:
        save_log (ftd["download_file_path"],running_start_time)
        url = ftd["download_url"]+"?access_token="+access_token
        success=download_file(running_start_time, url, ftd["download_file_path"], ftd["file_size_expected"])
        while not success:
            client = ZoomClient(API_KEY, API_SECRET)
            access_token=client.config["token"]                           
            url = ftd["download_url"]+"?access_token="+access_token
            success=download_file(running_start_time, url, ftd["download_file_path"], ftd["file_size_expected"])

def token_expired_check(response_objects, running_start_time):
    expired = True
    try:
        if response_objects['message']=="Access token is expired.":
            save_log("Token expired",running_start_time)
            expired = True
        else:
            expired = False
    except:
        expired = False
    return expired

def download_recordings(users_selected):

    API_KEY = config('API_KEY')
    API_SECRET = config('API_SECRET')
    download_root_path=config('download_root_path')
    start_year=int(config('start_year'))
    start_month=int(config('start_month'))
    start_day_of_month=int(config('start_day_of_month'))
    running_start_time=datetime.now()
    files_to_download=[]
    resend_request = True
    page_size = 300
    user_page = 0

    client = ZoomClient(API_KEY, API_SECRET)
    access_token=client.config["token"]
    user_list_response = client.user.list(page_size=page_size)
    user_list = json.loads(user_list_response.content)
    total_user_pages=user_list["page_count"]
    
    save_log("*** Getting user recordings from Zoom ***",running_start_time) 

    while user_page < total_user_pages:

        for user in user_list['users']:
            email = user['email']
            if email in users_selected:
                uid = user['id'] 
                room = email.split("@")[0]
                save_log("Room: " + room,running_start_time)
        
                ##Month by Month
                year_iterator=start_year
                month_iterator=start_month

                while date(year_iterator,month_iterator, start_day_of_month) <= date.today():

                    search_start_year = year_iterator
                    search_start_month = month_iterator
                    search_end_year = year_iterator
                    search_end_month =  month_iterator+1          
                    if month_iterator>=12:
                        search_end_month = 1
                        month_iterator = 1
                        search_end_year = year_iterator + 1
                        year_iterator = year_iterator + 1
                    else:
                        month_iterator=month_iterator+1
                    search_start_date = date(search_start_year,search_start_month,start_day_of_month)
                    search_end_date = date(search_end_year,search_end_month,start_day_of_month)

                    recordings_page=0
                    resend_request = True
                    while (resend_request):
                        user_recordings_response = client.recording.list(user_id=uid, start=search_start_date, end=search_end_date, page_size=page_size)
                        user_recordings = json.loads(user_recordings_response.content)
                        total_recordings_pages=user_recordings["page_count"]
                        next_page_token=user_recordings["next_page_token"]
                        resend_request = token_expired_check(user_recordings, running_start_time)
                        if resend_request:
                            client = ZoomClient(API_KEY, API_SECRET)
                            access_token=client.config["token"]

                    save_log("From: "+user_recordings['from'],running_start_time)
                    save_log("To: "+user_recordings['to'],running_start_time)
                    while recordings_page < total_recordings_pages:
                        save_log("Page: "+str(recordings_page+1),running_start_time)

                        for meeting in user_recordings['meetings']:
                            topic = meeting['topic']
                            meeting_start_date=parse(meeting['start_time'])
                            meeting_day=meeting_start_date.strftime("%Y-%m-%d")
                            meeting_hour=meeting_start_date.strftime("%H-%M-%S")

                            for recording_file in meeting['recording_files']:
                                file_type = ""
                                try:
                                    file_type = recording_file['file_type']
                                except:
                                    save_log("file type missing",running_start_time)
                                
                                if file_type == "MP4":
                                    file_id = recording_file['id']
                                    topic_normalized = re.sub('[^0-9A-Z_a-z??-????-????-??]+', '_', normalize("NFKD", topic).encode("ascii","ignore").decode("ascii"))
                                    file_name = topic_normalized+"-"+meeting_hour+"-"+file_id+".mp4"
                                    download_dir_path = download_root_path+"/"+room+"/"+meeting_day+"/"
                                    download_file_path = download_dir_path+file_name
                                    save_log (download_file_path,running_start_time)

                                    if (os.path.isdir(download_dir_path)==False):
                                        os.makedirs(download_dir_path)
                                    files_to_download.append({"download_url":recording_file['download_url'],"download_file_path":download_file_path,"file_size_expected":recording_file['file_size']})

                        recordings_page=recordings_page+1
                        resend_request = True
                        while (resend_request and recordings_page < total_recordings_pages):
                            user_recordings_response = client.recording.list(user_id=uid, start=search_start_date, end=search_end_date, page_size=page_size, next_page_token=next_page_token)
                            user_recordings = json.loads(user_recordings_response.content)
                            next_page_token=user_recordings["next_page_token"]
                            resend_request = token_expired_check(user_recordings, running_start_time)
                            if resend_request:
                                client = ZoomClient(API_KEY, API_SECRET)
                                access_token=client.config["token"]

                    save_log("All pages reached? "+ str(recordings_page >= total_recordings_pages) ,running_start_time)
    
        user_page=user_page+1
        resend_request = True
        while (resend_request):
            user_list_response = client.user.list(page_size=page_size, page_number=user_page)
            user_list = json.loads(user_list_response.content)
            resend_request = token_expired_check(user_list, running_start_time)
            if resend_request:
                client = ZoomClient(API_KEY, API_SECRET)
                access_token=client.config["token"]

    #At the end download all files
    download_all_files(files_to_download, access_token, running_start_time)
