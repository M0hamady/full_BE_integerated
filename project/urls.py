
from .views import AllDataAPIView, CommentImageAPIView, CommentImageDetailAPIView, DesignColorsCreateAPIView, FeedbackAPIView, FeedbackDetailView, FeedbackListCreateView, ProjectBasicCreateAPIView, ProjectFileAPIView, ProjectFileDeleteAPIView, ProjectImageDeleteAPIView, ProjectImagesAPIView, ProjectStudyAPIView, ProjectStudyDetailView, ProjectStudyListCreateView, ProjectUploadAPIView, ReplyDetailView, ReplyListCreateView, client_dash_home_data, create_comment, create_comment_options, create_comment_project_image_2d, create_notes, create_project_image_by_uuid, create_project_study, create_project_study_feeds, create_project_study_feeds_reply, feedback_exact_floor_view, feedback_floor_view, get_comments_by_image_and_client, get_project_image_by_uuid, get_project_image_with_comments, get_project_study, handle_form_submission, project_basic_retrieve, update_basic_project, update_can_sea, update_can_sea_file, update_client_approved, update_file, upload_file
from django.urls import path



urlpatterns = [
    path('basic-data/', AllDataAPIView.as_view(), name='project_basic_data'),
    path('data/<uuid:viewer_uuid>/', project_basic_retrieve, name='project-basic'),
    path('2d/<uuid:client_uuid>/', get_project_image_by_uuid, name='get_project_image_by_uuid'),
    path('2d/create/<uuid:client_uuid>/', create_project_image_by_uuid, name='create_project_image_by_uuid'),
    path('2d/comment/create/<uuid:project_image_uuid>/<uuid:client_uuid>/', create_comment_project_image_2d, name='create_comment_project_image_2d'),
    path('2d/comments/<uuid:project_image_uuid>/<uuid:client_uuid>/', get_project_image_with_comments, name='get_project_image_with_comments'),
    path('projects/', ProjectBasicCreateAPIView.as_view(), name='project-create'),
    path('update-basic-project/<str:viewer_uuid>', update_basic_project, name='project-basic-update'),
    path('upload/', ProjectUploadAPIView.as_view(), name='project-upload'),
    path('files/', ProjectFileAPIView.as_view(), name='project-files'),
    path('form-submission/', handle_form_submission, name='form-submission'),
    path('upload-file/', upload_file, name='upload-file'),
    path('update-file/', update_file, name='update_file'),
    path('images/', ProjectImagesAPIView.as_view(), name='project-images'),
    path('image/update-can-sea/<uuid:uuid>/', update_can_sea,name='update_can_sea'),
    path('file/update-can-sea/<uuid:uuid>/', update_can_sea_file,name='update_can_sea_file'),
    path('project/update-approvement/<uuid:uuid>/', update_client_approved,name='update_clients_approvement'),
    path('delete/files/', ProjectFileDeleteAPIView.as_view(), name='delete-project-file'),
    path('delete/image/', ProjectImageDeleteAPIView.as_view(), name='delete-project-image'),
    path('design-colors/create/', DesignColorsCreateAPIView.as_view(), name='design-colors-create'),
    path('images/comments/', CommentImageAPIView.as_view(), name='comment-image-list-create'),
    path('feedbackfloors/', feedback_floor_view, name='feedbackfloor-list'),
    path('feedbackfloors/<uuid:floor_uuid>/', feedback_exact_floor_view, name='feedbackfloor-list'),
    path('client_dash_home_data/<uuid:client_uuid>/', client_dash_home_data, name='client_dash_home_data'),
    path('api/comments/', get_comments_by_image_and_client, name='get_comments_by_image_and_client'),
    path('image/comments/<uuid:uuid>/', CommentImageDetailAPIView.as_view(), name='comment-image-detail'),
    path('comments/create/', create_comment, name='create_comment'),
    path('project-basic/create-notes/', create_notes ,name='notes-create'),
    path('project-basic/create-comment-options/<uuid:uuid>/', create_comment_options ,name='comment-create'),
    ##############################
    path('project-studies/', ProjectStudyListCreateView.as_view(), name='project-study-list'),
    path('project-studies/<int:pk>/', ProjectStudyDetailView.as_view(), name='project-study-detail'),
    path('feedbacks/', FeedbackListCreateView.as_view(), name='feedback-list'),
    path('feedbacks/<int:pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),
    path('api/feedback/', FeedbackAPIView.as_view(), name='feedback-api'),
    path('project-studies_feeds/<str:project_study_uuid>/', ProjectStudyAPIView.as_view(), name='project-study-api'),
    path('replies/', ReplyListCreateView.as_view(), name='reply-list'),
    path('replies/<int:pk>/', ReplyDetailView.as_view(), name='reply-detail'),
     path('create-study/<str:tech_uuid>/', create_project_study, name='create_project_study'),
     path('create-study-feeds/<str:tech_uuid>/', create_project_study_feeds, name='create_project_study'),
     path('create-study-feeds-reply/<str:tech_uuid>/', create_project_study_feeds_reply, name='create_project_study'),
     path('get-study/<str:tech_uuid>/', get_project_study, name='get_project_study'),
    
]