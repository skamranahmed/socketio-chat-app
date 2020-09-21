document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var socket = io.connect(`${location.protocol}//${document.domain}:${location.port}`);

    // Set default room
    let room = 'Python';

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
        span_username.innerHTML = data.username;
        span_timestamp.innerHTML = data.time_stamp;
        p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
        document.querySelector('#display-message-section').append(p)
        console.log(`Message received: ${data}`);
    });

    // Server will send the messages on the custom bucket and this piece of code will display all the incoming messages
    socket.on('custom', data => {
        console.log(`${data}`);
    });

    // Grabbing the user message from the input box and sending it to the message bucket on server side
    document.querySelector('#send_message').onclick = () => {
        // socket.send(document.querySelector('#user_message').value);
        socket.send({'msg': document.querySelector('#user_message').value,
            'username':username, 'room': room});

        document.querySelector('#user_message').value = '';
    }
})