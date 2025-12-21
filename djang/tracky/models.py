from decimal import Decimal

from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy
# from django.db.models.functions import Now

import logging
logger = logging.getLogger(__name__)


class Ingredient(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True)
    grams = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("100"),
        verbose_name = "Grams"
    )
    calories = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Calories"
    )
    protein = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "protein"
    )
    fat = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Fat"
    )
    saturated_fat = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Sat. Fat"
    )
    trans_fat = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Trans Fat"
    )
    fibre = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Fibre"
    )
    sugar = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Sugar"
    )
    carbs = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Carbs"
    )
    salt = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Salt"
    )
    sodium = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Sodium (not from NaCl)"
    )
    potassium = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Potassium"
    )
    magnesium = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Magnesium"
    )
    calcium = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Calcium"
    )
    iron = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Iron"
    )
    vitamin_D = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("0"),
        verbose_name = "Vit. D"
    )

    def __str__(self):
        return f"{self.name} - {self.grams}g"


class Recipe(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def __sum(self, field: str) -> Decimal:
        """
        Generic nutrient aggregator.
        Assumes ingredient values are per 100g.
        """
        total = Decimal("0")
        qs = self.recipeingredient_set.select_related("ingredient")
        for ri in qs:
            ing = ri.ingredient
            if ing.grams == 0:
                continue
            value_per_g = getattr(ing, field) / ing.grams
            total += value_per_g * ri.grams
        return total
    
    # Nutrient accessors
    def calories(self):
        return self.__sum("calories")

    def protein(self):
        return self.__sum("protein")

    def fat(self):
        return self.__sum("fat")

    def carbs(self):
        return self.__sum("carbs")

    def fibre(self):
        return self.__sum("fibre")

    def sugar(self):
        return self.__sum("sugar")
    
    def salt(self):
        return self.__sum("salt")

    def sodium(self):
        # returns grams of sodium
        return self.__sum("sodium")

    def sodium_mg(self):
        return self.sodium() * Decimal("1000")
    
    def potassium(self):
        return self.__sum("potassium")
    
    def magnesium(self):
        return self.__sum("magnesium")


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    grams = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("100"),
        verbose_name = "Grams"
    )

    def __str__(self):
        return f"{self.recipe.name} - {self.ingredient.name} {self.grams}g"


class Meal(models.Model):
    on = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.on.day}/{self.on.month}/{self.on.year} {self.on.hour}:{self.on.minute}"
    
    def get_time(self):
        return f"{self.on.hour}:{self.on.minute}"
    
    def __sum(self, field: str) -> Decimal:
        """
        Generic nutrient aggregator.
        Assumes ingredient values are per 100g.
        """
        total = Decimal("0")
        qs = self.mealingredient_set.select_related("ingredient")
        for mi in qs:
            ing = mi.ingredient
            if ing.grams == 0:
                continue
            value_per_g = getattr(ing, field) / ing.grams
            total += value_per_g * mi.grams

        qs = self.mealrecipe_set.select_related("ingredient")
        # TODO
        return total
    
    def calories(self):
        return self.__sum("calories")


    def get_calories(self):
        calories = 0
        for mr in self.mealrecipe_set.all():
            calories = calories + mr.recipe.calories()
        for mi in self.mealingredient_set.all():
            calories = calories + mi.get_calories()
        return calories

    def get_sodium(self):
        sodium = 0
        for mr in self.mealrecipe_set.all():
            sodium = sodium + mr.recipe.sodium()
        for mi in self.mealingredient_set.all():
            sodium = sodium + (((mi.ingredient.sodium / mi.ingredient.grams) * mi.grams) * 1000)
        return sodium

    def get_potassium(self):
        potassium = 0
        for mr in self.mealrecipe_set.all():
            potassium = potassium + mr.recipe.potassium()
        for mi in self.mealingredient_set.all():
            potassium = potassium + (((mi.ingredient.potassium / mi.ingredient.grams) * mi.grams) * 1000)
        return potassium

    def get_magnesium(self):
        magnesium = 0
        for mr in self.mealrecipe_set.all():
            magnesium = magnesium + mr.recipe.magnesium()
        for mi in self.mealingredient_set.all():
            magnesium = magnesium + (((mi.ingredient.magnesium / mi.ingredient.grams) * mi.grams) * 1000)
        return magnesium
    
    def get_protein(self):
        protein = 0
        for mr in self.mealrecipe_set.all():
            protein = protein + mr.recipe.protein()
        for mi in self.mealingredient_set.all():
            protein = protein + ((mi.ingredient.protein / mi.ingredient.grams) * mi.grams)
        return protein
    
    def get_fat(self):
        fat = 0
        for mr in self.mealrecipe_set.all():
            fat = fat + mr.recipe.fat()
        for mi in self.mealingredient_set.all():
            fat = fat + ((mi.ingredient.fat / mi.ingredient.grams) * mi.grams)
        return fat
    
    def get_fibre(self):
        fibre = 0
        for mr in self.mealrecipe_set.all():
            fibre = fibre + mr.recipe.fibre()
        for mi in self.mealingredient_set.all():
            fibre = fibre + ((mi.ingredient.fibre / mi.ingredient.grams) * mi.grams)
        return fibre
    
    def get_carbs(self):
        carbs = 0
        for mr in self.mealrecipe_set.all():
            carbs = carbs + mr.recipe.carbs()
        for mi in self.mealingredient_set.all():
            carbs = carbs + ((mi.ingredient.carbs / mi.ingredient.grams) * mi.grams)
        return carbs
    
    def get_sugar(self):
        sugar = 0
        for mr in self.mealrecipe_set.all():
            sugar = sugar + mr.recipe.sugar()
        for mi in self.mealingredient_set.all():
            sugar = sugar + ((mi.ingredient.sugar / mi.ingredient.grams) * mi.grams)
        return sugar


