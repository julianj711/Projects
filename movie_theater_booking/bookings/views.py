from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Seat, Booking
from rest_framework import viewsets
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from django.contrib.auth.decorators import login_required

#For CRUD operations on movies.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

#For seat availability and booking
class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

#For users to book seats and view their booking history
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

#cannot look at movie list without being logged in
@login_required
#Renders movie list 
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})

#Renders seat booking 
def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seats = Seat.objects.filter(movie=movie)
    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})

#Cannot book without being logged in
@login_required
#Confirms the booking
def confirm_booking(request, movie_id, seat_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seat = get_object_or_404(Seat, id=seat_id)
    seat.booked()
    Booking.objects.create(movie=movie, seat=seat, user=request.user)
    return redirect('booking_history')

#Renders booking history
def booking_history(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
    else:
        bookings = Booking.objects.none()
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})