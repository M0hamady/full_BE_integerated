from django.urls import path
from.views import ProfileClient, ProfileSiteEng, ProfileSiteEngProjects, ProfileSiteEngTasks, ProfileSiteEngTasksToday, ProfileSiteManager, ProfileSiteManagerProjects, ProfileView, check_viewer_uuid, delete_photo, finish_step, reply_feed, upload_photo

urlpatterns = [
    path('viewer/<uuid:uuid>/', check_viewer_uuid, name='check_viewer_uuid'),
    path('viewer/dash', ProfileView.as_view(), name='viewer_dash'),
    path('site-eng/dash/', ProfileSiteEng.as_view(), name='site_eng'),
    path('site-eng/dash/projects/', ProfileSiteEngProjects.as_view(), name='site_engProjects'),
    path('site-eng/client/profile/<int:client_id>', ProfileClient.as_view(), name='ProfileClient'),
    path('site-manager/dash/', ProfileSiteManager.as_view(), name='site_manager'),
    path('site-manager/dash/projects', ProfileSiteManagerProjects.as_view(), name='site_manager_projects'),
    path('floor/<int:floor_id>/tasks/', ProfileSiteEngTasks.as_view(), name='site_eng_tasks'),
    path('floor/tasks', ProfileSiteEngTasksToday.as_view(), name='site_eng_tasks_today'),
    path('upload_photo/<int:step_id>/', upload_photo, name='upload_photo'),
    path('delete_photo/<int:step_id>/', delete_photo, name='delete_photo'),
    path('site-manger/dash', ProfileSiteManager.as_view(), name='site_manger'),
    path('finish-step/<int:step_id>/', finish_step, name='finish_step'),
    path('feed/<int:feed_id>/reply/', reply_feed, name='reply_feed'),
]