import base64
import json
import logging
from typing import Generic
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .serializer import UsersSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from .serializer import CreateTaskMainSerializer
from django.contrib.auth.models import User
from .serializer import NoteSerializer
from .serializer import AllPollSerializer
from .serializer import OneOffMeetingMainSerializer
from .serializer import ScheduleMeetingBufferTimeSettingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from rest_framework.generics import RetrieveAPIView
from .models import Group, GroupMember, OneOffMeetingTable
from .models import MeetingPoll
from .models import AllTask
from .models import Note
from .models import TaskCategory
from .serializer import MeetingPollSerializer
from .serializer import TaskCategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import AllSnapShot
from .serializer import GroupSerializer
from .serializer import AllSnapShotSerializer
from .serializer import DocumentSerializer
from .serializer import SketchSerializer
from .serializer import AudioRecordingSerializer
from .serializer import UserSerializer
from .serializer import ProfileSerializer
from .serializer import ChatMessageSerializer
from django.core.files.base import ContentFile
from .models import Document
from .models import ScheduleMeetingBufferTimeSetting
from .models import Sketch
from .models import AudioRecording
from datetime import timedelta
from dateutil.parser import parse  # Import the parse function
from api import models
from .models import WorkFlow
from .models import Profile
from .models import ChatMessage
from .models import News
from .serializer import WorkFlowSerializer
from .serializer import NewsSerializer
logger = logging.getLogger(__name__)



