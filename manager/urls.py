from django.urls import path
from .views import ClientFilterView, Login, Meeting, Profile, add_style,delete_design, delete_color,Projects,add_color, RegisterView, ProfileProjectUpdateView, design_styles, profile_update_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", Profile.as_view(), name="profile"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('filter/<str:query1>/<str:query2>/', ClientFilterView.as_view(), name='client_filter'),
    path("projects/", Projects.as_view(), name="projects"),
    path("meetings/", Meeting.as_view(), name="meeting"),
    path('accounts/login/', Login.as_view(), name='login'),
    path("employee/register/", RegisterView.as_view(), name="register"),
    path('client/<uuid:client_uuid>/update/', profile_update_view, name='client_update'),
    path('client/project/<uuid:client_uuid>/update/', ProfileProjectUpdateView.as_view(), name='client_project_update'),
    path('client/colors/<uuid:project_uuid>/update/', add_color, name='add_color'),
    path('client/style/project<uuid:project_uuid>/update/style<str:style_uuid>/', add_style, name='add_style'),
    path('client/colors/delete/<uuid:project_uuid>/update/<int:color_uuid>', delete_color, name='delete_color'),
    path('client/design/delete/<uuid:project_uuid>/update/', delete_design, name='delete_design'),
    path('designs/', design_styles, name='design_styles'),
    

]