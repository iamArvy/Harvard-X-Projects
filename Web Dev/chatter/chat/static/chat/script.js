document.addEventListener('DOMContentLoaded', function () {
    changemainview('recent-container')
    const changepfp = document.getElementById('current-user-pfp')
    changepfp.addEventListener('click', openchanger)
    const friends = document.getElementById('friends-nav');
    friends.addEventListener('click', () => changeview('friends'));
    const changer = document.getElementById('pfp-changer')
    changer.addEventListener('change', changepfpimg)
});
function changepfpimg(){
    const pfpform = document.getElementById('pfpform')
    pfpform.submit();
}
function openchanger(){
    const changer = document.getElementById('pfp-changer')
    changer.click();
}

function changeview(view){
    disconnectRoomMessagesWebSocket()
    changemainview('main-container')
    var current = document.getElementById(view);
    var containers = document.getElementsByClassName('container');
    for (var i = 0; i < containers.length; i++){
        containers[i].style.display = 'none'
    }
    current.style.display = 'block'
}
var viewportwidth = window.innerWidth

function changefriendsview(view){
    var current = document.getElementById(view)
    var button = document.getElementById('add-page')
    var containers = document.getElementsByClassName('friends-page');
    for (var i = 0; i < containers.length; i++){
        containers[i].style.display = 'none'
    }
    current.style.display = 'block'

    if (view == 'findfriend'){
        changefriendsbutton('myfriends')
        } else if (view == 'friendlist'){
        changefriendsbutton('add-page')
        }
}
function changefriendsbutton(view){
    var button = document.getElementById(view)
    var containers = document.getElementsByClassName('friendnavs');
    for (var i = 0; i < containers.length; i++){
        containers[i].style.display = 'none'
    }
    button.style.display = 'block'
}
function changemainview(view){
    if (viewportwidth<900){
        disconnectRoomMessagesWebSocket()
        var major = document.getElementsByClassName('major-cont')
        var page = document.getElementById(view)
        for (var i = 0; i < major.length; i++){
            major[i].style.display = 'none'
        }
        page.style.display = 'block'
    }
}
function openchat(username){
    fid = username
    console.log(fid)
    fetch(`/chat/${username}/`)
    .then((response) => response.json())
    .then((data) => {
        var friendname = document.getElementById('chat_name')
        var headerimg = document.getElementById('room-header-img')
        var chat_messages = document.getElementById('messages')
        headerimg.src = `${data.friend.pfp}`
        var pfp = ``
        if (data.friend.pfp === 'none') {
            pfp = '/media/profile-pictures/default.jpeg'
        }else{
            pfp = `${data.friend.pfp}`
        }
        friendname.textContent = data.friend.username
        changeview('chatroom')
        chat_messages.innerHTML = ``
        if (document.getElementById('chatroom')){
            initWebSocket(`${data.chat_room.id}`, `${data.friend.username}`, 1)
        }
        document.getElementById('chat-form').addEventListener('submit', sendMessage);
    })
}
