from django.shortcuts import render, HttpResponse ,redirect , get_object_or_404
from django.views.generic import CreateView , ListView ,UpdateView ,DeleteView    , DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.contrib.auth.views import LoginView , LogoutView
from django.urls import reverse_lazy
from .models import Poc ,Profile ,Comment , BugProgress
from django.db import connection
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

# ---- Landing Page ----

def landing(request):
    return render(request, 'landing.html')


# ---- Scoreboard ----

@login_required
def scoreboard(request):
    progress = BugProgress.objects.filter(user=request.user)
    found_ids = [p.bug_id for p in progress]
    all_bugs = [b[0] for b in BugProgress.BUG_CHOICES]
    context = {
        'found_ids': found_ids,
        'all_bugs': all_bugs,
        'bug_labels': dict(BugProgress.BUG_CHOICES),
    }
    return render(request, 'scoreboard.html', context)


@login_required
def mark_found(request, bug_id):
    valid_ids = [b[0] for b in BugProgress.BUG_CHOICES]
    if bug_id in valid_ids:
        BugProgress.objects.get_or_create(user=request.user, bug_id=bug_id)
    return redirect('scoreboard')


# ---- Hints ----

def hints(request):
    return render(request, 'hints.html')


# ---- Solutions ----

def solutions(request):
    return render(request, 'solutions.html')


# ---- Auth ----

class UserRegister(CreateView):
        form_class=forms.cutomuserform
        template_name='register.html'
        model=User
        success_url= reverse_lazy('login')

# VULN: SQLi - uses string concatenation in raw SQL query instead of parameterized queries
# VULN: Open redirect - no validation on next parameter after login
def UserLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # VULN: SQL injection - raw SQL with string interpolation
        query = f"SELECT id FROM auth_user WHERE username = '{username}' AND password = '{password}'"
        cursor = connection.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            user = User.objects.get(pk=row[0])
            auth_login(request, user)
            # VULN: Open redirect - no URL validation, redirects to any URL
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('createprofile')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    return render(request, 'login.html')

class userlogout(LogoutView):
        success_url=reverse_lazy('landing')


class CreateProfile(CreateView):
        model=Profile
        fields=['bio','picture']
        template_name='createprofile.html'
        success_url=reverse_lazy('feed')

        
        def form_valid(self, form):
         existing_profile = Profile.objects.filter(user=self.request.user).first()
         if existing_profile:
             messages.warning(self.request, "You already have a profile.")
             return redirect('myprofile')

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

     return redirect('feed')
      
class AddPoc(LoginRequiredMixin,CreateView):
       model=Poc
       # VULN: Unrestricted file upload - no validation of file type, size, or content
       fields=['title','content']
       template_name='addpoc.html'
       success_url=reverse_lazy('feed')

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
      
# VULN: IDOR - no ownership check, any user's profile can be viewed by PK
class UserProfile(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'myprofile.html'
    context_object_name = 'profile'

class EditProfile(LoginRequiredMixin,UpdateView):
     model=Profile
     fields=['bio','picture']
     template_name='edit_profile.html'
     success_url=reverse_lazy('myprofile')

     def test_func(self):
            profile=self.get_object()
            return profile.owner == self.request.user 

     def get_object(self):
        obj, created = Profile.objects.get_or_create(user=self.request.user)
        return obj
     
class CommentPoc(LoginRequiredMixin,CreateView):
     model = Comment
     fields=['text']
     
     success_url = reverse_lazy('feed')

     def form_valid(self, form):
         poc = get_object_or_404(Poc,pk=self.kwargs['pk'])
         form.instance.poc = poc

         form.instance.coment_owner = self.request.user

         return super().form_valid(form)
