import json
from channels.generic.websocket import AsyncWebsocketConsumer 
from asgiref.sync import async_to_sync
from chat.models import Mychats
# from django.contrib.auth.models import User
from user_auth.models import CustomUser as User
from time import sleep
import datetime
from channels.db import database_sync_to_async


class MychatApp(AsyncWebsocketConsumer):
    
    async def connect(self):
        print(f"==================id {self.scope['user'].id}")
        await self.accept() 
        await self.channel_layer.group_add(f"mychat_app_{self.scope['user'].id}", self.channel_name)
         
         
    async def disconnect(self, close_code): 
        pass
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data = json.loads(text_data)
        frnd_user_id = await self.get_user_id_by_username(text_data['user'])
        print(f"==================frnd_user_id= {frnd_user_id}")
        print(f"==================text_data= {text_data['user']}")
        await self.channel_layer.group_send(
            f"mychat_app_{frnd_user_id}",
            {
                'type':'send.msg',
                'msg':text_data['msg']
            }
            )
        print(f"text user================== {text_data['user']}")
        await self.save_chat(text_data)

    @database_sync_to_async   
    def save_chat(self,text_data):
        frnd = User.objects.get(username=text_data['user'])
        mychats, created = Mychats.objects.get_or_create(me=self.scope['user'], frnd=frnd)
        # If the object was just created, initialize the 'chats' field as an empty dictionary
        if created:
            mychats.chats = {}
        mychats.chats[str(datetime.datetime.now())+"1"] = {'user': 'me', 'msg': text_data['msg']}
        mychats.save()
        mychats, created = Mychats.objects.get_or_create(me=frnd, frnd=self.scope['user'])
        # If the object was just created, initialize the 'chats' field as an empty dictionary
        if created:
            mychats.chats = {}
        mychats.chats[str(datetime.datetime.now())+"2"] = {'user': frnd.username, 'msg': text_data['msg']}
        mychats.save()
    async def send_videonofication(self,event):
        await  self.send(event['msg'])

    async def send_msg(self,event):
        print(event['msg'])
        await  self.send(event['msg'])
    async def chat_message(self, event):
        print(event['message'])
        await self.send(json.dumps("Total Online :- "+str(event['message'])))

    @database_sync_to_async
    def get_user_id_by_username(self, username):
        return User.objects.get(username=username).id