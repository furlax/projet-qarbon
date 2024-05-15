"""djangoHeroku URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers 
from .api.views import index_view, UserViewSet, GroupViewSet, MessageViewSet, EventViewSet, PlaceViewSet, is_authenticated, RatingViewSet, CommentViewSet, MyEventsViewSet, WaitlistViewSet, MessagesUsersViewSet
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter()
router.register('messages', MessageViewSet)
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)
router.register('events', EventViewSet)
router.register('places', PlaceViewSet)
router.register('comments', CommentViewSet)
router.register('ratings', RatingViewSet)
router.register('myevents', MyEventsViewSet, basename='myevents')
router.register('waitlist', WaitlistViewSet, basename='waitings')
router.register('messagesusers', MessagesUsersViewSet, basename='waitings')



urlpatterns = [
    
    path('', index_view, name='index'),
    path('api/', include(router.urls)),
    path('api/events/<int:pk>/register/', EventViewSet.register, name='register_event'),
    path('api/events/<int:pk>/unregister/', EventViewSet.unregister, name='unregister_event'),
    path('api/events/<int:pk>/isUserOnWaitingList/', EventViewSet.isUserOnWaitingList, name='isUserOnWaitingList'),
    path('api/places/<int:pk>/add_comment/', PlaceViewSet.add_comment, name='add_comments'),
    path('api/places/<int:pk>/add_rating/', PlaceViewSet.add_rating, name='add_ratings'),
    path('api/messagessusers/<int:pk>/send_message/', MessagesUsersViewSet.send_message, name='sending_message'),
    path('api/messagesusers/messages/', MessagesUsersViewSet.messages, name='get_messages'),
    path('api/messagesusers/<int:pk>/delete_messages/', MessagesUsersViewSet.delete_messages, name='delete_msg'),
    path('api/explorer/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/dj-rest-auth/is_authenticated/', is_authenticated),
    path('api/admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
