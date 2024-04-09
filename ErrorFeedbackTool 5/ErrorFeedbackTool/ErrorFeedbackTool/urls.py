"""ErrorFeedbackTool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('', RedirectView.as_view(url='/login/')),
    path('Admin_home/',views.Admin_home, name="Admin_home"),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration, name='registration'),
    path('Admin_download/', views.Admin_download, name='Admin_download'),
    path('SuperAdmin_user/', views.SuperAdmin_user, name='SuperAdmin_user'),
    path('SuperAdmin_home/', views.SuperAdmin_home, name='SuperAdmin_home'),
    path('SuperAdmin_download/', views.SuperAdmin_download, name='SuperAdmin_download'),
    path('role/', views.role, name='role'),
    path('SuperAdmin_project/', views.SuperAdmin_project, name='SuperAdmin_project'),
    path('Admin_project/', views.Admin_project, name='Admin_project'),
    path('create_project/', views.create_project, name='create_project'),
    path('default/', views.default, name='default'),
    path('default_download/', views.default_download, name='default_download'),
    path('center_management/', views.center, name='center_management'),
    path('create_project/new_page', views.new_page_view, name='new_page'), 
    path('feedback', views.feedback, name='feedback'), 
    path('acknowledge', views.acknowledge, name='acknowledge'), 
    path('add_admin', views.add_admin, name='add_admin'), 
    path('add_user', views.add_user, name='add_user'), 
    path('delete_user', views.delete_user, name='delete_user'), 

    path('database_view/', views.database_view, name='database_view'),
    path('database/search/', views.database_view, name='database_search'),
    path('update_status/', views.update_status, name='update_status'),
    path('update_status_reject/', views.update_status_reject, name='update_status_reject'),
    path('view_screenshot/<int:error_id>/', views.view_screenshot, name='view_screenshot'),
    path('error_data_view/', views.error_data_view, name='error_data_view'),
    path('Admin_user/', views.Admin_user, name='Admin_user'),
    path('images/<str:image_name>/', views.image_view, name='image_url_name'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('change_password/', views.change_password, name='change_password'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

