
var socket = io();

$('form').submit(function(){
    socket.emit('chat message', $('#m').val(), function(data, d2) {
      console.log("the data");
    });
    $('#m').val('');
    return false;
});

socket.on('chat message', function(msg){
    $('#messages').append($('<li>').text(msg));
});

socket.on('private', function(msg) {
    console.log(msg);
});
