/* global webots: false */

let view = null;

export function connect(ip, port, playerDiv) {
  console.log(playerDiv)
  view = new webots.View(playerDiv, true);
  view.broadcast = false;
  view.open('ws://' + ip + ':' + port);

  return view
}

export function disconnect() {
  view.close();
  view = null;
}