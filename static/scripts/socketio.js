document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var socket = io.connect(`${location.protocol}//${document.domain}:${location.port}`);

    // SocketIO will send message to the server on message bucket, once the client connects with the server
    socket.on('connect', () => {
        socket.send('I am connected......')
    });

    // Server will send the messages on the message bucket and this piece of code will display all the incoming messages
    socket.on('message', data => {
        const p = document.createElement('p');
        const br = document.createElement('br');
        p.innerHTML = data;
        document.querySelector('#display-message-section').append(p)
        console.log(`Message received: ${data}`);
    });

    // Server will send the messages on the custom bucket and this piece of code will display all the incoming messages
    socket.on('custom', data => {
        console.log(`${data}`);
    });

    // Grabbing the user message from the input box and sending it to the message bucket on server side
    document.querySelector('#send_message').onclick = () => {
        socket.send(document.querySelector('#user_message').value);
        document.querySelector('#user_message').value = '';
    }
})