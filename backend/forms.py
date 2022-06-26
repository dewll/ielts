from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . models import Audio_store,Skill

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required = True)
    phone = forms.CharField(max_length = 20, required = True)

    class Meta:
        model = get_user_model()
        fields = ("first_name","last_name","email","zip_code",
                  "phone","city","state","password1", "password2")
        
class LoginForm(forms.Form):
    email = forms.EmailField(required = True)
    password = forms.CharField(required = True)
    
class UpdateForm(forms.Form):
    first_name = forms.CharField(required= True)
    last_name = forms.CharField(required= True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length = 20)
    zip_code = forms.CharField(max_length = 20)
    address = forms.CharField(max_length = 300)
    state = forms.CharField(max_length = 150)
    city = forms.CharField(max_length = 150)
    password1 = forms.CharField(required = True)
    password2 = forms.CharField(required = True)
    
    def validate(self,request):
        if self.password1 != self.password2:
            raise ('password not match')
        
class CheckEmailForm (forms.Form):
    email = forms.EmailField(required = True, help_text = "Enter Your Associated Email To Reset Your Password")
    
class ConfirmPasswordForm (forms.Form):
    password = forms.CharField(max_length = 50, required = True, help_text = "Enter Your new password") 
    confirm_password = forms.CharField(max_length = 50,  required = True, help_text = "ReEnter password")
    
class UploadForm (forms.Form):
    essay = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write Your Essay here'}))
    
class AudioForm(forms.ModelForm):
    class Meta:
        model=Audio_store
        fields=['record']
        
class SkillForm(forms.ModelForm):
    class Meta:
        model= Skill 
        fields = ['package','amount']
    