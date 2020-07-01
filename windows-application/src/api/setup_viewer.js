/* global webots: false */

let view = null;

export function connect(ip, port, playerDiv) {
  console.log(playerDiv)
  view = new webots.View(playerDiv, true);
  view.broadcast = true;
  view.open('ws://' + ip + ':' + port);
}

export function disconnect() {
  view.close();
  view = null;
}