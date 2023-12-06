from django.urls import path
from .views import ClientFilterView, Login, Meeting, Profile, add_ceiling_decorations, add_flooring_material, add_furniture_details, add_light_type, add_style, add_wall_decorations, delete_ceiling_decorations,delete_design, delete_color,Projects,add_color, RegisterView, ProfileProjectUpdateView, delete_flooring_material, delete_furniture_details, delete_light_type, delete_wall_decorations, design_styles, profile_update_view
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
    path('client/colors/delete/<uuid:project_uuid>/update/<int:color_uuid>', delete_color, name='delete_color'),
    path('client/style/update/<uuid:project_uuid>/<str:style_uuid>/', add_style, name='add_style'),
    path('client/design/delete/<uuid:project_uuid>/<int:style_id>/', delete_design, name='delete_design'),
    path('client/ceiling/update/<uuid:project_uuid>/<str:style_uuid>/', add_ceiling_decorations, name='add_ceiling_decorations'),
    path('client/ceiling/delete/<uuid:project_uuid>/<int:style_id>/', delete_ceiling_decorations, name='delete_ceiling_decorations'),
    path('client/light_type/update/<uuid:project_uuid>/<str:light_id>/', add_light_type, name='add_light_type'),
    path('client/light_type/delete/<uuid:project_uuid>/<int:light_id>/', delete_light_type, name='delete_light_type'),
    path('client/wall_decoration/update/<uuid:project_uuid>/<str:wall_id>/', add_wall_decorations, name='add_wall_decorations'),
    path('client/wall_decoration/delete/<uuid:project_uuid>/<int:wall_id>/', delete_wall_decorations, name='delete_wall_decorations'),
    path('client/flooring/update/<uuid:project_uuid>/<str:flooring_id>/', add_flooring_material, name='add_flooring_material'),
    path('client/flooring/delete/<uuid:project_uuid>/<int:flooring_id>/', delete_flooring_material, name='delete_flooring_material'),
    path('client/furniture/update/<uuid:project_uuid>/<str:furniture_id>/', add_furniture_details, name='add_furniture_details'),
    path('client/furniture/delete/<uuid:project_uuid>/<int:furniture_id>/', delete_furniture_details, name='delete_furniture_details'),
    path('designs/', design_styles, name='design_styles'),
    

]