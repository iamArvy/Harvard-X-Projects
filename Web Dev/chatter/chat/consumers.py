import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message, User
from django.shortcuts import get_object_or_404
# from django.http import JsonResponse
from channels.db import database_sync_to_async
from django.core.paginator import Paginator, EmptyPage

class ChatConsumer(AsyncWebsocketConsumer):
    connected_users = {}
    async def connect(self):
        self.chat_room_id = self.scope['url_route']['kwargs']['crid']
        self.chat_room = await self.get_chat_room(self.chat_room_id)
        self.user = self.scope['user']

        if not self.chat_room:
            await self.close()

        await self.channel_layer.group_add(
            self.chat_room.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_room.group_name,
            self.channel_name
        )
        
        user_id = self.scope['user'].id
        
        if user_id in self.connected_users:
            del self.connected_users[user_id]
        else:
            pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        
    
        if data['type'] == 'pagenumber':
            page = data['page']
            self.prev_msgs = await self.getprevmsgs(self.chat_room, page)
            await self.send_messages()
        else:
            pass
        
        if data['type'] == 'sendmessage':
            message_content = data['message']
            sender = self.scope['user']
            message = await self.save_message(sender, message_content)
            await self.mark_message_as_read(message)
            await self.channel_layer.group_send(
                self.chat_room.group_name,
                {
                    'type': 'chat.message',
                    'message_id': message.id,
                    'message_content': message.content,
                    'sender_username': sender.username,
                    'timestamp': message.timestamp.strftime("%b %d %Y, %I:%M %p"),
                }
            )
            await self.channel_layer.group_send(
                'chat_list',
                {
                    'type': 'chat.message_received',
                    'chat_room_id': self.chat_room_id,
                }
            )
        else:
            pass
        
    @database_sync_to_async
    def get_chat_room(self, chat_room_id):
        try:
            return get_object_or_404(ChatRoom, id=chat_room_id)
        except Exception as e:
                return None
            
    @database_sync_to_async
    def getprevmsgs(self, chat_room, page):
        try:
            messages = Message.objects.filter(chat_room=chat_room).order_by('-timestamp') 
            paginator = Paginator(messages, 20)
            try:
                messages_page = paginator.page(page)
            except EmptyPage:
                messages_page = paginator.page(paginator.num_pages)
            return {
                'messages': [newmessage.serialize() for newmessage in messages_page],
                'has_next_page': messages_page.has_next()
                }
        except Exception as e:
                return None
        
    async def send_messages(self):
        content = {
            'type': 'chat.messages',
            'content': self.prev_msgs
        }
        await self.send(text_data=json.dumps(content))
        

    @database_sync_to_async
    def save_message(self, sender, content):
        message = Message.objects.create(sender=sender, chat_room=self.chat_room, content=content)
        return message
    
    @database_sync_to_async
    def mark_message_as_read(self, message):
        self.connected_users[self.scope['user'].id] = self.channel_name
        for user_id, channel_name in self.connected_users.items():
            user = User.objects.get(id=user_id)
            message.read_by.add(user)
        message.save()

    async def chat_message(self, event):
        try:
            await self.send_message(event)
        except Exception as e:
            return None

    async def send_message(self, message):
        try:
            await self.send(text_data=json.dumps({
                'type': 'chat.message',
                'message_id': message['message_id'],
                'message_content': message['message_content'],
                'sender_username': message['sender_username'],
                'timestamp': str(message['timestamp']),
            }))
        except Exception as e:
            return None

class ChatListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'chat_list',
            self.channel_name
        )
        await self.accept()

        await self.send_chat_list()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'chat_list',
            self.channel_name
        )

    async def receive(self):
        pass
    
    async def chat_message_received(self, event):
        await self.send_chat_list()

    @database_sync_to_async
    def get_user_chat_rooms(self, user):
        chat_rooms = ChatRoom.objects.filter(users=user)
        chat_rooms_data = []

        for chat_room in chat_rooms:
            if chat_room.message.exists():
                serializer = chat_room.listserialize()
                last_message_read = chat_room.message.last().read_by.filter(id=user.id).exists()
                if last_message_read:
                    unreadcount = 'none'
                else:
                    unreadcount = Message.objects.filter(chat_room=chat_room).exclude(read_by=user).count()
                friends = chat_room.users.exclude(id=user.id).first()
                friend = friends.serialize()
                content = {
                    'data':serializer,
                    'friend': friend,
                    'last_message_read': last_message_read,
                    'unreadcount': unreadcount
                }
                chat_rooms_data.append(content)
        return chat_rooms_data

    async def send_chat_list(self):
        user = self.scope['user']
        chat_rooms = await self.get_user_chat_rooms(user)
        chat_list_data = {
            'type': 'chat.list_update',
            'chat_list': chat_rooms,
        }
        await self.send(text_data=json.dumps(chat_list_data))

