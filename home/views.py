from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import EventSerializers,RegisterSerializer,LoginSerializer,BookingSerializer,TicketBookingSerializer
from .models import Event,Booking
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .permission import IsAdminUser
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from django.db.models import Q


class RegisterView(APIView):
    
    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":True,
                "message":"User is Registered Successfully..."
            })
        return Response({
            "status":False,
            "message":serializer.errors
        })
    

class LoginView(APIView):

    def post(self,request):
        data = request.data 
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = authenticate(username = serializer.validated_data['username'],
                                password = serializer.validated_data['password']
                                )
            if user:
                token,created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "status":True,""
                        "message":"User Logged in successfully..",
                        "Token":token.key
                    }
                )
            return Response({
                "status":False,
                "message":"Invvalid Credentials.."
            })
        return Response({
            "status":False,
            "message":serializer.errors
        })

class PublicEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializers 
    http_method_names = ["get"]

    @action(detail=False,methods=['GET'])
    def search_events(self,request):
        search = request.GET.get('search')
        events = Event.objects.filter( Q(title__icontains=search) | Q(description__icontains=search))
        serializer = EventSerializers(events,many=True)
        return Response({
            "status":True,
            "message":"Events Fetched",
            "data":serializer.data
        })


class PrivateEventViewSet(viewsets.ModelViewSet):
    permission_classes =  [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    queryset = Event.objects.all()
    serializer_class = EventSerializers

class BookViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False,methods=["GET"])
    def get_booking(self,request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings,many=True)
        print(request.user)
        print(type(request.user))
        print(request.user.id)
        return Response({
            "status":True,
            "message":"Booking fetched",
            "data":serializer.data
        })

    @action(detail=False,methods=["POST"])
    def create_booking(self,request):
        data = request.data 
        serializer = TicketBookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":True,
                "message":'Booking Created',
                "data":serializer.data
            })
        return Response({
            "status":False,
            "message":"Booking not created",
            "data":serializer.errors
        })