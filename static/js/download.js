// geting parmas
const urlParams = new URLSearchParams(window.location.search);
let url;
let format;
let ext;
let ERROR = 0;


// selecting down status DOM elemnts
const fileStatusDOM = document.querySelector("#fileStatus")
const fileNameDOM = document.querySelector("#fileName")
// const fileSpeedDOM = document.querySelector("#fileSpeed")
const fileSizeDOM = document.querySelector("#fileSize")

// selecting PP status DOM elemnts

const fileStatusPDOM = document.querySelector("#fileStatusP")
const fileProcessingDOM = document.querySelector("#fileProcessing")

const fileSystemTable = document.querySelector("#fileSystemTable")

const units = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
   
function convertBytes(x){

  let l = 0, n = parseInt(x, 10) || 0;

  while(n >= 1024 && ++l){
      n = n/1024;
  }
  
  return(n.toFixed(n < 10 && l > 0 ? 1 : 0) + ' ' + units[l]);
}
let socket = io();


socket.on("connect",()=>{
  socket.emit("NeedData",{})
  setInterval(()=>socket.emit("NeedData",{}),1000)
  console.log("connected")
  // if (urlParams.has("url") && urlParams.has("format") && urlParams.has("ext")) {
  //   url = urlParams.get("url")
  //   format = urlParams.get("format")
  //   ext = urlParams.get("ext")
  //   socket.emit('downloadInfo', {ERROR:ERROR,url: url,format:format,ext:ext});
  // }else{
  //   ERROR = 1
  // }
})


socket.on("prog",(prog)=>{
  let fileStatus = prog["status"]
  let fileName = prog["filename"].replace("./downloads/","")
  let fileSize = convertBytes(prog["total_bytes"])
  let fileSizeDownloaded = convertBytes(prog["downloaded_bytes"])
  fileStatusDOM.innerText = fileStatus
  fileNameDOM.innerText = fileName
  fileSizeDOM.innerText = " ("+fileSizeDownloaded+"/"+fileSize+")"
})
socket.on("pprog",(prog)=>{
  console.log(prog)
  let fileStatus = prog["status"]
  let fileProcessing = prog["postprocessor"]
  fileStatusPDOM.innerText = fileStatus
  fileProcessingDOM.innerText = fileProcessing
})


function fillingTable(files) {
  //<a href="#" class="text-decoration-none">This link has its text decoration removed</a>
  fileSystemTable.innerHTML = ""
  files.forEach(file=>{
    let trFile = document.createElement("tr")
    let thFile = document.createElement("th")
    thFile.setAttribute("scope","row")
    thFile.innerText = files.indexOf(file) + 1
    let tdFileName = document.createElement("td")
    let tdFileSize = document.createElement("td")
    let tdFileLink = document.createElement("td")
    let aFileLink = document.createElement("a")
    let fileName = file["fileName"]
    let FileSize = file["fileSizeB"]
    tdFileName.innerText = fileName
    tdFileSize.innerText = convertBytes(FileSize)
    aFileLink.href = window.location.href + "/downloads/"+fileName
    aFileLink.className = "text-decoration-none"
    aFileLink.innerText = "Download"
    tdFileLink.append(aFileLink)
    trFile.append(thFile)
    trFile.append(tdFileName)
    trFile.append(tdFileSize)
    trFile.append(tdFileLink)
    fileSystemTable.append(trFile)
  })
}
socket.on("downloadedFiles",(files)=>{
  let downloadedFiles = files["files"]
  console.log(downloadedFiles)
  fillingTable(downloadedFiles)
})
