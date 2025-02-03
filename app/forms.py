from django import forms 
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from app.models import User, Profile, Question, Tag, Answer

class LoginForm(forms.Form):
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrong':
            raise ValidationError('Wrong password!')
        return data
        

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(label='Upload avatar', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password' ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
    

class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'resize': 'none'}))
    tags = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Question
        fields = ['title', 'text']


    def clean(self, **kwargs):
        tags_input = self.cleaned_data['tags']
        tags = [tag.strip() for tag in tags_input.split(' ')]
        if len(tags) > 3:
            raise ValidationError('You cannot use more than 3 tags!')
        
    

class AnswerForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'style':'resize:none;'}))

    class Meta:
        model = Answer
        fields = ['text']

class SettingsForm(forms.ModelForm):
    forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(label='Upload avatar', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password' ]


    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.save()
        profile, created = Profile.objects.get_or_create(user=user)
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            profile.avatar = self.cleaned_data.get('avatar')
        profile.save()
        return user
