from django.urls import path

from .views import *

urlpatterns = [
    path("", AllMeals.as_view(), name="index"),
    path("meals", Meals.as_view(), name="meals"),
    path("all-meals", AllMeals.as_view(), name="all-meals"),
    path("drinks", Drinks.as_view(), name="drinks"),
]
