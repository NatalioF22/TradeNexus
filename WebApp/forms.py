from django import forms
from .models import Product, Profile, Conversation,User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'product_description', 'product_price', 'product_link', 'image', 'category']
        widgets = {
            'product_description': forms.Textarea(attrs={'rows': 4,'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'profile_image', 'profile_bio', 'website_link',
            'facebook_link', 'instagram_link', 'linkedIn_link', 'state', 'address', 
            'profession', 'zip_code', 'city', 'country', 'email', 'phone_number'
        ]
        widgets = {
            'state': forms.Select(attrs={'class': 'form-control'}),
        }

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")