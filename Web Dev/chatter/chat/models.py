from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.serializers import serialize

# Create your models here.
class User(AbstractUser):
    pfp = models.ImageField(upload_to='profile-pictures', blank=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    bio = models.TextField(blank=True, null=True)
    is_friend = models.BooleanField(default=False)
    has_sent_request = models.BooleanField(default=False)
    request_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"
    
    def serialize(self):
        if self.pfp:
            pfpurl = self.pfp.url
        else:
            pfpurl = 'none'
        return {
            "id": self.id,
            "username": self.username,
            'pfp': pfpurl,
            'is_friend': self.is_friend,
            'has_sent_request':self.has_sent_request,
            'request_sent': self.request_sent
        }

class ChatRoomManager(models.Manager):
    def get_chat_room(self, user1, user2):
        # Retrieve a chat room regardless of the order of users
        return self.filter(users=user1).filter(users=user2).first() or \
               self.filter(users=user2).filter(users=user1).first()

class ChatRoom(models.Model):
    users = models.ManyToManyField(User)
    objects = ChatRoomManager()

    @property
    def group_name(self):
        return f"chat_room_{self.id}"

    def serialize(self):
        if self.message:
            # message = self.message.serialize()
            # lastmessage = self.message.last().serialize()
            messages = []
            for message in self.message.all():
                messages.append(message.serialize())
        else:
            message = 'none'
        
        users = []
        for user in self.users.all():
            users.append(user.serialize())
        return {
            "id": self.id,
            'name': self.group_name,
            'users': users,
            'messages': messages,
            # 'lastmessage': lastmessage,
            # "group_name": self.username,
        }
    
    def listserialize(self):
        if self.message:
            lastmessage = self.message.last().serialize()
        else:
            lastmessage = 'none'
        return {
            "id": self.id,
            'name': self.group_name,
            'lastmessage': lastmessage,
        }
    # def latest_message(self):
    #     # Return the latest message in the chat room
    #     return self.message.last()

    # def last_message_read(self, user):
    #     # Check if the last message is read by the given user
    #     latest_message = self.latest_message()
    #     if latest_message:
    #         return latest_message.read_by.filter(id=user.id).exists()
    #     return False

    # def unread_messages_count(self, user):
    #     # Check for unread messages count
    #     last_read_message = self.message.filter(read_by=user).last()
    #     if last_read_message:
    #         unread_messages = self.message.filter(timestamp__gt=last_read_message.timestamp).count()
    #         return unread_messages
    #     else:
    #         return self.message.count()

    def __str__(self):
        return f"Chat Room {self.id}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messageSender")
    content = models.CharField(max_length=10000000000000)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="message")  # Add related_name
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name="read_messages", blank=True)  # Add this line

    def __str__(self):
        return f"Message from {self.sender} to {self.chat_room}"
    
    def serialize(self):
        read_by_array = []
        for user in self.read_by.all():
            read_by_array.append(user.username)
        return {
            "sender": self.sender.username,
            "content": self.content,
            "chat_room": self.chat_room.id,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read_by": read_by_array
        }


class Request(models.Model):
    requestee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requestee')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requester")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return{
            'id': self.id,
            'requestee' : self.requestee.serialize(),
            'requester': self.requester.serialize(),
            'time': self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }