
from django.urls import path
from .views import *

urlpatterns = [
    path('login', Login.as_view(), name='user-login'),
    path('user/', Createuser.as_view(),name="create_user"),
    path('data/', LoginView.as_view(),name="login-view"),
    path('events', Notes.as_view(), name='events'), 
    path('logout', Logout.as_view(), name='user-logout'),
    path('edit/<int:pk>/', Edit.as_view(), name='edit'),
    path('delete/<int:pk>/', Edit.as_view(), name='delete'),
    path('create', CreatePost.as_view(), name='create'),




]