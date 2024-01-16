from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import User, Message, ChatRoom, Request

# Create your views here.

@login_required
def changepfp(request):
    user = request.user
    img = request.FILES.get('image')
    if img:
        user.pfp.delete(save=False)
        user.pfp = img
        user.save()
        print(user.serialize())
        return JsonResponse({'message': 'Successful'})
    else:
        return JsonResponse({'message': 'none'})
@login_required
def friends(request):
    user = request.user
    friendlist = user.friends.all().order_by('username')
    requests = Request.objects.filter(requestee=user)
    return JsonResponse({
        'friends': [friend.serialize() for friend in friendlist],
        'requests': [req.serialize() for req in requests]
    })

@login_required
def requester(request, type, id):
    user = request.user
    friend = get_object_or_404(User, id=id)
    if friend in user.friends.all():
        return JsonResponse({'message': 'added'})
    else:
        if type == 'add':
            message = add_friend(request, friend)
            return message
        elif type == 'accept':
            message = accept_request(request, friend)
            return message
        elif type == 'reject':
            delete_request(request, friend)
        return JsonResponse({'message': 'hi'})
    
@login_required
def accept_request(request, friend):
    user = request.user
    friend_request = get_object_or_404(Request, requester=friend, requestee=user)
    user.friends.add(friend)
    user.save()
    friend_request.delete()
    return JsonResponse({'message': 'Successfully Accepted'})

@login_required
def delete_request(request, friend_request):
    user = request.user
    new_request = friend_request
    if user is (new_request.requestee or new_request.requester):
        new_request.delete()
        message='Successfully Rejected'
    else:
        message = 'Unauthorized'
    return JsonResponse({'message': message})

@login_required
def add_friend(request, friend):
    user = request.user
    try:
        is_request = Request.objects.filter(requestee=friend, requester=user)
        if is_request.exists():
            pass
        else:
            is_requested = Request.objects.filter(requestee=user, requester=friend)
            if is_requested.exists():
                request=get_object_or_404(Request, requestee=user, requester=friend)
                accept_request(user, request)
            else:
                new_request = Request.objects.create(requestee=friend, requester=user)
                new_request.save
        message = 'success'
    except Exception as e:
        message = 'error'
    return JsonResponse({'message':message})

@login_required
@csrf_exempt
def findfriends(request, key):
    currentuser = request.user
    users = User.objects.filter(username=key).exclude(username=currentuser)
    user_request_list = Request.objects.filter(requestee=currentuser).exists()
    user_sent_request_list = Request.objects.filter(requester=currentuser).exists()
    for user in users:
        if currentuser in user.friends.all():
            user.is_friend = True
        elif user_request_list:
            user.has_sent_request = True
        elif user_sent_request_list:
            user.request_sent = True
    if users is None:
        return JsonResponse({'message': 'none'})
    else:
        return JsonResponse({'users': [newuser.serialize() for newuser in users]})


@login_required
def chat_room_view(request, key):
    current_user = request.user
    friend = get_object_or_404(User, username=key)
    chat_room = ChatRoom.objects.get_chat_room(current_user, friend)

    if not chat_room:
        chat_room = ChatRoom.objects.create()
        chat_room.users.add(current_user, friend)

    messages = Message.objects.filter(chat_room=chat_room)
    # unreadmessages = 
    for message in messages:
        message.read_by.add(current_user)
    return JsonResponse(
        {'friend':friend.serialize(),
         'chat_room': chat_room.serialize(),
         })

@login_required
def chat_rooms_list(request):
    return render(request, 'chat/chat_rooms_list.html')

@login_required
def index(request):
    print(request.user.serialize())
    return render(request, 'chat/index.html')

@csrf_exempt
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chat/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chat/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chat/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "chat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chat/register.html")