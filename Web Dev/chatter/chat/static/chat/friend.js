document.getElementById('search-form').addEventListener('submit', find_friends);
if(document.getElementById('friends')){
    get_friends()
}
function requester(id, type){
    fetch(`/friends/${type}/${id}`)
    .then((response) => response.json())
    .then((data)=>{
        console.log(data)
    })
    get_friends()
}

function get_friends(){
    var friendlist = document.getElementById('friendlist')
    var requestlist = document.getElementById('requestlist')
    friendlist.innerHTML = ''
    requestlist.innerHTML = ''
    fetch(`/friends`)
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
        if (data.friends.length == 0){
            friendlist.innerHTML = `<p class="empty-page">You do not have any Friends</p>`
        }
        else{
            var friends = data.friends
            friends.forEach(element=>{
                var listdiv = document.createElement('div');
                listdiv.className = "friend-list-item"
                var listpfp = document.createElement('div');
                var listcontent = document.createElement('div');
                var username = element.username
                var id = element.id
                var pfp = ``
                if (element.pfp === 'none') {
                    pfp = '/media/profile-pictures/default.jpeg'
                }else{
                    pfp = `${element.pfp}`
                }
                listpfp.innerHTML = `
                <div class="img-pfp">
                        <div class="pfp-img">
                            <img src="${pfp}" alt="no img" class="pfp" id="header-img-${element.id}">
                        </div>
                    </div>`
                listpfp.classname = 'list-pfp'
                listdiv.className="friend-list-div";
                listdiv.id = `friend-list-${id}`
                listcontent.innerHTML = `
                <div class='room-user-cont'>
                    <span class='room-user'>${username}</span>
                    <div class='operator-buttons'>
                        <button onclick="openchat('${username}')" class="cursor nobgbtn"><i class="fa-brands fa-rocketchat"></i></button>
                        <button onclick="requester(${id}, 'reject')" class="cursor nobgbtn"><i class="fa-solid fa-user-xmark"></i></button>
                    </div>
                </div>
                `
                listcontent.className = 'list-item-content'
                listcontent.classList.add('flex')
                listdiv.appendChild(listpfp);
                listdiv.appendChild(listcontent)
                friendlist.appendChild(listdiv)
            })
            var requests = data.requests
            // console.log(requests)
            if(requests.length == 0){
                requestlist.innerHTML = `<p class="empty-page">You do not have requests</p>`
            }else{
                console.log('hi')
            requests.forEach(element=>{
                console.log(element)
                var listdiv = document.createElement('div');
                listdiv.className = "friend-list-item"
                var listpfp = document.createElement('div');
                var listcontent = document.createElement('div');
                var username = element.requester.username
                var id = element.requester.id
                var pfp = ``
                if (element.requester.pfp === 'none') {
                    pfp = '/media/profile-pictures/default.jpeg'
                }else{
                    pfp = `${element.requester.pfp}`
                }
                listpfp.innerHTML = `
                <div class="img-pfp">
                        <div class="pfp-img">
                            <img src="${pfp}" alt="no img" class="pfp" id="header-img-${element.id}">
                        </div>
                    </div>`
                listpfp.classname = 'list-pfp'
                listdiv.className="friend-list-div";
                listdiv.id = `friend-list-${id}`
                listcontent.innerHTML = `
                <div class='room-user-cont'>
                    <span class='room-user'>${username}</span>
                    <div class='operator-buttons'>
                        <button onclick="requester(${id}, 'accept')" class="cursor nobgbtn"><i class="fa-solid fa-check"></i></button>
                        <button onclick="requester(${id}, 'reject')" class="cursor nobgbtn"><i class="fa-solid fa-xmark"></i></button>
                    </div>
                </div>
                `
                listcontent.className = 'list-item-content'
                listcontent.classList.add('flex')
                listdiv.appendChild(listpfp);
                listdiv.appendChild(listcontent)
                requestlist.appendChild(listdiv)
            })
        }
        }
    })
}
function find_friends(e){
    e.preventDefault();
    let key = e.target.key.value;
    fetch(`find/${key}`,{
        method:'POST',
    })
    .then((response) => response.json())
    .then((data)=>{
        console.log(data)
        var searchlist = document.getElementById('searchlist')
        if (data.users.length == 0){
            console.log(data)
            searchlist.innerHTML = `<p class='empty-page'>There is no user with this name</p>`
        }
        else{
            var searchresult = data.users
            searchresult.forEach(element=>{
                console.log(element)
                var listdiv = document.createElement('div');
                listdiv.className = "friend-list-item"
                var listpfp = document.createElement('div');
                var listcontent = document.createElement('div');
                var pfp = ''
                var username = element.username
                var btncont = document.createElement('div')
                var id = element.id
                if(element.is_friend){
                        btncont.innerHTML= `<button onclick="openchat('${username}')" class="cursor nobgbtn"><i class="fa-brands fa-rocketchat"></i></button>`
                    }else if(element.has_sent_request){
                        btncont.innerHTML= `<button onclick="requester(${id}, 'accept')" class="cursor nobgbtn"><i class="fa-solid fa-check"></i></button>
                        <button onclick="requester(${id}, 'reject')" class="cursor nobgbtn"><i class="fa-solid fa-xmark"></i></button>`
                    }else if(element.request_sent){
                        btncont.innerHTML= `<button onclick="requester(${id}, 'reject')" class="cursor nobgbtn"><i class="fa-solid fa-xmark"></i></button>`
                    }else{
                        btncont.innerHTML= `<button onclick="requester(${id}, 'add')" class="cursor nobgbtn"><i class="fa-solid fa-user-plus"></i></button>`
                    }
                var pfp = ``
                if (element.pfp === 'none') {
                    pfp = '/media/profile-pictures/default.jpeg'
                }else{
                    pfp = `${element.pfp}`
                }
                listpfp.innerHTML = `
                <div class="img-pfp">
                        <div class="pfp-img">
                            <img src="${pfp}" alt="no img" class="pfp" id="header-img-${element.id}">
                        </div>
                    </div>`
                listpfp.classname = 'list-pfp'
                listdiv.className="friend-list-div";
                listdiv.id = `friend-list-${id}`
                listcontent.innerHTML = `
                <div class='room-user-cont'>
                    <span class='room-user'>${username}</span>
                    <div class='operator-buttons'>
                        ${btncont.innerHTML}
                    </div>
                </div>
                `
                listcontent.className = 'list-item-content'
                listcontent.classList.add('flex')
                listdiv.appendChild(listpfp);
                listdiv.appendChild(listcontent)
                searchlist.innerHTML = ``
                searchlist.appendChild(listdiv)
            })
        }
    })
    e.target.reset();
}
