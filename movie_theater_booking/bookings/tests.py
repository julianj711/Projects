from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Movie, Seat, Booking
from datetime import date
from django.core.exceptions import ValidationError

class MovieModelTest(TestCase):
    
    #make sure that a movie can be created successfully
    def test_test_create_movie(self):
        movie = Movie.objects.create( 
            title = "The Sandlot",
            description = "Young baseball players during the Summer of 1962",
            release_date = date(1993, 4, 7),
            duration = 101
        )
        self.assertEqual(movie.title, "The Sandlot")

    #make sure that our __str__ returns the title
    def test_test_movie_str(self):
        movie = Movie.objects.create(
            title = "The Sandlot",
            description = "Young baseball players during the Summer of 1962",
            release_date = date(1993, 4, 7),
            duration = 101 
        )
        self.assertEqual(str(movie), "The Sandlot")
    
    #test the max title length
    def test_movie_title_max_len(self):
        long_title = "A" * 200
        movie = Movie.objects.create(
            title = long_title,
            description = "Test",
            release_date = date(1993, 4, 7),
            duration = 101
        )
        self.assertEqual(len(movie.title), 200)

    #make sure a long title fails
    def test_movie_title_over_max_len(self):
        movie = Movie(
            title = "A" * 201,
            description = "Test",
            release_date = date(1993, 4, 7),
            duration = 101
        )
        with self.assertRaises(ValidationError):
            movie.full_clean()

    #make sure a movie cant have a negative duration
    def test_negative_duration_movie(self):
        movie = Movie(
            title = "Bad Movie",
            description = "Test",
            release_date = date(1993, 4, 7),
            duration = -101
        )
        with self.assertRaises(ValidationError):
            movie.full_clean()

class SeatModelTest(TestCase):
    
    #make sure seat number with max len will fail
    def test_seat_number_max_len(self):
        seat = Seat(seat_number = "A" * 11)
        with self.assertRaises(ValidationError):
                seat.full_clean()

    #make sure an empty seat number will fail
    def test_empty_seat_number(self):
        seat = Seat(seat_number = "")
        with self.assertRaises(ValidationError):
                seat.full_clean()

    #test that seats are defaultly set to available
    def test_seat_default_status(self):
        seat = Seat.objects.create(seat_number = "A1")
        self.assertFalse(seat.booking_status)

    #test that a seat can be marked as booked
    def test_seat_booked_status(self):
        seat = Seat.objects.create(seat_number = "B2", booking_status=True)
        self.assertTrue(seat.booking_status)

    #test that booking a seat that is already taken should raise an error
    def test_unavailable_seat(self):
        seat = Seat.objects.create(seat_number = "A1", booking_status=True)
        with self.assertRaises(ValueError):
            seat.booked()

class BookingModelTest(TestCase):
    
    #Set up reusable objects for booking tests
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.movie = Movie.objects.create(
            title="The Sandlot",
            description="Young baseball players during the Summer of 1962",
            release_date=date(1993, 4, 7),
            duration=101
        )
        self.seat = Seat.objects.create(seat_number = "A1")

    #test that a booking can be created successfully
    def test_create_booking(self):
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
        self.assertEqual(booking.movie.title, "The Sandlot")
        self.assertEqual(booking.seat.seat_number, "A1")
    
    #deleting a movie deletes its bookings
    def test_booking_deleted_when_movie_deleted(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.movie.delete()
        self.assertEqual(Booking.objects.count(), 0)

    #deleting a seat deletes its bookings
    def test_booking_deleted_when_seat_deleted(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.seat.delete()
        self.assertEqual(Booking.objects.count(), 0)

class IntegrationTestingAPI(TestCase):
    
    #Set up reusable objects for tests
    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(
            title="The Sandlot",
            description="Young baseball players during the Summer of 1962",
            release_date=date(1993, 4, 7),
            duration=101
        )
        self.seat = Seat.objects.create(seat_number = "A1")

    #test that movies API returns 200
    def test_movies_api_returns_200(self):
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, 200)

    #test that seats API returns 200
    def test_seats_api_returns_200(self):
        response = self.client.get('/api/seats/')
        self.assertEqual(response.status_code, 200)

    #test that bookings API returns 200
    def test_bookings_api_returns_200(self):
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, 200)

    #make sure that creating a movie returns 201
    def test_create_movie(self):
        response = self.client.post('/api/movies/', {
            'title': 'Dune',
            'description': 'A sci-fi epic',
            'release_date': '2021-10-22',
            'duration': 155
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    #make sure a movie with no title returns 400
    def test_missing_title(self):
        response = self.client.post('/api/movies/', {
            'description': 'No title here',
            'release_date': '2026-2-17',
            'duration': 155
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    #make sure a movie that does not exist returns 404
    def test_nonexistent_movie(self):
        response = self.client.get('/api/movies/9999/')
        self.assertEqual(response.status_code, 404)

    #make sure the movie list page loads correctly
    def test_movie_list_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    #make sure the booking history page loads correctly
    def test_booking_history_page_loads(self):
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 200)

    #make sure you cant visit a seat booking page for a movie that isnt there
    def test_seat_booking_invalid_movie(self):
        response = self.client.get('/seat/9999/')
        self.assertEqual(response.status_code, 404)