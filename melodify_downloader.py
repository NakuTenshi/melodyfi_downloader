"""
    hello
    if you reading this, that means i gived you this source code
    it's not big deal , it just downlaod song from melodify
    just give playlist/artist's profile link from pwa.melodify.app
    
    you can run this code by this command ( replace the 'url' to something else ):
        python melodify_downloader.py -u url

    this app have downlaod limit, if you want to downlaod more or less just give -l flag to something else
    just remeber the 'self.limit_value' is in MB
    like:
        python melodify_downloader.py -u url -l 8192

    

"""

import os
import sys
import time
import json
import ctypes
import requests
import argparse
from data import *
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

if not os.path.exists("./songs"):
    os.mkdir("./songs")
    os.mkdir("./songs/playlists")
    os.mkdir("./songs/artists")

parser = argparse.ArgumentParser(description="a Tool for downloading tracks from paylist/artist profile from melodify")

parser.add_argument("-u", help="url for profile/paylist (required)", required=True)
parser.add_argument("-l", help="limit value (default = 5120)", default=5120, type=int)
parser.add_argument("-q", help="set quality for songs that are gonna to be downloaded (high(default)/medium/low)", choices=["high","medium","low"], default="high")

args = parser.parse_args()
url = args.u
limit_value = args.l
allow_2_downlaod = False # by defualt is False
process_icon_index = 0
if args.q == "high":
    quality_index = 0 
elif args.q == "medium":
    quality_index = 1
else: # low
    quality_index = -1

class Check_System:
    def __init__(self):
        self.csv_file = "./history.csv"
        self.limit_value = limit_value       

        # create or load csv file
        if not os.path.exists(self.csv_file): 
            self.df = pd.DataFrame(columns=["date", "downloaded"])

            self.df.to_csv(self.csv_file, index=False)
        else:
            self.df = pd.read_csv(self.csv_file)

        self.todays_date = str(datetime.now().date())

        if not len(self.df[self.df['date'] == self.todays_date]):
            new_data = pd.DataFrame({
                "date": [self.todays_date],
                "downloaded": [0]
            })

            new_df = pd.concat([self.df, new_data])
            self.df = new_df
            self.df.to_csv(self.csv_file, index=False)

    def update_limit(self, value):
        index = self.df[self.df['date'] == self.todays_date].index[0]
        downloaded_value = self.df.loc[index].get("downloaded")

        self.df.loc[index, 'downloaded'] = downloaded_value + value        
        self.df.to_csv(self.csv_file, index=False)

    def check_limit(self): # True --> allow to download && False --> not allowed to download
        downloaded_value = self.df.iloc[-1].get("downloaded")
        return True if downloaded_value <= self.limit_value else False



def enable_ansi():
    if os.name == "nt":
        kernel = ctypes.windll.kernel32
        handle = kernel.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11
        mode = ctypes.c_ulong()
        kernel.GetConsoleMode(handle, ctypes.byref(mode))
        kernel.SetConsoleMode(handle, mode.value | 0x0004)  # ENABLE_VIRTUAL_TERMINAL_PROCESSING

def clear_lline():
    sys.stdout.write("\033[F")  # move cursor up
    sys.stdout.write("\033[K")  # clear line
    sys.stdout.flush()

def show_download_process(percent, song_name):
    global process_icon_index

    process_icon = ["/", "-", "\\", "|"]
    icon = process_icon[process_icon_index]
    clear_lline()
    print(f'[{icon}] "{song_name}": {percent}% downloaded')

    process_icon_index += 1
    process_icon_index = 0 if process_icon_index == 4 else process_icon_index 

