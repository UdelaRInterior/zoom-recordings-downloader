from zoom_recordings import download_recordings

domain_selected="example.com"

users_selected=["room01@"+domain_selected,"room02@"+domain_selected]
download_recordings(users_selected)

users_selected=[]
for i in range (1,8):
    users_selected.append("sala0"+str(i)+"@"+domain_selected)
download_recordings(users_selected)