class ProfileView(APIView):

    def post(self, request):
        """Create or update the profile for a user."""
        user = request.user  # Assuming the user is authenticated

        # Try to get the existing profile
        profile, created = Profile.objects.get_or_create(user=user)  # This create a new profile if it doesn't exist
        
        serializer = ProfileSerializer(profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save() 
            if created:
                return Response({"message": "Profile created successfully", "profile": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Profile updated successfully", "profile": serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Update the user's profile."""
        user = request.user 
        try:
            profile = Profile.objects.get(user=user)  
        except Profile.DoesNotExist:
            return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save() 
            return Response({"message": "Profile updated successfully", "profile": serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            u_profile = Profile.objects.filter(user=request.user).order_by('created_at')
            serializer = ProfileSerializer(u_profile, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'No profile were found'}, status=status.HTTP_404_NOT_FOUND)

class SaveFCMToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        user = request.user  

        if token:  # Ensure the token is provided
            try:
                user.push_token = token 
                user.save()
                return Response({'message': 'Token saved'}, status=200)
            except Exception as e:
                return Response({'error': str(e)}, status=500)
        return Response({'error': 'No token provided'}, status=400)

    

class CreateChatMessage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Add the user to the request data, so it’s automatically filled in the serializer
        request_data = request.data.copy()  
        request_data['user_id'] = request.user.id 

        serializer = ChatMessageSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Chat saved successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetChatMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the 'group_id' from the query parameters
        group_id = request.query_params.get('group_id')
        
        if not group_id:
            return Response({'error': 'group_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Filter messages based on the authenticated user and the group ID
            all_chat_message = ChatMessage.objects.filter(group_id=group_id).order_by('created_at')
            serializer = ChatMessageSerializer(all_chat_message, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        except ChatMessage.DoesNotExist:
            return Response({'error': 'No chat messages found for this group'}, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['DELETE'])
def delete_message(request, message_id):
    try:
        message = ChatMessage.objects.get(message_id=message_id)
        message.delete()
        return Response({"message": "Message deleted successfully"}, status=status.HTTP_200_OK)
    except ChatMessage.DoesNotExist:
        return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) 
def delete_task_category(request, task_category_id):
    
    try:
        task = TaskCategory.objects.get(task_category_id=task_category_id)
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_200_OK)
    except TaskCategory.DoesNotExist:
        return Response({"error": "Taskcategory not found"}, status=status.HTTP_404_NOT_FOUND)



# class GetChatMessageView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         try:
#             all_chat_message = ChatMessage.objects.filter(user_id=request.user).order_by('created_at')
#             serializer = ChatMessageSerializer(all_chat_message, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except WorkFlow.DoesNotExist:
#             return Response({'error': 'No chat were found'}, status=status.HTTP_404_NOT_FOUND)
            

class CreateWorkFlowView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = WorkFlowSerializer(data=request.data)
        if serializer.is_valid():
          serializer.save(created_by=request.user)
          return Response({"message": 'workflow was created'}, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetWorkFlowView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            all_work_flow = WorkFlow.objects.filter(created_by=request.user).order_by('created_at')
            serializer = WorkFlowSerializer(all_work_flow, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except WorkFlow.DoesNotExist:
            return Response({'error': 'No work_flow were found'}, status=status.HTTP_404_NOT_FOUND)
    

class GetTaskCategoryView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
            # 'uploaded_by' is the field that stores the user who uploaded the image
            all_task_category = TaskCategory.objects.filter(record_by=request.user).order_by('created_at')

            # Serialize the queryset, make sure to use many=True
            serializer = TaskCategorySerializer(all_task_category, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TaskCategory.DoesNotExist:  
            return Response({'error': 'No category were found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NoteSearchView(APIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request,):
        query = request.query_params.get('q', None)
        if query:
            note = Note.objects.filter(Q(title__icontains=query), created_by=request.user)
        else:
            note = Note.objects.none()

        # Serialize the result
        serializer = self.serializer_class(note, many=True)
        return Response(serializer.data)
    
class OneOffMeetingSearchView(APIView):
    serializer_class = OneOffMeetingMainSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request,):
        query = request.query_params.get('q', None)
        if query:
            meeting = OneOffMeetingTable.objects.filter(Q(meetingname__icontains=query), created_by=request.user)
        else:
            meeting = OneOffMeetingTable.objects.none()

        # Serialize the result
        serializer = self.serializer_class(meeting, many=True)
        return Response(serializer.data)
    
class GetAllNoteById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, note_id):
        try:
            # Fetch the task by the given task_id
            All_note = Note.objects.get(note_id=note_id, created_by=request.user)

            # Serialize the task data
            note_main_data = NoteSerializer(All_note).data

            # Get the admin (creator) of the task
            admin = All_note.created_by
            admin_data = {'id': admin.id, 'username': admin.username, 'is_admin': True}

            # Access the task's title or name directly
            note_name = All_note.title  

            return Response({
                'admin': admin_data,
                'note_table': note_main_data,
                'note_title_name': note_name,
            })
        except AllTask.DoesNotExist:
            return Response({'error': 'Task not found'}, status=404)
    
class TaskSearchView(APIView):
    serializer_class = CreateTaskMainSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request,):
        query = request.query_params.get('q', None)
        if query:
            tasks = AllTask.objects.filter(Q(t_title__icontains=query), created_by=request.user)
        else:
            tasks = AllTask.objects.none()

        # Serialize the result
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data)
    
class GetAllTaskById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, t_task_id):
        try:
            # Fetch the task by the given task_id
            All_task = AllTask.objects.get(t_task_id=t_task_id, created_by=request.user)

            # Serialize the task data
            task_main_data = CreateTaskMainSerializer(All_task).data

            # Get the admin (creator) of the task
            admin = All_task.created_by
            admin_data = {'id': admin.id, 'username': admin.username, 'is_admin': True}

            # Access the task's title or name directly
            task_name = All_task.t_title  

            return Response({
                'admin': admin_data,
                'task_table': task_main_data,
                'task_title_name': task_name,
            })
        except AllTask.DoesNotExist:
            return Response({'error': 'Task not found'}, status=404)


class DocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  

    def post(self, request):
    
        data = request.data.copy()

        # Set the `uploaded_by` field to the current authenticated user
        data['uploaded_by'] = request.user.id

        serializer = DocumentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def upload_audio_recording(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('file')
        if audio_file:
            audio_recording = AudioRecording(record_by=request.user, audio_file=audio_file)
            audio_recording.save()  # Save the audio recording to the database
            return Response({"message": "Audio uploaded successfully", "file_path": audio_recording.audio_file.url}, status=status.HTTP_201_CREATED)
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    
class GetAudioRecordingView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
            # Assuming 'uploaded_by' is the field that stores the user who uploaded the image
            all_audio = AudioRecording.objects.filter(record_by=request.user).order_by('uploaded_at')

            # Serialize the queryset, make sure to use many=True
            serializer = AudioRecordingSerializer(all_audio, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AudioRecording.DoesNotExist:  # Corrected the exception to UploadedImage
            return Response({'error': 'No Audio recording were found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class GetOneOffMeeting(APIView):
    permission_classes = [IsAuthenticated]
     
    def get(self, request):
    
     try: 
        all_meeting_data = OneOffMeetingTable.objects.filter(created_by=request.user).order_by('created_at')
        seriliazer = OneOffMeetingMainSerializer(all_meeting_data, many=True)
        return Response(seriliazer.data, status=status.HTTP_200_OK)
     except:
         OneOffMeetingTable.DoesNotExist
         return Response({'message': 'No Meeting found'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def upload_sketch(request):
    if request.method == 'POST':
        data = request.data

        
        base64_string = data.get('file')

        # Check if the base64 string is valid
        if not base64_string:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

       
        if base64_string.startswith('data:image/png;base64,'):
            base64_string = base64_string.replace('data:image/png;base64,', '')

        # Decode the base64 string
        file_data = base64.b64decode(base64_string)

        # Create a ContentFile to save it to the FileField
        content_file = ContentFile(file_data, name='sketch.png')  

        # Create a new Sketch object and save it
        sketch = Sketch(file=content_file, uploaded_by=request.user)
        sketch.save()

        return Response({'message': 'File uploaded successfully.'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class GetSketchView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
            # Assuming 'uploaded_by' is the field that stores the user who uploaded the image
            all_sketch = Sketch.objects.filter(uploaded_by=request.user).order_by('created_at')

            # Serialize the queryset, make sure to use many=True
            serializer = SketchSerializer(all_sketch, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Sketch.DoesNotExist:  # Corrected the exception to UploadedImage
            return Response({'error': 'No sketch image were found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetDocumentView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this endpoint

    def get(self, request):
        try:
            # Assuming 'uploaded_by' is the field that stores the user who uploaded the image
            all_documents = Document.objects.filter(uploaded_by=request.user).order_by('created_at')

            # Serialize the queryset, make sure to use many=True
            serializer = DocumentSerializer(all_documents, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Document.DoesNotExist:  # Corrected the exception to UploadedImage
            return Response({'error': 'No document were found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EplanApiView(APIView):
    def post(self, request):
        #  post request
        data = {'message': 'Welcome to Eplan'}
        return Response(data, status=status.HTTP_200_OK)

class Users(APIView):
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Form submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterUser(APIView):
    def post(self, request):
        # Extract data from the request
        first_name = request.data.get('firstname')  
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({
                "error": "All fields are required",
                "username": username,
                "email": email,
                "password": password
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the email or username already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already taken"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the new user
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
            first_name=first_name  
        )
        user.save()

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


# class RegisterUser(APIView):
#     def post(self, request):
#         # Extract data from the request
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')

#         if not username or not email or not password:
#             return Response({"error": "All fields are required","username":username,"email" :email,"password": password}, status=status.HTTP_400_BAD_REQUEST)
        
#          # Check if the email or username already exists
#         if User.objects.filter(username=username).exists():
#             return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(email=email).exists():
#             return Response({"error": "Email already taken"}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Create the new user
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.save()

#         return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
        # Check if the username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Username not found"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the password matches
        if not check_password(password, user.password):
            return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate the user
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens for the authenticated user
        refresh = RefreshToken.for_user(authenticated_user)
        return Response({
            'refresh': str(refresh),
            'access_token': str(refresh.access_token),
            'user': {
                'id': authenticated_user.id,  # Include the user's ID
                'username': authenticated_user.username,
                'email': authenticated_user.email
            }
        }, status=status.HTTP_200_OK)
        
    
class CreateTaskMainView(APIView):
    def post(self, request):
        serializer = CreateTaskMainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({"message": 'Task has been successfully created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateNote(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"Authenticated User ID: {request.user.id}")
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            note = serializer.save(created_by=request.user)  # Save the note instance

            # Generate a shareable link using the note's ID
            note_link = request.build_absolute_uri(reverse('note-detail', args=[note.note_id]))

            # Update the note instance with the generated note link
            note.note_link = note_link
            note.save()

            return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)  

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NoteDetailView(APIView):
    def get(self, request, note_id):
        try:
            note = Note.objects.get(note_id=note_id)  
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Note.DoesNotExist:
            return Response({'detail': 'No Note matches the given query.'}, status=status.HTTP_404_NOT_FOUND)
    
    
class SetBufferTime(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the buffer time value from the request
        buffer_time = request.data.get('buffer_time', 0)  # Default to 0 if not provided

        # Fetch the latest buffer time setting for the user
        buffer_time_setting = ScheduleMeetingBufferTimeSetting.objects.filter(created_by=request.user).first()

        if buffer_time_setting:
            # Update the existing setting
            buffer_time_setting.buffer_time = buffer_time
            buffer_time_setting.save()
            return Response({
                'message': 'Buffer time setting updated successfully',
                'buffer_time': buffer_time_setting.buffer_time
            }, status=status.HTTP_200_OK)
        else:
            # Create a new setting if no existing setting found
            buffer_time_setting = ScheduleMeetingBufferTimeSetting(
                buffer_time=buffer_time,
                created_by=request.user,
            )
            buffer_time_setting.save()
            return Response({
                'message': 'Buffer time setting saved successfully',
                'buffer_time': buffer_time_setting.buffer_time
            }, status=status.HTTP_201_CREATED)
            
class GetBufferView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this endpoint

    def get(self, request):
        try:
            # Assuming 'uploaded_by' is the field that stores the user who uploaded the image
            all_documents = ScheduleMeetingBufferTimeSetting.objects.filter(created_by=request.user).order_by('created_at')

            # Serialize the queryset, make sure to use many=True
            serializer = ScheduleMeetingBufferTimeSettingSerializer(all_documents, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ScheduleMeetingBufferTimeSetting.DoesNotExist:  # Corrected the exception to UploadedImage
            return Response({'error': 'No buffer were found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreateOneOffMeeting(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"Authenticated User ID: {request.user.id}")

        serializer = OneOffMeetingMainSerializer(data=request.data)
        if serializer.is_valid():
            global_settings = ScheduleMeetingBufferTimeSetting.objects.first()
            global_buffer_time = global_settings.buffer_time if global_settings else 0
            buffer_time = request.data.get('buffer_time', global_buffer_time)

            meeting_data = serializer.validated_data
            start_time = meeting_data['starttime']
            end_time = meeting_data['endtime']

            start_time = parse(start_time) - timedelta(minutes=buffer_time)
            end_time = parse(end_time) + timedelta(minutes=buffer_time)

            # Create the meeting with adjusted times
            meeting = OneOffMeetingTable(
                meetingname=meeting_data['meetingname'],
                starttime=start_time.strftime("%Y-%m-%d %H:%M:%S"),
                endtime=end_time.strftime("%Y-%m-%d %H:%M:%S"),
                meeting_date=meeting_data['meeting_date'],
                duration=meeting_data['duration'],
                location=meeting_data['location'],
                description=meeting_data['description'],
                additionalinfo=meeting_data['additionalinfo'],
                created_by=request.user,  # Automatically associate with the authenticated user
            )
            meeting.save()

            # Add users by their emails (convert emails to User instances)
            email_list = request.data.get('emails', [])
            users_to_add = []

            for email in email_list:
                try:
                    # Get user by email
                    user = User.objects.get(email=email)
                    users_to_add.append(user)  # Add the User instance to the list
                except User.DoesNotExist:
                    return Response({'error': f"User with email {email} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            # Use set() to add the list of User instances to the Many-to-Many field
            meeting.emails.set(users_to_add)

            # Add phone numbers (if applicable)
            phone_numbers = request.data.get('phone_numbers', [])
            meeting.phone_numbers = phone_numbers
            meeting.save()

            # Generate a shareable meeting link
            meeting_link = request.build_absolute_uri(reverse('meeting-detail', args=[meeting.meeting_id]))
            meeting.meeting_link = meeting_link
            meeting.save()
            
           

      

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateOneOffMeeting(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, meeting_id):
        try:
            meeting = OneOffMeetingTable.objects.get(meeting_id=meeting_id)
        except OneOffMeetingTable.DoesNotExist:
            return Response({'error': 'Meeting not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OneOffMeetingMainSerializer(meeting, data=request.data)
        if serializer.is_valid():
            global_settings = ScheduleMeetingBufferTimeSetting.objects.first()
            global_buffer_time = global_settings.buffer_time if global_settings else 0
            buffer_time = request.data.get('buffer_time', global_buffer_time)

            meeting_data = serializer.validated_data
            start_time = meeting_data['starttime']
            end_time = meeting_data['endtime']

            start_time = parse(start_time) - timedelta(minutes=buffer_time)
            end_time = parse(end_time) + timedelta(minutes=buffer_time)

            # Update the meeting with adjusted times
            meeting.meetingname = meeting_data['meetingname']
            meeting.starttime = start_time.strftime("%Y-%m-%d %H:%M:%S")
            meeting.endtime = end_time.strftime("%Y-%m-%d %H:%M:%S")
            meeting.meeting_date = meeting_data['meeting_date']
            meeting.duration = meeting_data['duration']
            meeting.location = meeting_data['location']
            meeting.description = meeting_data['description']
            meeting.additionalinfo = meeting_data['additionalinfo']

            # Update users by their emails
            email_list = request.data.get('emails', [])
            users_to_add = []
            for email in email_list:
                try:
                    user = User.objects.get(email=email)
                    users_to_add.append(user)
                except User.DoesNotExist:
                    return Response({'error': f"User with email {email} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            meeting.emails.set(users_to_add)

            # Update phone numbers
            phone_numbers = request.data.get('phone_numbers', [])
            meeting.phone_numbers = phone_numbers
            meeting.save()

            # Optionally regenerate the meeting link if needed
            meeting_link = request.build_absolute_uri(reverse('meeting-detail', args=[meeting.meeting_id]))
            meeting.meeting_link = meeting_link
            meeting.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class CreateMeetingPoll(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"Authenticated User ID: {request.user.id}")
        # Automatically associate the meeting with the authenticated user
        serializer = MeetingPollSerializer(data=request.data)
        if serializer.is_valid():
            meeting = serializer.save(created_by=request.user)
            
            # Generate a shareable meeting link using the meeting's ID or UUID
            meeting_link = request.build_absolute_uri(reverse('pool-meeting-detail', args=[meeting.meeting_id]))
            
            # Update the meeting instance with the generated meeting link
            meeting.meeting_link = meeting_link
            meeting.save()

            # Include the meeting link in the response data
            response_data = serializer.data
            response_data['meeting_link'] = meeting_link
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MeetingDetailView(RetrieveAPIView):
    queryset = OneOffMeetingTable.objects.all()
    serializer_class = OneOffMeetingMainSerializer
    lookup_field = 'meeting_id'
    
class PoolMeetingDetailView(RetrieveAPIView):
    queryset = MeetingPoll.objects.all()
    serializer_class = MeetingPollSerializer
    lookup_field = 'meeting_id'
    
    
class SelectMeetingTime(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, meeting_id):
        meeting = get_object_or_404(OneOffMeetingTable, meeting_id=meeting_id)
        selected_time = request.data.get('selected_time')

        if selected_time in meeting.available_times:
            meeting.starttime = selected_time  # Update the selected time
            meeting.save()
            return Response({'message': 'Time selected successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid time slot selected'}, status=status.HTTP_400_BAD_REQUEST)
        
class LatestMeetingView(APIView):
     
    permission_classes = [IsAuthenticated]  # Optional: Ensure only authenticated users can access this endpoint

    def get(self, request):
        try:
            # Get the latest meeting created by the authenticated user
            latest_meeting = OneOffMeetingTable.objects.filter(created_by=request.user).latest('created_at')
            serializer = OneOffMeetingMainSerializer(latest_meeting)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OneOffMeetingTable.DoesNotExist:
            return Response({'error': 'No meetings found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LastCreatedNoteView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the last note created by the authenticated user
        last_note = Note.objects.filter(created_by=request.user).order_by('-created_at').first()
        
        if last_note:
            serializer = NoteSerializer(last_note)
            # Generate a shareable link using the note's ID
            note_link = request.build_absolute_uri(reverse('note-detail', args=[last_note.note_id]))
            return Response({
                'note': serializer.data,
                'link': note_link
            }, status=status.HTTP_200_OK)
        
        return Response({'detail': 'No notes found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        
class GetAllTaskView(APIView):
     
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this endpoint

    def get(self, request):
        try:
            # Get all tasks created by the authenticated user and order them by 'created_at'
            all_task = AllTask.objects.filter(created_by=request.user).order_by('created_at')
            
            # Serialize the queryset, make sure to use many=True
            serializer = CreateTaskMainSerializer(all_task, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AllTask.DoesNotExist:
            return Response({'error': 'No tasks were found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetAllNoteView(APIView):
     
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this endpoint

    def get(self, request):
        try:
            # Get all tasks created by the authenticated user and order them by 'created_at'
            all_note = Note.objects.filter(created_by=request.user).order_by('created_at')
            
            # Serialize the queryset, make sure to use many=True
            serializer = NoteSerializer(all_note, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Note.DoesNotExist:
            return Response({'error': 'No Note were found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class GetGroupView(APIView):
     
#     permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this endpoint

#     def get(self, request):
#         try:
#             # Get all tasks created by the authenticated user and order them by 'created_at'
#             all_group = Group.objects.filter(created_by=request.user).order_by('created_at')
            
#             # Serialize the queryset, make sure to use many=True
#             serializer = GroupSerializer(all_group, many=True)
            
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Note.DoesNotExist:
#             return Response({'error': 'No group were found.'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetGroupView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this endpoint

    def get(self, request):
        try:
            # Get groups where the user is either the creator (created_by) or a member
            all_groups = Group.objects.filter(
                Q(members=request.user) | Q(created_by=request.user)
            ).distinct().order_by('created_at')

            # Serialize the queryset
            serializer = GroupSerializer(all_groups, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({'error': 'No groups were found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetGroupMembers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            # Fetch the group by the given group_id
            group = Group.objects.get(id=group_id)

            # Get all members of the group
            members = group.members.all()

            # The admin is the creator of the group
            admin = group.created_by

            # Serialize the members and admin data
            members_data = UserSerializer(members, many=True).data
            admin_data = {'id': admin.id, 'username': admin.username, 'is_admin': True}

          
            group_name = group.name

            return Response({
                'admin': admin_data,
                'members': members_data,
                'group_name': group_name,
            })
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=404)

        
class GetTaskCategoryView(APIView):
     
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
            # Get all tasks created by the authenticated user and order them by 'created_at'
            all_task_category = TaskCategory.objects.filter(created_by=request.user).order_by('created_at')
            
            # Serialize the queryset, make sure to use many=True
            serializer = TaskCategorySerializer(all_task_category, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TaskCategory.DoesNotExist:
            return Response({'error': 'No tasks category were found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteTaskCategoryView(APIView):
    permission_classes = [IsAuthenticated]  

    def delete(self, request, name=None):
        try:
            logger.info(f"Trying to delete task with name: {name}")
            
            # Ensure task category exists and belongs to the authenticated user
            task_category = TaskCategory.objects.get(name=name, created_by=request.user)
            print('task:',task_category)
            task_category.delete()

            return Response({'message': 'Task category deleted successfully'}, status=status.HTTP_200_OK)
        except TaskCategory.DoesNotExist:
            return Response({'error': 'Task category not found or you do not have permission to delete this.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PollLatestMeetingView(APIView):
     
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
            # Get the latest meeting created by the authenticated user
            latest_meeting = OneOffMeetingTable.objects.filter(created_by=request.user).latest('created_at')
            serializer = MeetingPollSerializer(latest_meeting)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MeetingPoll.DoesNotExist:
            return Response({'error': 'No meetings found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreatePoll(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        serializer = AllPollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user) # This stores the user ID
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
#-----------------------------------create group --------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    group_name = request.data.get('name')
    members = request.data.get('members', [])  # List of member IDs

    group = Group.objects.create(name=group_name, created_by=request.user)

    # Add selected members to the group
    for member_id in members:
        member_user = User.objects.get(id=member_id)
        GroupMember.objects.create(group=group, user=member_user)

    return Response({'message': 'Group created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = User.objects.all()
    user_data = [{'id': user.id, 'username': user.username} for user in users]
    return Response(user_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_users(request):
    query = request.GET.get('query', '')
    if query:
        users = User.objects.filter(username__icontains=query)[:10]
        user_data = [{'id': user.id, 'username': user.username} for user in users]
        return Response(user_data,status=status.HTTP_200_OK)
    return Response([])

@api_view(['GET'])
def search_users_email(request):
    query = request.GET.get('query', '')
    if query:
        users = User.objects.filter(email__icontains=query)[:10]
        user_data = [{'id': user.id, 'email': user.email} for user in users]
        return Response(user_data,status=status.HTTP_200_OK)
    return Response([])

@api_view(['POST'])
def add_user_to_group(request):
    group_name = request.data.get('name')
    members = request.data.get('members', [])
    user = request.user  # Get the authenticated user
    
    if not group_name or not members:
        return Response({'error': 'Group name and members are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the group with the `created_by` field set to the authenticated user
    group, created = Group.objects.get_or_create(name=group_name, created_by=user)

    for member_id in members:
        try:
            user = User.objects.get(id=member_id)
            group.members.add(user)  # Assuming `members` is a ManyToManyField in the `Group` model
        except User.DoesNotExist:
            return Response({'error': f'User with ID {member_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Users added successfully to the group'}, status=status.HTTP_201_CREATED)

class TaskCategoryView(APIView):
    
    def post(self, request):
        serializer = TaskCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NewsView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can upload

    def post(self, request):
        # Create a mutable copy of request data so that you can modify it
        data = request.data.copy()

        # Set the `uploaded_by` field to the current authenticated user
        data['created_by'] = request.user.id

        serializer = NewsSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Automatically associate the user with the image
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetNewsView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
       
            all_news = News.objects.filter().order_by('uploaded_at')

            # Serialize the queryset, make sure to use many=True
            serializer = NewsSerializer(all_news, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AllSnapShot.DoesNotExist:  # Corrected the exception to UploadedImage
            return Response({'error': 'No news were found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class AllSnapShotView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can upload

    def post(self, request):
        # Create a mutable copy of request data so that you can modify it
        data = request.data.copy()

        # Set the `uploaded_by` field to the current authenticated user
        data['uploaded_by'] = request.user.id

        serializer = AllSnapShotSerializer(data=data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)  # Automatically associate the user with the image
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class GetAllSnapShotView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
          
            all_images = AllSnapShot.objects.filter(uploaded_by=request.user).order_by('uploaded_at')

            # Serialize the queryset, make sure to use many=True
            serializer = AllSnapShotSerializer(all_images, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AllSnapShot.DoesNotExist:  # Corrected the exception to UploadedImage
            return Response({'error': 'No images were found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    





        
        
        
            
        