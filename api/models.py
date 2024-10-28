from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class UserDeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_tokens')
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"
 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Document(models.Model):
    file = models.FileField(upload_to='uploads/') 
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    
class AudioRecording(models.Model):
    audio_file = models.FileField(upload_to='audio/recordings/') 
    uploaded_at = models.DateTimeField(auto_now_add=True) 
    record_by = models.ForeignKey(User, on_delete=models.CASCADE) 
    

    def __str__(self):
        return f"{self.record_by.username}'s recording - {self.uploaded_at}"
    
class Sketch(models.Model):
    file = models.FileField(upload_to='uploads/') 
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    
class Users(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=8)
    
    def __str__(self):
        return self.fullname
    
class SnapShot(models.Model):
    user_image = models.ImageField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    user_description = models.TextField(blank=True)
    others = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"user_image {self.id}"
    
class AllSnapShot(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image {self.id}"
    
class News(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image {self.id}"

    
class UserTask(models.Model):
    title = models.CharField(max_length=1000)
    task_id = models.AutoField(primary_key=True)
    task_type = models.CharField(max_length=30)
    task_date = models.CharField(max_length=50)
    task_time = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    note_link = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
         return self.title
     
class AllTask(models.Model):
    t_title = models.CharField(max_length=1000)
    t_task_id = models.AutoField(primary_key=True)
    t_task_type = models.CharField(max_length=30)
    t_task_date = models.CharField(max_length=50)
    t_task_time = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.t_title
    
class TaskCategory(models.Model):
    task_category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class WorkFlow(models.Model):
    title = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
     
class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    
    def __str__(self):
         return self.title
     
class ChatMessage(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    group_id = models.ForeignKey('Group', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

     
#====================== one-off-meeting model ================================================ 
class OneOffMeetingTable(models.Model):
    meeting_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    meetingname = models.CharField(max_length=50)
    starttime = models.CharField(max_length=50)
    endtime = models.CharField(max_length=50)
    meeting_date = models.CharField(max_length=50)
    duration = models.CharField(max_length=40)
    location = models.CharField(max_length=50)
    description = models.TextField()
    additionalinfo = models.CharField(max_length=2000)
    meeting_link = models.URLField(max_length=255, null=True, blank=True) 
    available_times = models.JSONField(default=dict)  # Store multiple time slots as a JSON object
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='scheduled')
    emails = models.ManyToManyField(User, related_name='meeting_emails', blank=True)  # Registered users' emails
    phone_numbers = models.JSONField(default=list, blank=True)  # Store multiple phone numbers
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    


    def __str__(self):
        return self.meetingname
    
class ScheduleMeetingBufferTimeSetting(models.Model):
    buffer_time = models.IntegerField(default=0)  # Store buffer time in minutes
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Global Settings - Buffer Time: {self.buffer_time} minutes"
    
#====================== meeting poll model ================================================

class MeetingPoll(models.Model):
    meeting_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    meetingname = models.CharField(max_length=50)
    starttime = models.CharField(max_length=50)
    endtime = models.CharField(max_length=50)
    meeting_date = models.CharField(max_length=50)
    duration = models.CharField(max_length=40)
    location = models.CharField(max_length=50)
    description = models.TextField()
    meeting_link = models.URLField(max_length=255, null=True, blank=True) 
    available_times = models.JSONField(default=dict)  # Store multiple time slots as a JSON object
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='scheduled')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meetingname  
    
class AllPolls(models.Model):
    p_poll_id = models.AutoField(primary_key=True)
    p_question = models.CharField(max_length=2000)
    p_option1 = models.TextField()
    p_option2 = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.p_question 
    
class Poll(models.Model):
    poll_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=2000)
    option1 = models.TextField()
    option2 = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.question 
    
#............................................ group section ......................................................................
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="created_groups", on_delete=models.CASCADE)
    
    # Set a unique related_name to avoid clashes with auth.User.groups
    members = models.ManyToManyField(User, related_name="custom_groups")

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="group_members", on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"
    
    
    
     
     

     
     
