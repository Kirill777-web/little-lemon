from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('comments/', views.form_view, name='comments'),
    path('reservations/', views.reservations, name="reservations"),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('menu/', views.menu, name='menu'),
    path('menu_item/<int:pk>/', views.display_menu_items, name='menu_item'),
    path('bookings', views.bookings, name='bookings'),
]
