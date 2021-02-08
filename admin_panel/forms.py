from django import forms
from users.models import Users

class Upload_New_Product_Form(forms.Form):
    product_id = forms.IntegerField()
    name = forms.CharField(max_length=50)
    price = forms.DecimalField(max_digits=7, decimal_places=2)
    image = forms.ImageField()

class edit_user_form(forms.ModelForm):
    class Meta:  
        model = Users
        fields = "__all__"  