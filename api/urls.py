from django.urls import path
from .views import EplanApiView, create_group, search_users
from .views import Users
from .views import RegisterUser
from .views import LoginUser
from .views import CreateTaskMainView
from .views import CreateNote
from .views import CreateOneOffMeeting
from .views import MeetingDetailView
from .views import SelectMeetingTime
from .views import LatestMeetingView
from .views import CreatePoll
from .views import search_users
from .views import add_user_to_group
from .views import CreateMeetingPoll
from .views import PollLatestMeetingView
from .views import GetAllTaskView
from .views import TaskCategoryView
from .views import GetTaskCategoryView
from .views import DeleteTaskCategoryView
from .views import GetAllNoteView
from .views import GetGroupView
from .views import GetAllSnapShotView
from .views import AllSnapShotView
from .views import DocumentView
from .views import GetDocumentView
from .views import upload_sketch
from .views import GetSketchView
from .views import GetOneOffMeeting
from .views import upload_audio_recording
from .views import GetAudioRecordingView
from .views import GetGroupMembers
from .views import TaskSearchView
from .views import GetAllTaskById
from .views import GetAllNoteById
from .views import NoteSearchView
from .views import SetBufferTime
from .views import GetBufferView
from .views import CreateWorkFlowView
from .views import GetWorkFlowView
from .views import search_users_email
from .views import CreateChatMessage
from .views import GetChatMessageView
from .views import ProfileView
from .views import SaveFCMToken
from .views import GetProfileView
from .views import delete_message 
from .views import NewsView 
from .views import GetNewsView 
from .views import OneOffMeetingSearchView 
from .views import UpdateOneOffMeeting 
from .views import delete_task_category
from .views import PoolMeetingDetailView
from .views import NoteDetailView
from .views import LastCreatedNoteView


urlpatterns = [
    path('getnotlink/', LastCreatedNoteView.as_view(), name='last-created-note'),
    path('delete-task-category/<int:task_category_id>/', delete_task_category, name='delete_task_category'),
    path('meeting/<uuid:meeting_id>/', UpdateOneOffMeeting.as_view(), name='update-meeting'),  # Update URL for editing
    path('news/all-new/', GetNewsView.as_view(), name='news'),  # URL for deleting messages
    path('news/', NewsView.as_view(), name='news'),  # URL for deleting messages
    path('group/meeting/chatroom/<uuid:message_id>/', delete_message, name='delete_message'),  
    path('savePushNotificationToken/', SaveFCMToken.as_view(), name='user-token'),
    path('profile/get-profile/', GetProfileView.as_view(), name='user-profile'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('group/meeting/chatroom/get-all-chat/', GetChatMessageView.as_view(), name='get-chat-room'),
    path('group/meeting/chatroom/', CreateChatMessage.as_view(), name='chat-room'),
    path('setting/communication/get-workflow/', GetWorkFlowView.as_view(), name='workflow'),
    path('setting/communication/workflow/', CreateWorkFlowView.as_view(), name='workflow'),
    path('get-buffer/', GetBufferView.as_view(), name='buffer'),
    path('oneoffmeeting/seeting/buffer-setting/', SetBufferTime.as_view(), name='one-search-note'),
    path('oneoffmeeting/search-meeting/', OneOffMeetingSearchView.as_view(), name='search-one-off-meeting'),
    path('note/search-note/', NoteSearchView.as_view(), name='search-note'),
    path('note/get-note/<note_id>/', GetAllNoteById.as_view(), name='fetch-note-by-id'),
    path('task/get-task/<t_task_id>/', GetAllTaskById.as_view(), name='fetch-task-by-id'),
    path('task/search-task/', TaskSearchView.as_view(), name='search-task'),
    path('note/recent-captured/upload/audio-recording/get-recording/', GetAudioRecordingView.as_view(), name='get-audio-recording'),
    path('note/recent-captured/upload/audio-recording/', upload_audio_recording, name='audio-recording'),
    path('meeting/one-of-meeting/get/', GetOneOffMeeting.as_view(), name='get-oneOffMeeting'),
    path('user/upload/sketch/get-sketch-image/', GetSketchView.as_view(), name='get-sketch'),
    path('user/upload/sketch/', upload_sketch, name='upload-sketch'),
    path('user/upload/get-document/', GetDocumentView.as_view(), name='get-document'),
    path('user/upload/document/', DocumentView.as_view(), name='document'),
    path('snapshot/', AllSnapShotView.as_view(), name='snap-shot'),
    path('note/snapshot/getsnapshot/', GetAllSnapShotView.as_view(), name='get-snap-shot'),
    path('group/getgroup/', GetGroupView.as_view(), name='image-upload'),
    path('group/getgroupmembers/<group_id>/', GetGroupMembers.as_view(), name='image-upload'),
    path('task-category/delete/<str:name>/', DeleteTaskCategoryView.as_view(), name='delete-task-category-by-name'),  
    path('note/category/getnote/', GetAllNoteView.as_view(), name='get_note'),
    path('task/category/gettask/', GetTaskCategoryView.as_view(), name='get_task'),
    path('task/category/create/', TaskCategoryView.as_view(), name='get_task'),
    path('task/gettask/', GetAllTaskView.as_view(), name='get_task'),
    path('groups/create/add_user/', add_user_to_group, name='create_group'),
    path('groups/searchuser/', search_users, name='create_group'),
    path('groups/create/', create_group, name='create_group'),
    # path('groups/<int:group_id>/add-members/', add_group_members, name='add_group_members'),
    path('users/search/', search_users, name='search_users'),
    path('users/search-email/', search_users_email, name='search_users_email'),
    path('createpoll/', CreatePoll.as_view(), name='createpoll'),
    path('meetingpoll/lastest/', PollLatestMeetingView.as_view(), name='select-time-poll'),
    path('meetings/lastest/', LatestMeetingView.as_view(), name='select-time'),
    path('meetings/<uuid:meeting_id>/select_time/', SelectMeetingTime.as_view(), name='select-time'),
    path('poolmeetings/<uuid:meeting_id>/', PoolMeetingDetailView.as_view(), name='pool-meeting-detail'),
    path('meetings/<uuid:meeting_id>/', MeetingDetailView.as_view(), name='meeting-detail'),
    path('create_poll_meeting/', CreateMeetingPoll.as_view(), name='meetingpoll'),
    path('createoneoffmeeting/', CreateOneOffMeeting.as_view(), name='oneoffmeeting'),
    path('createNote/', CreateNote.as_view(), name='note'),
    path('notes/<int:note_id>/', NoteDetailView.as_view(), name='note-detail'),
    path('myTask/', CreateTaskMainView.as_view(), name='task'),
    path('registerUser/', RegisterUser.as_view(), name='RegisterUser'),
    path('loginUser/', LoginUser.as_view(), name='LoginUser'),
    path('Users/', Users.as_view(), name='Users'),
    path('check/', EplanApiView.as_view(), name='check'),
]