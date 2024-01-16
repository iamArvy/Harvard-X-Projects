var roomSocket = null
const messagediv = document.getElementById('messages') // Replace 'myDiv' with the actual ID of your div
var currentPage = 1
function initWebSocket(chatRoomId, friend) {
    page = 1
    roomSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${chatRoomId}/`);
    roomSocket.onopen = function(e) {
        roomSocket.send(JSON.stringify({ page: page, type: 'pagenumber' }));
    };
    roomSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if(data.type === 'chat.messages'){
            getMessages(data.content, friend)
        }
        if(data.type === 'chat.message'){
            appendMessage(data, friend);
        }
        // Handle the received message on the frontend
    };// return { sendMessage };
}
function sendMessage(e) {
    e.preventDefault();
    let message = e.target.message.value;
    roomSocket.send(JSON.stringify({ message: message, type: 'sendmessage' }));
    e.target.reset();
}
function getMessages(data, friend){
    var moreButton = document.createElement('button')
    moreButton.innerHTML = ``
    var chat_messages = document.getElementById('messages')
    var data_messages = data.messages
    if (data_messages && data_messages.length > 0){
        var firstItem = data_messages[0];
        console.log(firstItem)
        data_messages.forEach(message=>{
            var listdiv = document.createElement('div');
            listdiv.className="message-list-div";
            if(friend == message.sender){
                listdiv.classList.add('friend-message')
            }else{
                listdiv.classList.add('my-message')
            }
            listdiv.id = `message-${message.chat_room}-${message.id}`
            var content = document.createElement('p');
            content.className = 'chat-content'
            content.textContent=`${message.content}`
            var time = document.createElement('small')
            time.textContent=`${message.timestamp}`
            time.className = 'message-time'
            listdiv.appendChild(content);
            listdiv.appendChild(time)
            chat_messages.prepend(listdiv)
            if (message === firstItem) {
                listdiv.scrollIntoView({ behavior: 'smooth' });
                console.log(listdiv)
            }
        })
        console.log(data)
        if(data.has_next_page){
            moreButton.addEventListener('click', function() {
                moreButton.style.display = 'none'
                currentPage++
                fetchMessages();
            });
            moreButton.textContent = 'Load More'
            chat_messages.prepend(moreButton)
        }
       
    }
}
function disconnectRoomMessagesWebSocket() {
    currentPage = 1
    if (roomSocket !== null) {
        roomSocket.close();
    }
}
function appendMessage(data, friend) {
    const chatMessages = document.getElementById('messages');
    var listdiv = document.createElement('div');
    listdiv.className="message-list-div";
    if(friend == data.sender_username){
        listdiv.classList.add('friend-message')
    }else{
        listdiv.classList.add('my-message')
    }
    listdiv.id = `message-${data.message_id}`
    var content = document.createElement('p');
    content.className = 'chat-content'
    content.textContent=`${data.message_content}`
    var time = document.createElement('small')
    time.textContent=`${data.timestamp}`
    listdiv.appendChild(content);
    listdiv.appendChild(time)
    chatMessages.appendChild(listdiv);
    listdiv.scrollIntoView({behavior: 'smooth'})
}
function fetchMessages(){
    roomSocket.send(JSON.stringify({ page: currentPage, type: 'pagenumber' }));
    console.log(currentPage)
}