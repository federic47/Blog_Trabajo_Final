from django.http import HttpResponse
from django .views.generic import ListView
from django .views.generic.detail import DetailView
from django .views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import *
from AppBlog.forms import NewsFormulario,UserRegistrationForm, UserEditForm,AvatarForm,MensajeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



#--------Definimos la views de inicio-----------------------------------------------------------------------------------#
def inicio(request):
        return render(request, 'AppBlog/inicio.html')
    


        
#---------Definimos la views de About-----------------------------------------------------------------------------------#
def about(request):
    return render(request,'AppBlog/about.html')
    

#----------Definimos la views de Login----------------------------------------------------------------------------------#

def login_request(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request=request, data=request.POST)
        if formulario.is_valid():
            usuario=formulario.cleaned_data.get('username')
            clave=formulario.cleaned_data.get('password')
            user=authenticate(username=usuario, password=clave)

            if user is not None:
                login(request, user)
                return render(request, 'AppBlog/inicio.html', {'usuario':usuario, 'mensaje':'Bienvenido al sistema'})
            else:
                return render(request, 'AppBlog/login.html', {'formulario':formulario, 'mensaje':'USUARIO INCORRECTO, VUELVA A LOGUEAR'})
        else:
            return render(request, 'AppBlog/login.html', {'formulario':formulario, 'mensaje':'FORMULARIO INVALIDO, VUELVA A LOGUEAR'})
    
    else:
        formulario=AuthenticationForm()
        return render(request, 'AppBlog/login.html', {'formulario':formulario})

#------------------------------Definimos la views de register------------------------------------------------------------------------#

def register(request):
    if request.method == 'POST':
        formulario = UserRegistrationForm(request.POST)
        if formulario.is_valid():
            username=formulario.cleaned_data['username']
            formulario.save()
            return render(request, 'AppBlog/inicio.html', {'mensaje':f'USUARIO: {username} CREADO EXITOSAMENTE'})
        
    else:
        formulario = UserRegistrationForm()
        return render(request, 'AppBlog/register.html', {'formulario':formulario})

#--------------------------------------Definimos la views de editar el perfil-------------------------------------------------------#

@login_required
def editarPerfil(request):
    usuario=request.user

    if request.method == 'POST':
        formulario=UserEditForm(request.POST, instance=usuario)
        if formulario.is_valid():
            informacion=formulario.cleaned_data
            usuario.email=informacion['email']
            usuario.password1=informacion['password1']
            usuario.password2=informacion['password2']
            usuario.save()  

            return render(request, 'AppBlog/about.html', {'usuario':usuario, 'mensaje':'PERFIL EDITADO EXITOSAMENTE'})
    else:
        formulario=UserEditForm(instance=usuario)
    return render(request, 'AppBlog/editarPerfil.html', {'formulario':formulario, 'usuario':usuario.username})


#---------------------------------------Agregando Avatar---------------------------------------------------------------------------#
@login_required
def agregarAvatar(request):
    user=User.objects.get(username=request.user)
    if request.method == 'POST':
        formulario=AvatarForm(request.POST, request.FILES)
        if formulario.is_valid():

            avatarViejo=Avatar.objects.get(user=request.user)
            if(avatarViejo.avatar):
                avatarViejo.delete()
                avatar=Avatar(user=user, avatar=formulario.cleaned_data['avatar'])
                avatar.save()
                return render(request, 'AppBlog/inicio.html', {'usuario':user, 'mensaje':'AVATAR AGREGADO EXITOSAMENTE','avatar':avatar})
            else:
                avatar=Avatar(user=user, avatar=formulario.cleaned_data['avatar'])
                avatar.save()
                return render(request, 'AppBlog/inicio.html', {'usuario':user, 'mensaje':'AVATAR AGREGADO EXITOSAMENTE', 'avatar':avatar})
    else:
        formulario=AvatarForm()
    return render(request, 'AppBlog/agregarAvatar.html', {'formulario':formulario, 'usuario':user})

#-----------------------------------Vista de Formulario de mensajes-----------------------#

def enviarMensaje(request):
    if request.method == 'POST':
        formulario = MensajeForm(request.POST)

        if formulario.is_valid():
            informacion = formulario.cleaned_data
            mensaje = Mensaje(usuario = informacion['usuario'], asunto= informacion['asunto'], campo=informacion['campo'])
            mensaje.save()
            return render(request, 'AppBlog/inicio.html',{'formulario':formulario, 'mensaje':'Mensaje enviado Exitosamente'})
    else:
        formulario =MensajeForm()
    return render(request, 'AppBlog/enviarMensaje.html', {'formulario':formulario})

#-----------------------------------vista de Buscar mensaje por usuario -----------------------------------------------------#

def buscarMensajes(request):
    usuario=request.user
    usuario = str(usuario)
    mensajes= Mensaje.objects.all()
    return render(request,'AppBlog/resultadosMensajes.html',{'mensajes': mensajes,'usuario':usuario})












#------------------------------Defino la vista de formulario Culture ------------------------------------------------------------------------------#

