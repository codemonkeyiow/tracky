from django.urls import path

from .views import *

urlpatterns = [
    path("", AllMeals.as_view(), name="index"),
    path("ingredients", Ingredients.as_view(), name="ingredients"),
    path("add-ingredient", AddIngredient.as_view(), name="add-ingredient"),
    path("meals", Meals.as_view(), name="meals"),
    path("all-meals", AllMeals.as_view(), name="all-meals"),
    path("drinks", Drinks.as_view(), name="drinks"),
]
