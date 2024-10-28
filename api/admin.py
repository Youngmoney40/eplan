from django.contrib import admin
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
from .models import AudioRecording
from .models import ScheduleMeetingBufferTimeSetting
from .models import WorkFlow
from .models import ChatMessage
from .models import Profile
from .models import News
from .models import UserDeviceToken

# Register your models here.
@admin.register(ScheduleMeetingBufferTimeSetting)
class ScheduleMeetingBufferTimeSettingAdmin(admin.ModelAdmin):
    list_display =  ['id',"buffer_time", "created_by", "created_at"]
    
@admin.register(UserDeviceToken)
class UserDeviceTokenAdmin(admin.ModelAdmin):
    list_display =  ['user', 'token', 'created_at','updated_at'] 
    
@admin.register(WorkFlow)
class WorkFlowAdmin(admin.ModelAdmin):
    list_display =  ['id',"title", "created_by", "created_at"]
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'profile_picture','created_at') 
    search_fields = ('user__username',)

admin.site.register(Profile, ProfileAdmin)
    
@admin.register(Sketch)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id',"file", "uploaded_by", "created_at"]
    
@admin.register(AudioRecording)
class AudioRecordingAdmin(admin.ModelAdmin):
    list_display = ['id',"audio_file", "record_by", "uploaded_at"]
    
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id',"file", "uploaded_by", "created_at"]
    
# @admin.register(Users)
# class UsersAdmin(admin.ModelAdmin):
#     list_display = ['id',"fullname", "email", "password"]
    
@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ['task_category_id',"name", "created_by", "created_at"]
    
# @admin.register(UploadedImage)
# class UploadedImageAdmin(admin.ModelAdmin):
#     list_display = ['id', 'image', 'description','uploaded_by', 'uploaded_at']
    
# @admin.register(SnapShot)
# class SnapShotAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user_image', 'user_description','others', 'uploaded_by', 'uploaded_at']
    
@admin.register(AllSnapShot)
class AllSnapShotAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'uploaded_by', 'uploaded_at']
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id','title','description', 'image','created_by', 'uploaded_at']
    
@admin.register(AllPolls)
class AllPollAdmin(admin.ModelAdmin):
    list_display = ['p_poll_id', 'p_question', 'p_option1', 'p_option2', 'created_by', 'created_at']
    
# @admin.register(Test)
# class TestAdmin(admin.ModelAdmin):
#     list_display = ["test_id", "title"]
      
# @admin.register(UserTask)
# class CreateTaskMainModelListAdmin(admin.ModelAdmin):
#     list_display = ['task_id', 'title', 'task_type', 'task_date', 'task_time','created_by', 'created_at']
    
@admin.register(AllTask)
class CreateTaskMainModelListAdmin(admin.ModelAdmin):
    list_display = ['t_task_id', 't_title', 't_task_type', 't_task_date', 't_task_time','created_by', 'created_at']
    
# @admin.register(Poll)
# class ConnectPollAdmin(admin.ModelAdmin):
#     list_display = ['poll_id', 'question', 'option1', 'option2', 'created_by', 'created_at']

    
#----------------group start============================================================
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'created_at', 'created_by')  
    search_fields = ('name', 'created_by__username')  
    filter_horizontal = ('members',)  

admin.site.register(Group, GroupAdmin)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id','message_id', 'group_id', 'user_id', 'created_at')
    search_fields = ('text',)
    list_filter = ('group_id', 'user_id')
    
@admin.register(OneOffMeetingTable)
class OneOffMeetingTableAdmin(admin.ModelAdmin):
    list_display = ['id','meeting_id', 'meetingname', 'starttime', 'status', 'endtime', 'meeting_date', 'meeting_link', 'duration', 'location', 'description', 'additionalinfo', 'available_times', 'phone_numbers', 'created_by', 'created_at', 'display_emails']

    # Custom method to display emails in the list display
    def display_emails(self, obj):
        return ", ".join([email.email for email in obj.emails.all()])
    
    display_emails.short_description = 'Emails'
 
    
# @admin.register(OneOffMeetingTable)
# class OneOffMeetingTableAdmin(admin.ModelAdmin):
#      list_display = ['meeting_id', 'meetingname', 'starttime','status', 'endtime','meeting_date','meeting_link','duration','location','description','additionalinfo','available_times','phone_numbers', 'created_by', 'created_at']
        
    
@admin.register(MeetingPoll)
class MeetPollAdmin(admin.ModelAdmin):
     list_display = ['meeting_id', 'meetingname', 'starttime','status', 'endtime','meeting_date','meeting_link','duration','location','description','available_times','created_by', 'created_at']
        
    
class NoteAdmin(admin.ModelAdmin):
    list_display = ('note_id', 'title', 'created_by', 'category', 'created_at')  
    search_fields = ('title', 'description', 'category')  

    def created_by(self, obj):
        return obj.created_by.id  

    created_by.short_description = 'Creator ID'  

# Register the Note model with the custom admin class
admin.site.register(Note, NoteAdmin)



# class OneOffMeetingAdmin(admin.ModelAdmin):
#     list_display = ('meetingname', 'starttime', 'endtime', 'meeting_date', 'status', 'created_by','created_at')
#     # search_fields = ('meetingname', 'location', 'created_by__username')
#     # list_filter = ('status', 'meeting_date')
   

# admin.site.register(OneOffMeeting, OneOffMeetingAdmin)