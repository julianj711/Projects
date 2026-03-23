from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

#Creating api endpoints 
router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'seats', views.SeatViewSet)
router.register(r'bookings', views.BookingViewSet)

#Creating URL routes
urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("seat/<int:movie_id>/", views.seat_booking, name="book_seat"),
    path("history/", views.booking_history, name="booking_history"),
    path("api/", include(router.urls)),
    path("confirm/<int:movie_id>/<int:seat_id>/", views.confirm_booking, name="confirm_booking"),
] 