# from channels.generic.websocket import AsyncWebsocketConsumer

# class MyAsyncConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         await self.send(text_data=f"Echo: {text_data}")
from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync



class mysyncCounsumer(SyncConsumer):
    def websocket_connect(self,event):
        print('websocket Connected....',event)
        print("channel  layer",self.channel_layer)
        print("channel  name",self.channel_name)
        async_to_sync(self.channel_layer.group_add)('programmers',self.channel_name)

        self.send({
            'type':'websocket.accept'
        })


    def websocket_receive(self,event):
        print('Message Recevied from Cient....',event['text'])
        print('type of....',type(event['text']))
        async_to_sync(self.channel_layer.group_send)('programmers',{
            'type':'chat.message',
            'message':event['text']
        })
    def chat_message(self,event):
        print('Event ...',event)
        print('Actual data',event['message'])

        self.send({
            'type':'websocket.send',
            'text':event['message']
        })




    def websocket_disconnect(self,event):
        print("channel  layer",self.channel_layer)
        print("channel  name",self.channel_name)
        print('websocket Disconnected....',event)   
        async_to_sync(self.channel_layer.group_discard)("programmers",self.channel_name)
        raise StopConsumer()



from channels.generic.websocket import AsyncConsumer

class myAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('WebSocket Connected....', event)
        print("Channel layer:", self.channel_layer)
        print("Channel name:", self.channel_name)
        
        # Add the current channel to a group
        await self.channel_layer.group_add('programmers', self.channel_name)

        # Accept the WebSocket connection
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('Message Received from Client....', event['text'])
        print('Type of message....', type(event['text']))
        
        # Broadcast the message to the group
        await self.channel_layer.group_send(
            'programmers',
            {
                'type': 'chat_message',
                'message': event['text']
            }
        )

    async def chat_message(self, event):
        print('Event....', event)
        print('Actual data....', event['message'])

        # Send the message to the WebSocket
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self, event):
        print("Channel layer:", self.channel_layer)
        print("Channel name:", self.channel_name)
        print('WebSocket Disconnected....', event)
        
        # Remove the current channel from the group
        await self.channel_layer.group_discard('programmers', self.channel_name)

        # Stop the consumer
        raise StopConsumer()
