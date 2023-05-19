function allowDrop(ev) {
    ev.preventDefault();
  }

function drag(ev) {
ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
ev.preventDefault();
var data = ev.dataTransfer.getData("text");
ev.target.appendChild(document.getElementById(data));
document.getElementById('position').value = ev.target.id;
document.getElementById('submitButton').disabled = false;
//window.alert(document.getElementById('position').value);
}

