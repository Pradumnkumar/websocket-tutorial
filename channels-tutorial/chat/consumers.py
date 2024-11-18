import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_room = self.scope["url_route"]["kwargs"]["room_name"]
        print("Connecting")
        self.room_group_name = f"chat_{self.chat_room}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        event = {
            'type': 'chat.message',
            'message': message
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, event
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
    
    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))