def download_songs(url):
    global allow_2_downlaod
    
    melodify_endpoints = {
        "get_info" : "",
        "get_tracks": ""
    }

    if url.startswith("https://pwa.melodify.app/artist-profile/"): # downlaod from profile
        melodify_endpoints["get_info"] = "https://melodify.pw/api/pwa/v9/getArtistData?artist_id={}"
        melodify_endpoints["get_tracks"] = "https://melodify.pw/api/pwa/v9/getArtistTracks"
        download_from = "profile"
        SONG_MAIN_FOLDER_PATH = "./songs/artists/"

    elif url.startswith("https://pwa.melodify.app/playlist-songs/"): # downlaod from playlist
        melodify_endpoints["get_info"] = "https://melodify.pw/api/pwa/v9/getCollectionData?collection_id={}"
        melodify_endpoints["get_tracks"] = "https://melodify.pw/api/pwa/v9/getCollectionTracks"
        download_from = "playlist"
        SONG_MAIN_FOLDER_PATH = "./songs/playlists/"

    else:
        print("[ERROR] the url is not valid")
        exit()
        
    id = url.split("/")[-1]
    downloaded_song_count = 0
    is_ended = False
    get_tracks_request_data = {"collection_id":f"{id}","offset":0,"sort":"melodify"} if download_from == "playlist" else {"artist_id":f"{id}","offset":0,"sort":"new"} 
    
    try:
        get_info_request = requests.get(melodify_endpoints["get_info"].format(id), headers=get_headers)
        name = str(get_info_request.json()["result"]["collection"]["title"]).replace(" ", "_") if download_from == "playlist" else str(get_info_request.json()["result"]["artist"]["name"]).replace(" ", "_")
        songs_count = get_info_request.json()["result"]["collection"]["tracks_count"] if download_from == "playlist" else get_info_request.json()["result"]["artist"]["tracks_count"]
    except KeyError:
        print("[ERROR] you need to active the account for your device !!")
        exit()

    song_folder = os.path.join(SONG_MAIN_FOLDER_PATH, name)
    if not os.path.exists(song_folder):
        os.mkdir(song_folder)

    print(f"[INFO] downloading musics from {name}'s {download_from}\n")
    while (not is_ended and get_info_request.status_code == 200):
        tracks_request = requests.post(url=melodify_endpoints["get_tracks"] ,data=json.dumps(get_tracks_request_data), headers=post_headers)

        if tracks_request.status_code == 200:
            try:
                tracks_data = tracks_request.json()
                tracks = tracks_data["result"]["tracks"]# [:1]

                for track in tracks:
                    if check_obf.check_limit() or allow_2_downlaod:
                        song_name = track["title"].replace("/"," ").replace("|" , "").replace("\\", "").replace("?", "").replace("'"," ").replace('"', " ").replace("(","").replace(")","").replace(":", " ").replace(";", " ").replace("*", "")
                        song_path = str(os.path.join(song_folder, song_name)) + ".mp3"
                        downloaded_song_count += 1

                        if not os.path.exists(song_path):
                            timestamp = str(time.time()).split(".")[0]
                            try:
                                get_download_link = str(track["mp3s"][quality_index]["name"]) + f"?type=download&timestamp={timestamp}"
                            except:
                                get_download_link = str(track["mp3s"][0]["name"]) + f"?type=download&timestamp={timestamp}"

                            response = requests.get(get_download_link, headers=get_headers, allow_redirects=False)
                            if response.status_code == 307:
                                download_link = BeautifulSoup(response.text, "lxml").find('a').get("href")
                                download_request = requests.get(download_link, headers=get_headers, stream=False)
                        
                                if download_request.status_code == 200:
                                    content_length = round((int(download_request.headers.get("Content-Length")) / 1024) / 1024 ) # byte --> kilo byte --> mega byte
                                    check_obf.update_limit(content_length)
                                    downloaded_length = 0 
                                    process_icon_index = 0

                                    with open(song_path, "wb") as f:
                                        for chunk in download_request.iter_content(chunk_size=1024):
                                            if chunk:
                                                downloaded_length += (int(len(chunk)) / 1024 )/ 1024
                                                downloaded_percent = round((downloaded_length / content_length) * 100)
                                                show_download_process(downloaded_percent, song_name)
                                                f.write(chunk)
                                    clear_lline()
                                    print(f'[{downloaded_song_count}/{songs_count}] "{song_name}": fully downloaded')
                    else:
                        print("[WARNING] you reached into download limit")
                        print(f"if you want to download more that limited value press Y")
                        print(f"but remeber it can be cuz of banning your account")
                        while True:
                            user_input = input("Y or N ? ")
                            if user_input.lower() == "y":
                                allow_2_downlaod = True
                                break
                            elif user_input.lower() == "n":
                                print("bye")
                                exit()
                            else:
                                continue

                if not tracks_data["result"]["end"]:
                    get_tracks_request_data["offset"] = downloaded_song_count
                else:
                    is_ended = True
                    clear_lline()
                    print(f"[INFO] songs saved at {song_folder}")


            except Exception as e:
                print(f"[ERROR] there was an error in response: {e}")
                exit()

if __name__ == "__main__":
    enable_ansi()
    try:
        check_obf = Check_System()
        if check_obf.check_limit():
            download_songs(url)
        else:
            print(f"[WARNING] you downloaded more that {check_obf.limit_value}MB")
            print(f"if you want to download more that limited value press Y")
            print(f"but remeber it can be cuz of banning your account")

            while True:
                user_input = input("Y or N ? ")
                
                if user_input.lower() == "y":
                    allow_2_downlaod = True
                    print("\n")
                    download_songs(url)
                    break
                elif user_input.lower() == "n":
                    print("bye")
                    exit()
                else:
                    continue
    except KeyboardInterrupt:
        print("\nbye bye:)")
        exit()
