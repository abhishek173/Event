from rest_framework import serializers
from home.models import Event,Booking,Ticket
from django.contrib.auth.models import User


class EventSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

class TicketBookingSerializer(serializers.Serializer):
    event = serializers.IntegerField()
    ticket_type = serializers.CharField()
    total_person = serializers.IntegerField()
    user = serializers.IntegerField()

    def validate_event(self,value):
        if not Event.objects.filter(id=value,status="Happening").exists():
            raise serializers.ValidationError("Event does not Exists..")
        return value

    def validate_user(self,value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exists..")
        return value
    
    def create(self,validated_data):
        event = Event.objects.get(id=validated_data['event'])
        user = User.objects.get(id=validated_data['user'])  
        ticket = Ticket.objects.create(event=event,ticket_type=validated_data['ticket_type'],total_person=validated_data['total_person'])
        total_person = validated_data['total_person']
        total_price = event.ticket_price * total_person
        booking = Booking.objects.create(ticket=ticket,user=user,status="Confirmed",total_price=total_price)
        return {
            "event":event.id,
            "ticket_type":ticket.ticket_type,
            "total_person":total_person,
            "user":user.id   
        }
    