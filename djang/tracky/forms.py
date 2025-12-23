from django.forms import ModelForm
from tracky.models import Ingredient

class IngredientForm(ModelForm):
    
    class Meta:
        model = Ingredient
    
        fields = '__all__'
