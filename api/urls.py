from django.urls import path
from api.views import index, greet
urlpatterns=[
    path("", index),
    path("greet/", greet, name='greet' )
]