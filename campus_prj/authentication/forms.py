from django.contrib.auth.forms import UserCreationForm, forms
from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'photo', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'password1': forms.TextInput(attrs={'placeholder': 'Password'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Confirm password'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'


class UserProfileForm(forms.ModelForm):
    # password1 = forms.CharField(required=False, widget=forms.PasswordInput)
    # password2 = forms.CharField(required=False, widget=forms.PasswordInput)
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['photo', 'bio', 'password']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'

    # def save(self, commit=True):
    #     user = super(UserProfileForm, self).save(commit=False)
    #     user.(self.request.user.password)
    #     if commit:
    #         user.save()
    #     return user
