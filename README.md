# YouTubeDownloader - READ IT!
YouTube Downloader App (download videos or music)

To start:
- clone repo
- click the YoutubeDownloader.exe

If youre on linux then just use wine (keep in mind that wine can be a little bit buggy with this app but it mostly works ok)
<br><br>

Fun little project I created for my friends so we can download youtube videos or youtube music.

You just insert youtube video link and then click "ENTER".
After that application shows you video thumbnail, title, how long it is and if it's age restricted.
It can download 1080p (it uses FFMPEG to do that, more explained at the bottom), 720p or 360p MP4s or 160kbps MP3s. 
You can change directory where file will be downloaded to.
Sound plays after file gets downloaded (of course you can disable it in the app if you want to). 
It even shows you progress bar when the file is downloading.

To download in 1080p quality you NEED to have FFMPEG.exe in the program directory!
Download Link: https://www.gyan.dev/ffmpeg/builds/

1080p downloading works this way:
- The video and audio is downloaded separately
- It "glues" it together and creates a new video file
- Then video and audio downloaded before is deleted

App is mostly in Polish.
