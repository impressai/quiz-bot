import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .reply_factory import generate_bot_responses


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = self.scope['session'].session_key

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        user_message = text_data_json['message']

        if user_message == '/reset':
            self.scope['session']['current_question_id'] = None
            self.scope['session']['message_history'] = []
            self.scope['session'].save()
            return

        user_message_obj = {
            'type': 'chat_message',
            'is_user': True,
            'text': user_message
        }

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            user_message_obj
        )

        bot_response_list = generate_bot_responses(user_message, self.scope['session'])
        for bot_response in bot_response_list:
            bot_response_obj = {
                'type': 'chat_message',
                'is_user': False,
                'text': bot_response
            }
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                bot_response_obj
            )

    def chat_message(self, message_obj):
        # Send message to WebSocket
        self.send(text_data=json.dumps(message_obj))
        self.add_to_history(message_obj)

    def add_to_history(self, message_obj):
        message_history = self.scope['session'].get('message_history', [])
        message_history.append(message_obj)
        self.scope['session']['message_history'] = message_history
        self.scope['session'].save()
