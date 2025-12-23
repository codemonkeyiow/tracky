import logging

# from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView

from tracky.forms import *
from tracky.models import *

logger = logging.getLogger(__name__)


class Index(TemplateView):
    template_name = 'tracky/index.html'

    def get(self, request):
        logger.warning('hmm')
        return render(
            request,
            self.template_name,
            {
                'meals': Meal.objects.all(),
            },
        )

class Ingredients(TemplateView):
    template_name = 'tracky/ingredients.html'

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                'ingredients': Ingredient.objects.all(),
            }
        )

class AddIngredient(TemplateView):
    template_name = 'tracky/add-ingredient.html'

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                'form': IngredientForm()
            }
        )

class Meals(TemplateView):
    template_name = 'tracky/meals.html'

    def get(self, request):
        today_meals = Meal.objects.filter(on__date=timezone.now().date()).order_by("on")
        today_calories = today_sodium = today_magnesium = today_potassium = 0
        today_protein = today_fat = today_fibre = today_sugar = today_carbs = 0
        for meal in today_meals:
            today_calories = today_calories + meal.get_calories()
            today_sodium = today_sodium + meal.get_sodium()
            today_magnesium = today_magnesium + meal.get_magnesium()
            today_potassium = today_potassium + meal.get_potassium()
            today_protein = today_protein + meal.get_protein()
            today_fat = today_fat + meal.get_fat()
            today_fibre = today_fibre + meal.get_fibre()
            today_carbs = today_carbs + meal.get_carbs()
            today_sugar = today_sugar + meal.get_sugar()

        return render(
            request,
            self.template_name,
            {
                'meals': Meal.objects.all(),
                'today': today_meals,
                'today_calories': today_calories,
                'today_potassium': today_potassium,
                'today_magnesium': today_magnesium,
                'today_sodium': today_sodium,
                'today_protein': today_protein,
                'today_fat': today_fat,
                'today_fibre': today_fibre,
                'today_sugar': today_sugar,
                'today_carbs': today_carbs,
            },
        )

class AllMeals(TemplateView):
    template_name = 'tracky/all-meals.html'

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                'meals': Meal.objects.order_by("-on"),
            },
        )


class Drinks(TemplateView):
    template_name = 'tracky/drinks.html'

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                'drinks': Drink.objects.order_by("-start"),
            },
        )
