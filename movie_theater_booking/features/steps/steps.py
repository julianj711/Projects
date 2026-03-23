from behave import given, when, then 
from django.test import Client
from bookings.models import Movie, Seat, Booking
from django.contrib.auth.models import User
from datetime import date

@given('I am on the login page')
def login_page(context):
    context.client = Client()

@when('I enter valid credentials')
def valid_credentials(context):
    User.objects.create_user(username="testuser", password="password")
    context.response = context.client.post('/login/', {
        'username': 'testuser',
        'password': 'password'
    })

@then('I should be redirected to the movie listing page')
def redirected_to_moive_list_page(context):
    assert context.response.status_code == 302

@when('I enter invalid credentials')
def invalid_credentials(context):
    context.response = context.client.post('/login/', {
        'username': 'wronguser',
        'password': 'wrongpassword'
    })

@then('I should see a login error')
def login_error(context):
    assert b'Please enter a correct username and password' in context.response.content

@given('there are movies in the database')
def movies_in_database(context):
    context.client = Client()
    context.movie = Movie.objects.create(
        title = "The Sandlot",
        description = "Young baseball players during the Summer of 1962",
        release_date = date(1993, 4, 7),
        duration = 101 
        )

@when('I navigate to the movie listing page')
def movie_listing_page(context):
    context.response = context.client.get('/')

@then('I should see a 200 status code')
def status_code_200(context):
    assert context.response.status_code == 200

@when('I navigate to the seat booking page')
def seat_booking_page(context):
    context.response = context.client.get(f'/seat/{context.movie.id}/')

@given('I am in the app')
def in_the_app(context):
    context.client = Client()

@when('I navigate to the booking history page')
def booking_history(context):
    context.response = context.client.get('/history/')


@given('there is an available seat')
def available_seat(context):
    context.seat = Seat.objects.create(seat_number="A1", booking_status=False)

@given('I am logged in')
def step_logged_in(context):
    context.user = User.objects.create_user(username="testuser", password="password")
    context.client.login(username="testuser", password="password")

@when('I book the seat')
def book_seat(context):
    context.seat.booked()

@then('the seat should be marked as booked')
def seat_marked_as_booked(context):
    context.seat.refresh_from_db()
    assert context.seat.booking_status == True

@given('there is an unavailable seat')
def unavailable_seat(context):
    context.seat = Seat.objects.create(seat_number="B2", booking_status=True)
    context.error = None

@when('I choose a seat that is unavailable')
def choose_unavailable_seat(context):
    context.raised_error = False
    if context.seat.booking_status:
        context.raised_error = True

@then('I should see a seat already booked error')
def seat_booked_error(context):
    assert context.raised_error == True