var button = document.querySelector("button"),
  output = document.querySelector("#output"),
  textarea = document.querySelector("textarea"),
  fpimage = document.getElementById("fpImg"),
  fingerAnim = document.getElementById("finger-anim"),
  wsUri = "ws://127.0.0.1:8080/",
  websocket = new WebSocket(wsUri);

button.addEventListener("click", onClickButton);

websocket.onopen = function(e) {
  writeToScreen("CONNECTED");
  doSend("WebSocket rocks");
};

websocket.onclose = function(e) {
  writeToScreen("DISCONNECTED");
};

websocket.onmessage = function(e) {
  //removeFingerAnim();
  try {
    let obj = JSON.parse(e.data);
    console.log(obj);

    if (obj.hasOwnProperty("Imagedata")) {
      removeFingerAnim();
      getImageData(obj, i => {
        addImagePlaceholder(i.Imagedata);
      });
    } else if (obj.hasOwnProperty("ReaderList")) {
      bindDropDownList(obj.ReaderList);
    } else if (obj.hasOwnProperty("Type")) {
      writeToScreen("<span class=error>ERROR:</span> " + obj.Message);
    } else {
      console.log(obj);
    }
  } catch (ex) {
    writeToScreen("<span>RESPONSE: " + e.data + "</span>");
  }

  //websocket.close();
};

websocket.onerror = function(e) {
  console.log(e);
  writeToScreen("<span class=error>ERROR:</span> " + e.data);
  websocket.close();
};

function doSend(message) {
  writeToScreen("SENT: " + message);
  websocket.send(message);
}

function writeToScreen(message) {
//   output.insertAdjacentHTML("afterbegin", "<p>" + message + "</p>");
}

function onClickButton() {
  var text = textarea.value;

  text && doSend(text);
  textarea.value = "";
  textarea.focus();
}

function removeFingerAnim() {
  document.getElementById("finger-anim").remove();
}
function addImagePlaceholder(thumb) {
  
  var imgDiv = document.createElement("div");
  imgDiv.className = "fingerprint-image";
  imgDiv.id = "finger-container-tanvir";
  document.getElementById("finger-image").appendChild(imgDiv);
  var img = document.createElement("img");
  img.id = "fpImg";
  img.height = "200";
  img.width = "200";
  img.src = thumb;
//   img.border = "solid";
//   img.border.width = "3px";
//   img.border.color = "black";
  document.getElementById("finger-container-tanvir").appendChild(img);
  down.innerHTML = "Image Element Added.";
}

function getImageData(obj, callback) {
  let i = obj;
  callback(i);
}
