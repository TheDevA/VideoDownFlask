// geting parmas
const urlParams = new URLSearchParams(window.location.search);
let url;
// selecting loading , working and invalid DOM
const loadingState = document.querySelector(".loadingState")
const workingState = document.querySelector(".workingState")
const invalidState = document.querySelector(".invalidState")
// selecting video information DOM elements
const videoTitle = document.querySelector("#videoTitle")
const videoUploader = document.querySelector("#videoUploader")
const videoDuration = document.querySelector("#videoDuration")
const videoThumbnail = document.querySelector("#thumbnail")
const videoFormatsDOM = document.querySelector("#videoFormatsDOM")

// func for filling video information
function fillingVideoInfo(data) {
  let title = data["title"]
  let uploader = data["channel"]
  let duration = data["duration"] + " min"
  let thumbnail = data["thumbnail"]
  videoTitle.innerText = title
  videoUploader.innerText = uploader
  videoDuration.innerText = duration
  videoThumbnail.src = thumbnail
}
//func for filling video formats
function fillingFormats(data) {
  let formats = data["formats"]
  formats.forEach(format =>{
    // console.log(format)
    // let formatQual = format.split("-")[1].trim()
    // let formatID = format.split("-")[0].trim()
    let formatQual = format["format_note"]
    let formatID = format["format_id"]
    let formatExt = format["ext"]
    let formatVbr = format["vbr"]
    let formatAbr = format["abr"]
    // console.log("Qual: "+formatQual)
    // console.log("ID: "+formatID)
    if ( format["vcodec"] != "none") {
      let formatInput = document.createElement("input")
      formatInput.type = "radio"
      formatInput.className = "btn-check"
      formatInput.name = "btnradio"
      formatInput.id = formatID
      formatInput.autocomplete = "off"
      let formatLabel = document.createElement("label")
      formatLabel.className = "formatBtn btn btn-outline-primary m-1"
      formatLabel.setAttribute("for",formatID)
      format["acodec"] != "none" ? formatLabel.innerText = formatQual + " (" +formatExt + "/WithAudio)" : formatLabel.innerText = formatQual + " (" +formatExt + "/"+ Math.round(Number(formatVbr)) + "K)"
      videoFormatsDOM.appendChild(formatInput)
      videoFormatsDOM.appendChild(formatLabel)
    }
    
  })
}
// handling downloading
const downButton = document.querySelector("#downButton")
const extMP4Button = document.querySelector("#btnMP4")
function downButtonClicked() {
  let formatChoice = []
  for (const child of videoFormatsDOM.children) {
    if (child.tagName == "INPUT") {
      child.checked ? formatChoice.push(child.id): ""
    }
  }
  if (extMP4Button.checked) {
    formatChoice.push("mp4")
  }else{
    formatChoice.push("mp3")
  }
  console.log(formatChoice)
  window.location.href = "/download?url="+ url+"&format="+formatChoice[0]+"&ext="+formatChoice[1]
}

downButton.addEventListener("click",downButtonClicked)

let DATA
// Reciving information & socket setup
let socket = io();
if (urlParams.has("url")) {
  url = urlParams.get("url")
}else{
  url = 0
}

socket.on('connect', function() {
    socket.emit('url', {url: url});
    
});

// socket.on("message",(data)=> console.log(data))
socket.on("DATA",(data)=>{
  let ERROR = data["ERROR"]
  if (ERROR == 0) {
    // console.log(data)
    DATA = data
    fillingVideoInfo(data)
    fillingFormats(data)
    loadingState.hidden = true
    workingState.hidden = false
  }else{
    console.log("ERROR: "+ERROR) 
    loadingState.hidden = true
    invalidState.hidden = false
  }
})

// manipulating DOM with information

// const videoTitle = document.querySelector("#videoTitle")


// function usingData(data) {
//   let title = data["title"]
//   videoTitle.innerText = title
// }


