from django.urls import path
from api.views import index, greet, schedule
urlpatterns=[
    path("", index),
    path("greet/", greet, name='greet' ),
    path('schedule', schedule, name='schedule')
]