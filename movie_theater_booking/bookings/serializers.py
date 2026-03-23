from rest_framework import serializers
from .models import Movie, Seat, Booking

#Converts Movie model data to JSON format
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

#Converts Seat model data to JSON format
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

#Converts Booking model data to JSON format
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'