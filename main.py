from flask import Flask, render_template, url_for, request,redirect,copy_current_request_context,send_from_directory
import yt_dlp
from yt_dlp.utils import DownloadError
from flask_socketio import SocketIO, send, emit
import random
import os,threading


app = Flask(__name__)
socketio = SocketIO(app,async_mode="threading")


def main(URL, ORDER):
  if ORDER == "INFO":
    formats = []
    title = ""
    id = ""
    duration = ""
    uploader = ""
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
      try:
        info0 = ydl.extract_info(URL, download=False)
      except DownloadError as e:
        DATA = {"ERROR": str(e.msg)}
        return DATA
      title = info0['title']
      id = info0["id"]
      thumbnail = info0["thumbnail"]
      duration = info0["duration"]
      uploader = info0["uploader"]
      formats = info0["formats"]

    DATA = {
      "ERROR": 0,
      "title": title,
      "id": id,
      "channel": uploader,
      "thumbnail": thumbnail,
      "duration": round(duration / 60, 2),
      "formats": formats
    }
    return DATA


def myPHook(d):
  fileStatus = d["status"]
  if fileStatus == "started":
    with app.test_request_context('/'):
      socketio.emit("pprog",{
        "status":fileStatus,
        "postprocessor":d["postprocessor"]
      })
  elif fileStatus == "finished":
    with app.test_request_context('/'):
      socketio.emit("pprog",{
        "status":fileStatus,
        "postprocessor":d["postprocessor"]
      })
  elif fileStatus == "processing":
    with app.test_request_context('/'):
      socketio.emit("pprog",{
        "status":fileStatus,
        "postprocessor":d["postprocessor"]
      })
def myHook(d):
  fileStatus = d["status"]
  
  if fileStatus == "finished":
    with app.test_request_context('/'):
      socketio.emit("prog",{
        "downloaded_bytes": d["downloaded_bytes"],
        "status":fileStatus,
        "filename":d["filename"],
        "total_bytes":d["total_bytes"]
      })
  elif fileStatus == "error":
    with app.test_request_context('/'):
      socketio.emit("prog",{
        "status":fileStatus,
        "filename":d["filename"],
        "total_bytes":d["total_bytes"]
      })
  elif fileStatus == "downloading":
    with app.test_request_context('/'):
      socketio.emit("prog",{
        "downloaded_bytes": d["downloaded_bytes"],
        "speed":d["speed"],
        "status":fileStatus,
        "filename":d["filename"],
        "total_bytes":d["total_bytes_estimate"]
        
      })

def downloading(url, format, ext):
  baseFormats = ["b", "bv", "ba", "bv*", "ba*"]
  if baseFormats.count(format) > 0:
    print("BaseFormat choosed")
    if ext == "mp3":
      print("BaseFormat choosed >>>> mp3")
      ydlOps = {
        "quiet": True,
        'progress_hooks': [myHook],
        "postprocessor_hooks":[myPHook],
        'final_ext': 'mp3',
        "ffmpeg_location": "./ffmpegFolder",
        "outtmpl" : "./downloads/%(title)s-%(uploader)s.%(ext)s",
        "format": format,
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
      }
    else:
      print("BaseFormat choosed >>>> mp4")
      ydlOps = {
        "quiet": True,
        'progress_hooks': [myHook],
        "postprocessor_hooks":[myPHook],
        "merge_output_format": "mp4",
        'final_ext': 'mp4',
        "ffmpeg_location": "./ffmpegFolder",
        "outtmpl": "./downloads/%(title)s-%(uploader)s.%(ext)s",
        "format": format,
      }
  else:
    print("NONE BaseFormat choosed")
    if ext == "mp3":
      print("NONE BaseFormat choosed >>>> mp3")
      ydlOps = {
        "quiet": True,
        "postprocessor_hooks":[myPHook],
        'progress_hooks': [myHook],
        'final_ext': 'mp3',
        "ffmpeg_location": "./ffmpegFolder",
        "outtmpl" : "./downloads/%(title)s-%(uploader)s.%(ext)s",
        "format": format,
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
      }
    else:
      print("NONE BaseFormat choosed >>>> mp4")
      ydlOps = {
        "quiet": True,
        "postprocessor_hooks":[myPHook],
        'progress_hooks': [myHook],
        "merge_output_format": "mp4",
        'final_ext': 'mp4',
        "ffmpeg_location": "./ffmpegFolder",
        "outtmpl": "./downloads/%(title)s-%(uploader)s.%(ext)s",
        "format": format + "+ba",
      }
  with yt_dlp.YoutubeDL(ydlOps) as ydl:
    URL = [url]
    try:
      ydl.download(URL)
    except DownloadError as e:
      print(e.msg)


@app.route('/')
def index():
  return render_template("index.html")


@app.route("/video")
def video():
  url = request.args.get("url")
  if url != None:
    return render_template("video.html")
  else:
    return "<h1>Need URL</h1>"


@app.route("/download")
def download():
  url = request.args.get("url")
  format = request.args.get("format")
  ext = request.args.get("ext")
  if url != None and ext != None and format != None:
    downloadingThread= threading.Thread(target=downloading,args=(url,format,ext))
    downloadingThread.start()
    return redirect(url_for("fS"))
  else:
    return "<h1>Missing Info</h1>"
  # # downloading("https://www.youtube.com/watch?v=TTklJ3GQxb8&t=160s","2","MP4")
  # downloadingThread= threading.Thread(target=downloading,args=(url,format,ext))
  # downloadingThread.start()

@app.route("/fileSystem")
def fS():
   return render_template("download.html")

@app.route('/fileSystem/downloads/<path:filename>', methods=['GET', 'POST'])
def downloads(filename):
    uploads = os.getcwd() + "/downloads"
    return send_from_directory(directory=uploads, path=filename)
@app.route("/test")
def test():
  ydlOps = {
    "merge_output_format": "mp4",
    'final_ext': 'mp3',
    "ffmpeg_location": "./ffmpegFolder",
    "outtmpl": "./downloads/%(title)s-%(uploader)s.%(ext)s",
    "format": "398+ba"
  }

  with yt_dlp.YoutubeDL(ydlOps) as ydl:
    ydl.download(["https://www.youtube.com/watch?v=X4KNqjF34E4"])
    return "ydl"


@socketio.on('url')
def handle_message(data):
  url = data['url']
  if url != 0:
    DATA = main(url, "INFO")
    # send(DATA)
    emit("DATA", DATA)
  else:
    print("NO URL")


# @socketio.on("downloadInfo")
# def handle_downloadInfo(data):
#   ERROR = data["ERROR"]
#   if ERROR == 0:
#     url = data["url"]
#     format = data["format"]
#     ext = data["ext"]
#     downloading(url, format, ext)
#   else:
#     print("missing Info")
@socketio.on("NeedData")
def handle_fileSysytem(d):
  path = os.getcwd() + "/downloads"

  downloadedFilesList = os.listdir(path)
  downloadedFiles = []
  for file in downloadedFilesList:
    fileSize = os.stat(path+"/"+file)
    downloadedFilesDict = {"fileName":file,"fileSizeB":fileSize.st_size}
    downloadedFiles.append(downloadedFilesDict)
  emit("downloadedFiles",{"files":downloadedFiles})

socketio.run(app, host='0.0.0.0', port=81, debug=False)
