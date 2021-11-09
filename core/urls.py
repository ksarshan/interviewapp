from django.urls import path

from . import views

urlpatterns = [
    path('availability/', views.Availability.as_view(), name='availability'),
    path('schedule/', views.ScheduleTime.as_view(), name='get_schedule'),
]
