# api/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import uuid
from .models import ChatMessage
from django.contrib.auth import get_user_model


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"Connecting to room: {self.scope['url_route']['kwargs']['room_name']}")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f"Disconnected from room: {self.room_name}, close_code: {close_code}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            print(f"Received data: {data}")

            message_type = data['type']
            if message_type == 'chat_message':
                await self.handle_chat_message(data)
            elif message_type == 'delete_message':
                await self.handle_delete_message(data)
            else:
                print(f"Unknown message type: {message_type}")

        except json.JSONDecodeError:
            print("Invalid JSON received")
            await self.close()
        except Exception as e:
            print(f"Error processing message: {e}")
            await self.close()

    async def handle_chat_message(self, data):
        message_id = uuid.uuid4()  # Generate a unique message_id
        message = data['message']
        sender = self.scope['user']  # Get the current user

        # Save the message to the database
        chat_message = ChatMessage.objects.create(
            message_id=message_id,
            group_id=data['group_id'],  
            user_id=sender,
            text=message,
        )

        # Broadcast the message to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message_to_room',
                'message_id': str(chat_message.message_id),
                'message': chat_message.text,
                'from': sender.username,
            }
        )

    async def handle_delete_message(self, data):
        message_id = data.get('message_id')
        user = self.scope['user']

        try:
            # Check if the message exists and belongs to the user
            chat_message = ChatMessage.objects.get(message_id=message_id, user_id=user)
            chat_message.delete()

            # Notify the room that the message has been deleted
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'delete_message_to_room',
                    'message_id': message_id,
                }
            )

        except ChatMessage.DoesNotExist:
            print("Message not found or user not authorized to delete it")

    async def chat_message_to_room(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_id': event['message_id'],
            'message': event['message'],
            'from': event['from'],
        }))

    async def delete_message_to_room(self, event):
        # Send delete notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'delete_message',
            'message_id': event['message_id'],
        }))

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         print(f"Connecting to room: {self.scope['url_route']['kwargs']['room_name']}")
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         print(f"Disconnected from room: {self.room_name}, close_code: {close_code}")
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         try:
#             data = json.loads(text_data)
#             print(f"Received data: {data}")

#             message_type = data['type']
#             if message_type == 'webrtc_offer':
#                 await self.send_offer(data)
#             elif message_type == 'webrtc_answer':
#                 await self.send_answer(data)
#             elif message_type == 'new_ice_candidate':
#                 await self.send_ice_candidate(data)
#             else:
#                 print(f"Unknown message type: {message_type}")

#         except json.JSONDecodeError:
#             print("Invalid JSON received")
#             await self.close()
#         except Exception as e:
#             print(f"Error processing message: {e}")
#             await self.close()


#     async def send_offer(self, offer_data):
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'send_offer_to_room',
#                 'offer': offer_data['offer'],
#                 'from': offer_data['from']
#             }
#         )

#     async def send_answer(self, answer_data):
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'send_answer_to_room',
#                 'answer': answer_data['answer'],
#                 'from': answer_data['from']
#             }
#         )

#     async def send_ice_candidate(self, candidate_data):
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'send_candidate_to_room',
#                 'candidate': candidate_data['candidate'],
#                 'from': candidate_data['from']
#             }
#         )

#     async def send_offer_to_room(self, event):
#         await self.send(text_data=json.dumps({
#             'type': 'webrtc_offer',
#             'offer': event['offer'],
#             'from': event['from'],
#         }))

#     async def send_answer_to_room(self, event):
#         await self.send(text_data=json.dumps({
#             'type': 'webrtc_answer',
#             'answer': event['answer'],
#             'from': event['from'],
#         }))

#     async def send_candidate_to_room(self, event):
#         await self.send(text_data=json.dumps({
#             'type': 'new_ice_candidate',
#             'candidate': event['candidate'],
#             'from': event['from'],
#         }))

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"Connecting to room: {self.scope['url_route']['kwargs']['room_name']}")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'call_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f"Disconnected from room: {self.room_name}, close_code: {close_code}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            print(f"Received data: {data}")

            message_type = data['type']
            if message_type == 'webrtc_offer':
                await self.send_offer(data)
            elif message_type == 'webrtc_answer':
                await self.send_answer(data)
            elif message_type == 'new_ice_candidate':
                await self.send_ice_candidate(data)
            else:
                print(f"Unknown message type: {message_type}")

        except json.JSONDecodeError:
            print("Invalid JSON received")
            await self.close()
        except Exception as e:
            print(f"Error processing message: {e}")
            await self.close()

    async def send_offer(self, offer_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_offer_to_room',
                'offer': offer_data['offer'],
                'from': offer_data['from']
            }
        )

    async def send_answer(self, answer_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_answer_to_room',
                'answer': answer_data['answer'],
                'from': answer_data['from']
            }
        )

    async def send_ice_candidate(self, candidate_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_candidate_to_room',
                'candidate': candidate_data['candidate'],
                'from': candidate_data['from']
            }
        )

    async def send_offer_to_room(self, event):
        await self.send(text_data=json.dumps({
            'type': 'webrtc_offer',
            'offer': event['offer'],
            'from': event['from'],
        }))

    async def send_answer_to_room(self, event):
        await self.send(text_data=json.dumps({
            'type': 'webrtc_answer',
            'answer': event['answer'],
            'from': event['from'],
        }))

    async def send_candidate_to_room(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_ice_candidate',
            'candidate': event['candidate'],
            'from': event['from'],
        }))




