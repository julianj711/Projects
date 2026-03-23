from django.db import models
from django.core.validators import MinValueValidator

#stores movie details
class Movie(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.title

#track seat availability
class Seat(models.Model):
    #ForeignKey so that every seat is connected to a specific movie
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    seat_number =  models.CharField(max_length = 10)
    booking_status = models.BooleanField(default=False)
    
    #raises error if already booked
    def booked(self):
        if self.booking_status:
            raise ValueError("Seat is already booked")
        self.booking_status = True
        self.save()

#links a user, movie, and seat together
class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
