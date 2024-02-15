from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import CreateView,FormView, View
from .models import User
from .forms import UserForm, LoginForm, UpdatePasswordForm, VerificationForm
from .functions import code_generator


class UsuarioCreateView(FormView):
    model = User
    template_name = 'users/crear_usuario.html'
    form_class = UserForm
    success_url = '/'

    
    def form_valid(self, form):        
        #generamos el codigo
        codigo = code_generator()
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            codregistro = codigo
        )
        #enviar el codigo al email del usuario
        remitente = 'jacto2024@gmail.com'
        asunto = 'Confirmacion de Email'
        mensaje = 'Tu codigo de vertificacion es ' + codigo
        
        send_mail(asunto, mensaje, remitente, [form.cleaned_data['email'],])
        #redirigir a la pnatalla de confirmacion        
                
        return HttpResponseRedirect(
            reverse(
                'user_app:verificacion',
                kwargs={'pk':usuario.id}
            )
        )



class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:home')
    
    
    def form_valif(self,form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        login(self.request, user)
                
        return super(LoginView, self).form_valid(form)
    


class LogoutUser(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)        
             
        return HttpResponseRedirect(
            reverse(
                'user_app:login'
            )
        )



class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/updatepassword.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('user_app:login')
    login_url = reverse_lazy('user_app:login')
    
    
    def form_valid(self, form):
        
        usuario = self.request.user
        
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
        )
        if user:
            new_password = form.cleaned_data['password2']
            user.set_password(new_password)
            user.save()
            
        logout(self.request)            
        return super(UpdatePasswordView,self).form_valid(form)
    
    
    

class CodeVericationView(FormView):    
    template_name = 'users/verificacion.html'
    form_class = VerificationForm
    success_url = reverse_lazy('user_app:login')
    
    def get_form_kwargs(self):
        kwargs = super(CodeVericationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })
        return kwargs
    
    def form_valid(self, form):
        
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(is_active=True
        )
        
        return super(CodeVericationView, self).form_valid(form)
    
