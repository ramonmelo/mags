
var io = require('socket.io')();

io.on('connection', function(socket) {
    console.log('user connected');

    socket.on('disconnect', function() {
        console.log('user disconnected');
    });

    socket.on('chat message', function(msg, fn) {
        console.log('message: ' + msg);
        io.emit('chat message', msg);

        fn('the fn function', 123);

        socket.emit('private', {
            name: 'my name',
            msg: msg
        });
    });
});

exports.io = io