class NotificationConsumer(AsyncWebsocketConsumer):
    connected_users = {}
    async def connect(self):
        self.user = self.scope['user']
        await self.accept()
        await self.send_notification('Connected')

    async def send_notification(self, message):
        await self.send

    async def disconnect(self, close_code):
        # await self.channel_layer.group_discard(
        #     self.chat_room.group_name,
        #     self.channel_name
        # # )
        
        # user_id = self.scope['user'].id
        
        # if user_id in self.connected_users:
        #     del self.connected_users[user_id]
        # else:
        pass

    async def receive(self, text_data):
        # data = json.loads(text_data)
        
    
        # if data['type'] == 'pagenumber':
        #     page = data['page']
        #     self.prev_msgs = await self.getprevmsgs(self.chat_room, page)
        #     await self.send_messages()
        # else:
        #     pass
        
        # if data['type'] == 'sendmessage':
        #     message_content = data['message']
        #     sender = self.scope['user']
        #     message = await self.save_message(sender, message_content)
        #     await self.mark_message_as_read(message)
        #     await self.channel_layer.group_send(
        #         self.chat_room.group_name,
        #         {
        #             'type': 'chat.message',
        #             'message_id': message.id,
        #             'message_content': message.content,
        #             'sender_username': sender.username,
        #             'timestamp': message.timestamp.strftime("%b %d %Y, %I:%M %p"),
        #         }
        #     )
        #     await self.channel_layer.group_send(
        #         'chat_list',
        #         {
        #             'type': 'chat.message_received',
        #             'chat_room_id': self.chat_room_id,
        #         }
        #     )
        # else:
        pass
        
    # @database_sync_to_async
    # def get_chat_room(self, chat_room_id):
    #     try:
    #         return get_object_or_404(ChatRoom, id=chat_room_id)
    #     except Exception as e:
    #             return None
            
    # @database_sync_to_async
    # def getprevmsgs(self, chat_room, page):
    #     try:
    #         messages = Message.objects.filter(chat_room=chat_room).order_by('-timestamp') 
    #         paginator = Paginator(messages, 20)
    #         try:
    #             messages_page = paginator.page(page)
    #         except EmptyPage:
    #             messages_page = paginator.page(paginator.num_pages)
    #         return {
    #             'messages': [newmessage.serialize() for newmessage in messages_page],
    #             'has_next_page': messages_page.has_next()
    #             }
    #     except Exception as e:
    #             return None
        
    # async def send_messages(self):
    #     content = {
    #         'type': 'chat.messages',
    #         'content': self.prev_msgs
    #     }
    #     await self.send(text_data=json.dumps(content))
        

    # @database_sync_to_async
    # def save_message(self, sender, content):
    #     message = Message.objects.create(sender=sender, chat_room=self.chat_room, content=content)
    #     return message
    
    # @database_sync_to_async
    # def mark_message_as_read(self, message):
    #     self.connected_users[self.scope['user'].id] = self.channel_name
    #     for user_id, channel_name in self.connected_users.items():
    #         user = User.objects.get(id=user_id)
    #         message.read_by.add(user)
    #     message.save()

    # async def chat_message(self, event):
    #     try:
    #         await self.send_message(event)
    #     except Exception as e:
    #         return None

    # async def send_message(self, message):
    #     try:
    #         await self.send(text_data=json.dumps({
    #             'type': 'chat.message',
    #             'message_id': message['message_id'],
    #             'message_content': message['message_content'],
    #             'sender_username': message['sender_username'],
    #             'timestamp': str(message['timestamp']),
    #         }))
    #     except Exception as e:
    #         return None
