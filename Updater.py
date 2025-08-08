import requests, wget
import os
import json
import time

links=(
"http://updater.project-epoch.net/api/v2/latest?file=Project-Epoch.exe",
"http://updater.project-epoch.net/api/v2/latest?file=ClientExtensions.dll",
"http://updater.project-epoch.net/api/v2/latest?file=patch-A.MPQ",
"http://updater.project-epoch.net/api/v2/latest?file=patch-B.MPQ",
"http://updater.project-epoch.net/api/v2/latest?file=patch-Y.MPQ",
"http://updater.project-epoch.net/api/v2/latest?file=patch-Z.MPQ",
"http://updater.project-epoch.net/api/v2/latest?file=realmlist"
)

ShaApi = 'https://updater.project-epoch.net/api/v2/manifest?environment=production'

path = "."

# Check if update API is aviable
for times in range(3):

    try:
        response = requests.get(ShaApi,allow_redirects=True)
    except:
        if times == 2:
            print(f"\nTry number {times+1} unsuccesfull\nNo response from server, quiting")
            quit()
        
        print(f"\nTry number {times+1} unsuccesfull\n retrying in 3 seconds")
        time.sleep(3)



if response.status_code == 200:

    # Store current version from website
    jsonData = response.json()
    websiteVersion = jsonData["Version"]
    print("Current Web Version: "+ websiteVersion)

    # Compare website with local version
    with open("Current_Version.json") as localVersionFile:

        local = json.load(localVersionFile)
        localVersion = local["Version"]

        # Update uptional if new version detected
        if localVersion != websiteVersion: 
            print(f"\nNew version in town\nLocal: {localVersion}\nNew: {websiteVersion}\n")
            print("Update?\ny/n")
            option = input()

            if option == "n":
                quit()
            elif option != "y":
                print("Bad option")
                quit()
            
        else:
            print(f"No updates necessary\nLocal: {localVersion}\nNew: {websiteVersion}\n")
            quit()
else: 
    print("\nNo useful response on URL\n")
    print(response)
    print("\nClosing Program")
    quit()


# Start Updater
for url in links:

    filename = url.split('=')[-1]

    if os.path.exists(filename): # Delete existing name matching files
        os.remove(filename)

    print("\nDownloading: " + filename)
	
    wget.download(url,filename)

    print ("\nDone\n")

# Register New version updated
with open("Current_Version.json","w") as localVersionFile:
    json.dump(jsonData,localVersionFile)
