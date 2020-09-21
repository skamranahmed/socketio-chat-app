document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var socket = io.connect(`${location.protocol}//${document.domain}:${location.port}`);

    // Set default room
    let room = 'Python';
    joinRoom('Python')

    // SocketIO will send message to the server on message bucket, once the client connects with the server
    // socket.on('connect', () => {
        // socket.send('I am connected......')
    // });

    // Server will send the messages on the message bucket and this piece of code will display all the incoming messages
    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');
        // p.innerHTML = data;
        if (data.username){
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p)
        } else {
            printSysMsg(data.msg)
        }

        console.log(`Message received: ${data}`);
    });

    // Server will send the messages on the custom bucket and this piece of code will display all the incoming messages
    socket.on('custom', data => {
        console.log(`${data}`);
    });

    // Grabbing the user message from the input box and sending it to the message bucket on server side
    document.querySelector('#send_message').onclick = () => {
        // socket.send(document.querySelector('#user_message').value);
        socket.send(
            {
                'msg': document.querySelector('#user_message').value,
                'username':username,
                'room': room
            }
        );
        // Clear the text input field after sending the message
        document.querySelector('#user_message').value = '';
    }

    // Room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            console.log('Clicked')
            let newRoom = p.innerHTML;
            console.log(newRoom)
            if (newRoom === room){
                msg = `You are already in ${room} room`;
                console.log(msg)
                printSysMsg(msg)
            } else {
                leaveRoom(room)
                joinRoom(newRoom)
                console.log(`You left ${room} room and joined ${newRoom} room`)
                room = newRoom
            }
        }
    })

    // Leave room
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room})
    }

    // Join room
    function joinRoom(newRoom) {
        socket.emit('join', {'username': username, 'newRoom': newRoom})
        // clear the message section after user joins a new room
        document.querySelector('#display-message-section').innerHTML = ''
    }
    
    // Print system message
    function printSysMsg(msg) {
        const p = document.createElement('p')
        p.innerHTML = msg
        document.querySelector('#display-message-section').append(p)
    }



})