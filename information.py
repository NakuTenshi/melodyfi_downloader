MUSIC_PATH = "./songs"
PLAYLIST_PATH_MAIN = "./songs/playlists/"
ARTHIST_PATH_MAIN = "./songs/arthist/"

Authorization = ""
Device_Id = ""
Device_Name = ""
Device_Token = ""
User_Id = ""

post_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Authorization": Authorization,
    "App-Version": "9.1.0",
    "Pwa-Version": "9.3.9",
    "Device-Id": Device_Id,
    "Device-Name": Device_Name,
    "Device": "pwa",
    "Device-Token": Device_Token,
    "User-Id": User_Id,
    "User-Device-Info": "screen_w:1360-screen_w:616  PWA_REACT",
    "User-Signature": "MA==",
    "Platform": "Linux",
    "Content-Length": "53",
    "Origin": "https://pwa.melodify.app",
    "Referer": "https://pwa.melodify.app/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Te": "trailers",
    "Connection": "keep-alive"
}

get_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Access-Control-Allow-Origin": "*",
    "Authorization": Authorization,
    "App-Version": "9.1.0",
    "Pwa-Version": "9.3.9",
    "Device-Id": Device_Id,
    "Device-Name": Device_Name,
    "Device": "pwa",
    "Device-Token": Device_Token,
    "User-Id": User_Id,
    "User-Device-Info": "screen_w:1360-screen_w:616  PWA_REACT",
    "User-Signature": "MA==",
    "Platform": "Linux",
    "Origin": "https://pwa.melodify.app",
    "Referer": "https://pwa.melodify.app/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Te": "trailers",
    "Connection": "keep-alive"
}

