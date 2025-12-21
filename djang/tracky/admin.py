from django.contrib import admin

from .models import *

admin.site.register(Ingredient)
admin.site.register(Meal)
admin.site.register(RecipeIngredient)
admin.site.register(Recipe)
admin.site.register(MealRecipe)
admin.site.register(MealIngredient)
admin.site.register(BloodPressure)
admin.site.register(Weight)
admin.site.register(Drink)
admin.site.register(Sleep)
admin.site.register(Mood)
admin.site.register(Exercise)
