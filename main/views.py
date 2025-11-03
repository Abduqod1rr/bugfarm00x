from django.shortcuts import render, HttpResponse ,redirect , get_object_or_404
from django.views.generic import CreateView , ListView ,UpdateView ,DeleteView    , DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.contrib.auth.views import LoginView , LogoutView
from django.urls import reverse_lazy
from .models import Poc ,Profile ,Comment

class UserRegister(CreateView):
        form_class=forms.cutomuserform
        template_name='register.html'
        model=User
        success_url= reverse_lazy('login')

class UserLogin(LoginView):
        template_name='login.html'
        success_url=reverse_lazy('createprofile')

class userlogout(LogoutView):
        success_url=reverse_lazy('login')


class CreateProfile(CreateView):
        model=Profile
        fields=['bio','picture']
        template_name='createprofile.html'
        success_url=reverse_lazy('login')

        
        def form_valid(self, form):
         existing_profile = Profile.objects.filter(user=self.request.user).first()
         if existing_profile:
             messages.warning(self.request, "You already have a profile.")
             return redirect('myprofile')  # or wherever you want to send them

         form.instance.user = self.request.user
         return super().form_valid(form)

        
class Home(LoginRequiredMixin,ListView):
       model=Poc
       template_name='home.html'
       context_object_name='pocs'

       def get_queryset(self):    
            query = self.request.GET.get('q')
            if query:
                 return Poc.objects.filter(title__icontains=query)
            return Poc.objects.all().order_by('-created_at')


       
  

def toggle_like(request, pk):
     poc = get_object_or_404(Poc,pk=pk)

     if request.user in poc.like.all():
          poc.like.remove(request.user)
     else:
          poc.like.add(request.user)

     return redirect('home')
      
class AddPoc(LoginRequiredMixin,CreateView):
       model=Poc
       fields=['title','content']
       template_name='addpoc.html'
       success_url=reverse_lazy('home')

       def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
       
class MyPocs(LoginRequiredMixin,ListView):
      model=Poc 
      template_name='crud.html'
      context_object_name='pocs'

      def get_queryset(self):
          return Poc.objects.filter(owner=self.request.user)

class DeletePoc(LoginRequiredMixin,DeleteView):
      model=Poc
      template_name='crud.html'
      success_url=reverse_lazy('mypocs')

      def test_func(self):
            poc=self.get_object()
            return poc.owner == self.request.user

class UpdatePoc(LoginRequiredMixin,UpdateView):
      model=Poc
      template_name='crud.html'
      success_url=reverse_lazy('mypocs')
      fields=['title','content']

      def test_func(self):
            poc=self.get_object()
            return poc.owner == self.request.user
      
class MyProfile(LoginRequiredMixin,DetailView):
      model=Profile
      template_name='myprofile.html'
      context_object_name='profile'

      def get_object(self):
       obj, created = Profile.objects.get_or_create(user=self.request.user)
       return obj

class EditProfile(LoginRequiredMixin,UpdateView):
     model=Profile
     fields=['bio','picture']
     template_name='edit_profile.html'
     success_url=reverse_lazy('myprifile')

     def test_func(self):
            profile=self.get_object()
            return profile.owner == self.request.user 

     def get_object(self):
        # Automatically get the current user's profile
        obj, created = Profile.objects.get_or_create(user=self.request.user)
        return obj
     
class CommentPoc(LoginRequiredMixin,CreateView):
     model = Comment
     fields=['text']
     
     success_url = reverse_lazy('home')

     def form_valid(self, form):
         poc = get_object_or_404(Poc,pk=self.kwargs['pk'])
         form.instance.poc = poc

         form.instance.coment_owner = self.request.user

         return super().form_valid(form)
     