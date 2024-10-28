from inspect import getmembers
from rest_framework import serializers, viewsets
from .models import Group, GroupMember, Users
from .models import UserTask
from .models import Note
from .models import OneOffMeetingTable
from .models import Poll
from .models import MeetingPoll
from .models import Test
from .models import AllPolls
from .models import AllTask
from .models import TaskCategory
from .models import UploadedImage
from .models import SnapShot
from .models import AllSnapShot
from .models import Document
from .models import Sketch
from .models import ScheduleMeetingBufferTimeSetting
from .models import AudioRecording
from .models import WorkFlow
from .models import ChatMessage
from .models import Profile
from .models import UserDeviceToken
from .models import News
from django.contrib.auth.models import User



class UserDeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDeviceToken
        fields = ['user', 'token', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']  #

    def create(self, validated_data):
        # Automatically set the user to the authenticated user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_token(self, value):
        # Ensure that the token is unique for the user
        if UserDeviceToken.objects.filter(user=self.context['request'].user, token=value).exists():
            raise serializers.ValidationError("This token is already associated with this user.")
        return value
 
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'profile_picture', 'created_at']
        read_only_fields = ['user', 'created_at'] 

    def create(self, validated_data):
        """Override the create method to handle profile creation."""
        user = validated_data.pop('user')  # Remove user from validated data
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        """Override the update method to handle profile updates."""
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['id','user', 'profile_picture','created_at']  # Fields to include in the serializer

#     def create(self, validated_data):
#         """Override the create method to handle profile creation."""
#         profile = Profile.objects.create(**validated_data)
#         return profile

#     def update(self, instance, validated_data):
#         """Override the update method to handle profile updates."""
#         instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
#         instance.save()
#         return instance

class ChatMessageSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    
    class Meta:
        model = ChatMessage
        fields = ['id','message_id', 'group_id', 'user_id', 'text', 'created_at']


class ScheduleMeetingBufferTimeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleMeetingBufferTimeSetting
        fields = ['id',"buffer_time", "created_by", "created_at"]
        
class WorkFlowSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = WorkFlow
        fields = ['id',"title", "created_by", "created_at"]
        
class SketchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sketch
        fields = ['id',"file", "uploaded_by", "created_at"]
        
class AudioRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioRecording
        fields = ['id',"audio_file", "record_by", "uploaded_at"]
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id',"file", "uploaded_by", "created_at"]
        
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id',"fullname", "email", "password"]
        
class AllPollSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = AllPolls
        fields = ['p_poll_id', 'p_question', 'p_option1', 'p_option2', 'created_by', 'created_at']
        
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ["test_id", "title"]
        
# class CreateTaskMainSerializer(serializers.ModelSerializer):
#     created_by = serializers.PrimaryKeyRelatedField(read_only=True)
#     class Meta:
#         model = UserTask
#         fields = ['task_id', 'title', 'task_type', 'task_date', 'task_time','created_by', 'created_at']
        
class CreateTaskMainSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = AllTask
        fields = ['t_task_id', 't_title', 't_task_type', 't_task_date', 't_task_time', 'created_by', 'created_at']
        
class TaskCategorySerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = TaskCategory
        fields = ['task_category_id','name', 'created_by', 'created_at']
        
class NoteSerializer(serializers.ModelSerializer):
    # Specify that 'created_by' should use the user's ID
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Note
        fields = ['note_id', 'title', 'category', 'description', 'created_by', 'created_at', 'note_link']  
        
class ConnectPollSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Poll
        fields = ['poll_id', 'question', 'option1', 'option2', 'created_by', 'created_at']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  
       
        
#..........................group.......................
class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ['id','name','members', 'created_by', 'created_at']
        

class GroupSerializer(serializers.ModelSerializer):
    admin = serializers.CharField(source='created_by.username')
    members = serializers.SlugRelatedField(slug_field='username', many=True, queryset=User.objects.all())

    class Meta:
        model = Group
        fields = ['id', 'name', 'created_at', 'admin', 'members']

# Viewset to retrieve the group with members
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
        
class GroupMemberSerializerold(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = GroupMember
        fields = ['group','user', 'added_at']
#..................group end..............................

class OneOffMeetingMainSerializer(serializers.ModelSerializer):
    # Specify that 'created_by' should use the user's ID and be read-only
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
    # Meeting link will be generated after creation, so it should be read-only
    meeting_link = serializers.CharField(read_only=True)

    # Add emails field (use ListField with CharField)
    emails = serializers.ListField(
        child=serializers.EmailField(), 
        write_only=True
    )

    class Meta:
        model = OneOffMeetingTable
        fields = [
            'id','meeting_id', 'meetingname', 'starttime', 'endtime', 'meeting_date', 
            'duration', 'location', 'description', 'additionalinfo', 'available_times', 
            'status', 'meeting_link', 'phone_numbers', 'emails', 'created_by', 'created_at'
        ]

    def validate_emails(self, value):
        # Validate that all emails correspond to valid users
        invalid_emails = []
        for email in value:
            if not User.objects.filter(email=email).exists():
                invalid_emails.append(email)
        if invalid_emails:
            raise serializers.ValidationError(f"Users with emails {', '.join(invalid_emails)} do not exist.")
        return value


        
        
# class OneOffMeetingMainSerializer(serializers.ModelSerializer):
#     # Specify that 'created_by' should use the user's ID and be read-only
#     created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
#     # Meeting link will be generated after creation, so it should be read-only
#     meeting_link = serializers.CharField(read_only=True)

#     class Meta:
#         model = OneOffMeetingTable
#         fields = [
#             'meeting_id', 'meetingname', 'starttime', 'endtime', 'meeting_date', 
#             'duration', 'location', 'description', 'additionalinfo', 'available_times', 
#             'status', 'meeting_link','phone_numbers', 'created_by', 'created_at'
#         ]
#++++++++++++++++++++++++++++ meet poll================================
class MeetingPollSerializer(serializers.ModelSerializer):
    # Specify that 'created_by' should use the user's ID and be read-only
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
    # Meeting link will be generated after creation, so it should be read-only
    meeting_link = serializers.CharField(read_only=True)

    class Meta:
        model = MeetingPoll
        fields = [
            'meeting_id', 'meetingname', 'starttime', 'endtime', 'meeting_date', 
            'duration', 'location', 'description', 'available_times', 
            'status', 'meeting_link', 'created_by', 'created_at'
        ]
        
class SnapShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnapShot
        fields = ['id', 'user_image', 'user_description','uploaded_by', 'uploaded_at']
        
class AllSnapShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllSnapShot
        fields = ['id', 'image','uploaded_by', 'uploaded_at']
        
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id','title','description', 'image','created_by', 'uploaded_at']
        
class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['id', 'image', 'description','others','uploaded_by', 'uploaded_at']
        
# class OneOffMeetingSerializer(serializers.ModelSerializer):
#     # Specify that 'created_by' should use the user's ID
#     created_by = serializers.PrimaryKeyRelatedField(read_only=True)
#     class Meta:
#         model = OneOffMeeting
#         fields = ['meeting_id', 'meetingname', 'starttime', 'endtime','meeting_date','duration','location','description','additionalinfo','created_by', 'created_at']
        
    
        