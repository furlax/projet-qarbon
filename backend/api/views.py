from django.contrib.auth.models import User, Group
from django.views.decorators.cache import never_cache
from rest_framework import viewsets, permissions
from .models import Message
from django.views.generic import TemplateView
from .serializers import UserSerializer, GroupSerializer, MessageSerializer, WaitListSerializer, MessagesUsersSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .models import Event, Place, Rating, Comment, Waitlist, MessagesUsers
from .serializers import EventSerializer, PlaceSerializer,  RatingSerializer, CommentSerializer
from .filters import EventFilter, PlaceFilter, CommentFilter, RatingFilter, MessagesUsersFilter, UsersFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
# Email
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from smtplib import SMTPException
import traceback
from django.db.models import Q




# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = UsersFilter

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        current_user = request.user
        messages = MessagesUsers.objects.filter(
            Q(sender=current_user, sender_deleted=False) | Q(receiver=current_user, receiver_deleted=False)
        ).order_by('timestamp')
        serializer = MessagesUsersSerializer(messages, many=True)
        return Response(serializer.data)
    

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # SHOULD IMPLEMENT CUSTOM PERMISSIONS FOR OBJECT LEVEL SECURITY

class PlaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows places to be viewed or edited.
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filterset_class = PlaceFilter
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        user = request.user
        place = self.get_object()  # Utiliser la méthode get_object() pour obtenir l'objet place
        serializer = CommentSerializer(data=request.data)  # Utiliser le serializer pour valider les données
        if serializer.is_valid():
            serializer.save(user=user, place=place)  # Enregistrer le commentaire si les données sont valides
            return Response({'status': 'Comment added successfully'})
        return Response({'status': 'Comment could not be added'})

    @action(detail=True, methods=['post'])
    def add_rating(self, request, pk=None):
        user = request.user
        place = self.get_object()
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            # Assurez-vous que l'utilisateur n'a pas déjà noté cette place
            if not Rating.objects.filter(place=place, rated_by=user).exists():
                serializer.save(rated_by=user, place=place)  # Enregistrer la notation si les données sont valides
                return Response({'status': 'Rating added successfully'})
            else:
                return Response({'status': 'User has already rated this place'})
        return Response({'status': 'Rating could not be added'})
        

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    # SHOULD IMPLEMENT CUSTOM PERMISSIONS FOR OBJECT LEVEL SECURITY
    
    # Ajoute auto le user authentifié comme user de l'event
    def perform_create(self, serializer):
        print("Serializer validated data:", serializer.validated_data)
        serializer.save(user=self.request.user)

    # Register the user to the event
    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        user = request.user

        # Check if the user is already registered
        if event.participants.filter(pk=user.pk).exists():
            return Response({'status': 'User already registered for the event'})
        
        # Check if user is already on the waitlist
        if Waitlist.objects.filter(event=event, user=user).exists():
            return Response({'status': 'User already on the waiting list'})

        if event.is_full():
            Waitlist.objects.create(user=user, event=event)
            return Response({'status': 'Event is full, user added to waiting list'})
        else:
            event.participants.add(user)
            event.save()
            return Response({'status': 'User registered for the event'})
    
    @action(detail=True, methods=['delete'])
    def unregister(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        user = request.user
        event.participants.remove(user)
        event.save()
        waiting_list = Waitlist.objects.filter(event=event).order_by('created_at').first() 
        if waiting_list:
            event.participants.add(waiting_list.user)
            event.save()
            waiting_list.delete()
            return Response({'status': 'User unregistered from the event, and first user on waiting list registered'})
        else:
            return Response({'status': 'User unregistered from the event'})
        
    @action(detail=True, methods=['get'])
    def isUserOnWaitingList(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        user = request.user
        waiting_list = Waitlist.objects.filter(event=event, user=user).exists()
        return Response({'status': waiting_list})
    
    @action(detail=True, methods=['post'])
    def send_notification(self, request, pk=None):
        subject = request.data.get('subject')
        message = request.data.get('message')

        email_from = settings.EMAIL_HOST_USER

        # Get the list of recipients
        event = self.get_object()
        recipient_list = [participant.email for participant in event.participants.all() if participant.email]

        # Send email
        print("Recipient list:", recipient_list)
        print(email_from)
        if recipient_list:
            try:
                send_mail(subject, message, email_from, recipient_list)
            except SMTPException:
                print("Failed to send email. Exception: ", e)
                traceback.print_exc()


        return Response({'status': 'Attempted to send emails'}, status=status.HTTP_200_OK)


class MyEventsViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        user = self.request.user  
        return Event.objects.filter(user=user) 


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_class = CommentFilter



class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ratings to be viewed or edited.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filterser_class = RatingFilter

class WaitlistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows waitlists to be viewed or edited.
    """
    queryset = Waitlist.objects.all()
    serializer_class = WaitListSerializer
    # filterset_class = WaitlistFilter

class MessagesUsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = MessagesUsers.objects.all()
    serializer_class = MessagesUsersSerializer
    filterset_class = MessagesUsersFilter

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        receiver = User.objects.get(pk=pk)
        sender = request.user
        content = request.data.get('content')
        if not content:
            return Response({'status': 'Message content cannot be empty'})
        MessagesUsers.objects.create(sender=sender, receiver=receiver, content=content)
        return Response({'status': 'Message sent successfully'})
    
    @action(detail=False, methods=['get'])
    def messages(self, request):
        current_user = request.user
        messages = MessagesUsers.objects.filter(
            Q(sender=current_user) | Q(receiver=current_user)
        ).order_by('timestamp')
        serializer = MessagesUsersSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'])
    def delete_messages(self, request, pk=None):
        receiver = User.objects.get(pk=pk)
        current_user = request.user
        conversation = MessagesUsers.objects.filter(
            Q(sender=current_user, receiver=receiver) | Q(sender=receiver, receiver=current_user)
        )
        if conversation.exists():
            for message in conversation:
                if message.sender == current_user:
                    message.sender_deleted = True
                elif message.receiver == current_user:
                    message.receiver_deleted = True
                message.save()
            return Response({'status': 'Conversation marked as deleted successfully'})
        else:
            return Response({'status': 'Conversation could not be found or you do not have permission to delete this conversation'}, status=status.HTTP_404_NOT_FOUND)



# def get_recipient_list(event_id):
#     # Assuming Event model has a related name 'participants' to User model
#     event = Event.objects.get(pk=event_id)
#     return [participant.email for participant in event.participants.all()]

# class SendEventNotificationView(viewsets.ModelViewSet):
#     """
#     API View for sending event notifications
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self, request, *args, **kwargs):
#         subject = request.data.get('subject')
#         message = request.data.get('message')
#         event_id = request.data.get('event_id')  # Get the event ID from the request data

#         email_from = settings.EMAIL_HOST_USER

#         # Get the list of recipients
#         recipient_list = get_recipient_list(event_id)

#         # Send email
#         send_mail(subject, message, email_from, recipient_list)

#         return Response({'status': 'email sent'}, status=status.HTTP_200_OK)



@api_view(['GET'])
def is_authenticated(request):
    auth = JWTAuthentication()
    try:
        auth.get_validated_token(raw_token=request.COOKIES.get('jwt-app-auth'))
        return Response({'is_authenticated': True})
    except:
        return Response({'is_authenticated': False})
@api_view(['GET'])
def api_overview(request):
    api_urls = {
        "messages": "http://127.0.0.1:8000/api/messages/",
        "users": "http://127.0.0.1:8000/api/users/",
        "groups": "http://127.0.0.1:8000/api/groups/",
        "events": "http://127.0.0.1:8000/api/events/",
        "places": "http://127.0.0.1:8000/api/places/",
        "is_authenticated": "http://127.0.0.1:8000/api/dj-rest-auth/is_authenticated/",
    }
    return Response(api_urls)