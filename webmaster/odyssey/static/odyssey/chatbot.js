function createBubble(message, user){
    var d = new Date();
    var chatLog = document.getElementById("chat-body");
    var current_time = d.toLocaleTimeString();
    if(user == "You")
      {chatLog.innerHTML += "<p class = 'message-bubble user-message'><strong>"+user+"</strong> " + current_time + "<br>" + message + "</p>";}
    else
      {chatLog.innerHTML += "<p class = 'message-bubble bot-message'><strong>"+user+"</strong> " + current_time + "<br>" + message + "</p>";}
    chatLog.scrollTop = chatLog.scrollHeight;
    notBusy();
}

function pretendingToBeBusy()
{
    var target = document.getElementById("chat-header-status");
    target.innerHTML = "typing...";
}

function notBusy()
{
    var target = document.getElementById("chat-header-status");
    target.innerHTML = "Chat with us";
}

function autoFill(m) {
  document.getElementById("chatMessage").value = m;
}

//chatbot function
document.addEventListener("DOMContentLoaded", function() {
    // Get the chat log and message input elements
    var messageInput = document.getElementById("chatMessage");
    
    // Add an event listener to the message input element
    messageInput.addEventListener("keydown", function(event) {
        // Check if the user has pressed the enter key
        if (event.keyCode === 13) {
        // Get the user's message
        var messageInput = document.getElementById("chatMessage");
        var message = messageInput.value;
        createBubble(message, "You")
        
        // Send the user's message to the server using an AJAX request
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/chatbot/", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
            // Get the bot's response
            var response = JSON.parse(xhr.responseText).message;
            
            // Display the bot's response in the chat log
            pretendingToBeBusy();
            setTimeout(function () {
                createBubble(response, "O-Bot");
              }, 2500);
            // Clear the message input field
            messageInput.value = "";
            }
        };
        xhr.send(JSON.stringify({ 'message': message }));
        }
    });
    });


// Make the DIV element draggable:
dragElement(document.getElementById("chat-container"));

function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById("chat-header")) {
    // if present, the header is where you move the DIV from:
    document.getElementById("chat-header").onmousedown = dragMouseDown;
  } else {
    // otherwise, move the DIV from anywhere inside the DIV:
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }
}