def newsFormulario(request):

    if request.method == 'POST':
          miFormulario = NewsFormulario(request.POST,request.FILES)
          
          
          if miFormulario.is_valid():
              informacion = miFormulario.changed_data
              culture = Culture(titulo=informacion['titulo'], subtitulo=informacion['subtitulo'], cuerpo=informacion['cuerpo'], autor=informacion['autor'], fecha=informacion['fecha'],imagen=informacion['imagen'])
              culture.save()
              return render(request,'AppBlog/inicio.html', {'mensaje':'Post creado exitosamente'})
    else:
        miFormulario= NewsFormulario()
    return render(request,'AppBlog/newsFormulario.html', {'miFormulario': miFormulario})

#**************************************Defino la vista del formulario Sports**************************************

def SportsFormulario(request):

    if request.method == 'POST':
          miFormulario = SportsFormulario(request.POST,request.FILES)
          
          
          if miFormulario.is_valid():
              informacion = miFormulario.changed_data
              sports = Sports(titulo=informacion['titulo'], subtitulo=informacion['subtitulo'], cuerpo=informacion['cuerpo'], autor=informacion['autor'], fecha=informacion['fecha'],imagen=informacion['imagen'])
              sports.save()
              return render(request,'AppBlog/inicio.html', {'mensaje':'Post creado exitosamente'})
    else:
        miFormulario= SportsFormulario()
    return render(request,'AppBlog/newsFormulario.html', {'miFormulario': miFormulario})

#**************************************Defino la vista del formulario Economy***********************
def EconomyFormulario(request):

    if request.method == 'POST':
          mieconomia = EconomyFormulario(request.POST,request.FILES)
          
          
          if mieconomia.is_valid():
              informacion = mieconomia.changed_data
              economy = Economy(titulo=informacion['titulo'], subtitulo=informacion['subtitulo'], cuerpo=informacion['cuerpo'], autor=informacion['autor'], fecha=informacion['fecha'],imagen=informacion['imagen'])
              economy.save()
              return render(request,'AppBlog/inicio.html', {'mensaje':'Post creado exitosamente'})
    else:
        miFormulario= EconomyFormulario()
    return render(request,'AppBlog/newsFormulario.html', {'miFormulario': miFormulario})
      
       
#*************************      CLASES BASADAS EN VISTAS     ***********************************************************************#
#***********************************************************************************************************************************#

#--------------------------Clase Culture------------------------------------------------------------------------------------#

class CultureList(LoginRequiredMixin,ListView):
    model = Culture
    template_name = 'AppBlog/culture_list.html'

class CultureDetalle(LoginRequiredMixin,DetailView):
    model = Culture
    template_name = 'AppBlog/culture_detalle.html'

class CultureCreacion(CreateView):
    model = Culture
    success_url= reverse_lazy('culture_listar')
    fields= ['titulo','subtitulo','cuerpo','autor','fecha','imagen']

class CultureEdicion(UpdateView):
    model = Culture
    success_url= reverse_lazy('culture_listar')
    fields= ['titulo','subtitulo','cuerpo','autor','fecha','imagen']

class CultureEliminacion(DeleteView):
    model = Culture
    success_url= reverse_lazy('culture_listar')
    fields= ['titulo','subtitulo','cuerpo','autor','fecha','imagen']


#--------------------------Clase Sport------------------------------------------------------------------------------------------#

class SportList(LoginRequiredMixin,ListView):
    model = Sports
    template_name = 'AppBlog/sports_list.html'

class SportsDetalle(LoginRequiredMixin,DetailView):
    model = Sports
    template_name = 'AppBlog/sports_detalle.html'

class SportCreacion(CreateView):
    model = Sports
    success_url= reverse_lazy('sports_listar')
    fields= ['titulo','subtitulo','cuerpo','autor','fecha','imagen']

class SportsEdicion(UpdateView):
    model = Sports
    success_url= reverse_lazy('sports_listar')
    fields= ['titulo','subtitulo','cuerpo','autor','fecha','imagen']

class SportsEliminacion(DeleteView):
    model = Sports
    success_url= reverse_lazy('sports_listar')
    fields= ['titulo','subtitulo','cuerpo','autor','fecha','imagen']


#--------------------------Clase Economy------------------------------------------#

class EconomyList(LoginRequiredMixin,ListView):
    model = Economy
    template_name = 'AppBlog/economy_list.html'

class EconomyDetalle(LoginRequiredMixin,DetailView):
    model = Economy
    template_name = 'AppBlog/economy_detalle.html'

class EconomyCreacion(CreateView):
    model = Economy
    success_url= reverse_lazy('economy_listar')
    fields= ['titulo','subtitulo','cuerpo','autor','fecha','imagen']

class EconomyEdicion(UpdateView):
    model = Economy
    success_url= reverse_lazy('economy_listar')
    fields= ['titulo','subtitulo','cuerpo','autor','fecha','imagen']

class EconomyEliminacion(DeleteView):
    model = Economy
    success_url= reverse_lazy('economy_listar')
    fields= ['titulo','subtitulo','cuerpo','autor','fecha','imagen']