class MealRecipe(models.Model):
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.meal} - {self.recipe}"


class MealIngredient(models.Model):
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    grams = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("100"),
        verbose_name = "Grams"
    )

    def get_calories(self):
        return (self.ingredient.calories / self.ingredient.grams) * self.grams

    def __str__(self):
        return f"{self.meal} - {self.ingredient.name} {self.grams}"


class BloodPressure(models.Model):
    on = models.DateTimeField(default=timezone.now)
    systolic = models.PositiveSmallIntegerField(default=120)
    diastolic = models.PositiveSmallIntegerField(default=80)
    heartrate = models.PositiveSmallIntegerField(default=60)

    def __str__(self):
        return f"{self.systolic} / {self.diastolic} - {self.on.day}/{self.on.month}/{self.on.year} {self.on.hour}:{self.on.minute}"


class Weight(models.Model):
    on = models.DateTimeField(default=timezone.now)
    lbs = models.PositiveSmallIntegerField(default=196)

    def __str__(self):
        return f"{self.lbs} - {self.on.day}/{self.on.month}/{self.on.year} {self.on.hour}:{self.on.minute}"
    

class Drink(models.Model):
    class DrinkIngredient(models.TextChoices):
        WATER = "WR", gettext_lazy("Water")
        COFFEE = "CF", gettext_lazy("Coffee")
        COCO = "CO", gettext_lazy("Coco")
        COFECO = "CC", gettext_lazy("CoffeeCoco")
        TEA = "TE", gettext_lazy("Tea")

    drink = models.CharField(
        max_length=2,
        choices=DrinkIngredient,
        default=DrinkIngredient.WATER,
    )
    litres = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("1"),
        verbose_name = "Litres"
    )
    start = models.DateTimeField(default=timezone.now)
    finish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_drink_display()} - {self.start.day}/{self.start.month}/{self.start.year} {self.start.hour}:{self.start.minute}"


class Mood(models.Model):
    on = models.DateTimeField(default=timezone.now)
    rating = models.PositiveSmallIntegerField(default=3)

    def __str__(self):
        return f"{self.on.day}/{self.on.month} {self.on.hour}:{self.on.minute} - {self.rating}"


class Sleep(models.Model):
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    rating = models.PositiveSmallIntegerField(default=3)

    def __str__(self):
        return f"{self.end.day}/{self.end.month} {self.end.hour}:{self.end.minute} - {self.rating}"
    

class Smoke(models.Model):
    on = models.DateTimeField(default=timezone.now)
    grams = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal("100"),
        verbose_name = "Grams"
    )

    def __str__(self):
        return f"{self.on.day}/{self.on.month} {self.on.hour}:{self.on.minute} - {self.grams}"


class Exercise(models.Model):
    class ExerciseType(models.TextChoices):
        CYCLE = "CY", gettext_lazy("Cycle")
        HIKE = "HK", gettext_lazy("Hike")

    exercise = models.CharField(
        max_length=2,
        choices=ExerciseType,
        default=ExerciseType.CYCLE,
    )
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    rating = models.PositiveSmallIntegerField(default=3)
    distance = models.PositiveIntegerField(default=1000) # Meters