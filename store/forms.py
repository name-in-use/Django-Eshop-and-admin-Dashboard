from django import forms

class RecommendProductForm(forms.Form):
    RECOMMEND=(
        ('y','Yes'),
        ('n','No'),
    )
   
    Recommend = forms.ChoiceField(choices = RECOMMEND, required=True)