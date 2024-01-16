let chatListSocket = new WebSocket(`ws://${window.location.host}/ws/chat_list/`);

chatListSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);

    if (data.type === 'chat.list_update') {
        updateChatList(data.chat_list);
    }
};

function updateChatList(chatRooms) {
    chatRooms.sort((a, b) => new Date(a.data.lastmessage.timestamp) - new Date(b.data.lastmessage.timestamp));
    chatRooms.reverse();
    const chatListDiv = document.getElementById('chat-list');
    chatListDiv.innerHTML = '';

    for (let chatRoom of chatRooms) {
        console.log(chatRoom)
        const chatRoomElement = document.createElement('div');
        const hr = document.createElement('hr')
        chatRoomElement.className = 'list-item'
        chatRoomElement.classList.add('cursor')
        chatRoomElement.addEventListener('click', () => openchat(`${chatRoom.friend.username}`));
        chatRoomElement.id = `chat-room-${chatRoom.data.id}`
        var roommessage = document.createElement('div')
        var pfp = ``
        if (chatRoom.friend.pfp === 'none') {
            pfp = '/media/profile-pictures/default.jpeg'
        }else{
            pfp = `${chatRoom.friend.pfp}`
        }
        if(chatRoom.unreadcount != 'none'){
            var unreadcount = chatRoom.unreadcount
            roommessage.innerHTML = `
                <strong class='flex'>${chatRoom.data.lastmessage.content}</strong>
                <strong>${unreadcount}</strong>
            `
        }else{
            roommessage.innerHTML = `
            <span class='flex'>${chatRoom.data.lastmessage.content}</span>
        `        
        }
        chatRoomElement.innerHTML = `
                <div class='list-pfp'>
                    <div class="img-pfp">
                        <div class="pfp-img">
                            <img src="${pfp}" alt="no img" class="pfp" id="header-img-${chatRoom.data.id}">
                        </div>
                    </div>
                </div>
                <div class='list-item-content flex'>
                    <div class='room-user-cont'>
                        <span class='room-user'>${chatRoom.friend.username}</span>
                        <span class='message-date'>${chatRoom.data.lastmessage.timestamp}<span>
                    </div>
                    <div class='room-message'>
                        ${roommessage.innerHTML}
                    </div>
                </div>
        `;
        chatListDiv.appendChild(chatRoomElement);
        chatListDiv.appendChild(hr);
    }
}