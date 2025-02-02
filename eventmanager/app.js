const express = require("express");
const http = require("http");
const socketIo = require("socket.io");

const port = process.env.PORT || 4001;

const app = express();
app.get("/", (req, res) => {
    res.send({ response: "I am alive" }).status(200);
  });

const server = http.createServer(app);

const io = socketIo(server);

let interval;
function randomInt(min, max) {
	return min + Math.floor((max - min) * Math.random());
}

io.on("connection", (socket) => {
  console.log("New client connected");
  if (interval) {
    clearInterval(interval);
  }
  interval = setInterval(() => getApiAndEmit(socket), 20000);
  socket.on("disconnect", () => {
    console.log("Client disconnected");
    clearInterval(interval);
  });
});

let types = ['success', 'info', 'warning', 'error']
const getApiAndEmit = socket => {
    let _type = randomInt(0,3)
  const response = {type: types[_type],title:'Notification',message: new Date()}
  // Emitting a new message. Will be consumed by the client
  socket.emit("notification", response);
};

server.listen(port, () => console.log(`Listening on port ${port}`));