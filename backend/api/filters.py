from django_filters import rest_framework as filters
from .models import Event, Place, Comment, Rating, MessagesUsers, User

class EventFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    place_name = filters.CharFilter(field_name='place__name', lookup_expr='icontains')
    user = filters.CharFilter(field_name='user__username', lookup_expr='exact')

    class Meta:
        model = Event
        fields = ['name', 'description', 'place_name', 'user']


class PlaceFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    street = filters.CharFilter(lookup_expr='icontains')
    locality = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Place
        fields = ['name', 'street', 'locality']

class CommentFilter(filters.FilterSet):
    
    place = filters.CharFilter(field_name='place__id', lookup_expr='icontains')

    class Meta:
        model = Comment
        fields = ['place']

class RatingFilter(filters.FilterSet):

    place = filters.CharFilter(field_name='place__id', lookup_expr='icontains')
    rated_by = filters.CharFilter(field_name='rated_by__id', lookup_expr='icontains')
    
    class Meta:
        model = Rating
        fields = ['place', 'rated_by']

class MessagesUsersFilter(filters.FilterSet):
    
    sender = filters.NumberFilter(field_name='sender__id', lookup_expr='exact')
    receiver = filters.NumberFilter(field_name='receiver__id', lookup_expr='exact')
    
    class Meta:
        model = MessagesUsers
        fields = ['sender', 'receiver']

class UsersFilter(filters.FilterSet):
    id = filters.CharFilter(lookup_expr='icontains')
    username = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = User
        fields = ['username', 'id']
