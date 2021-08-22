from django import forms
from django.views import generic
from django.shortcuts import redirect, render
from django.urls.base import is_valid_path
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
#from django.core.forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


from .models import Message

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class UserEditView(generic.UpdateView):
    form_class = UserChangeForm
    template_name = 'chat/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

class CustomLoginView(LoginView):
    template_name = 'chat/login.html'
    fields = '__all__'
    redirected_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

def registerView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'chat/register.html', {'form': form})
    
@login_required
def index(request):
    return render(request, 'chat/index.html')
@login_required
def room(request, room_name):
    username = request.GET.get('username', 'Anonymous')
    messages = Message.objects.filter(room=room_name)[0:25]

    return render(request, 'chat/room.html', {'room_name': room_name, 'username': username, 'messages': messages})