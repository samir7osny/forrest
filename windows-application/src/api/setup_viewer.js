/* global webots: false */

let view = null;

export function connect(ip, port) {
  console.log("Hello")
  let playerDiv = document.getElementById('playerDiv');
  console.log(playerDiv)
  view = new webots.View(playerDiv, true);
  view.broadcast = true;
  view.open('ws://' + ip + ':' + port);
}

// export function disconnect() {
//   view.close();
//   view = null;
//   let playerDiv = document.getElementById('playerDiv');
//   playerDiv.innerHTML = null;
//   connectButton.value = 'Connect';
//   connectButton.onclick = connect;
//   ipInput.disabled = false;
//   portInput.disabled = false;
// }