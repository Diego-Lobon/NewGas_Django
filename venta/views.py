from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import View

from django.urls import reverse_lazy
from django.contrib import messages

from venta.models import *
from venta.forms import *
from ipware import get_client_ip
from django.template import Context

from django.template.defaulttags import register
from django.db.models import Sum

from itertools import chain


import stripe

from django.conf import settings
from django.urls import reverse

class HomePageView(TemplateView):
    
    template_name = 'index.html'
    
    #def get(self, request):
    #    ip, public_or_private = get_client_ip(request)
    #    return render(request, 'index.html', {
    #        'ip': ip
    #    })
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['ip'], public_or_private = get_client_ip(self.request)
        return context

class EmpresaPageView(TemplateView):
    template_name = 'empresa.html'

class ProductosPageView(ListView):
    template_name = 'productos.html'
    model = productos


    def get_queryset(self):
        
        new_context = productos.objects.filter(
            categoria = 'Balon de Gas'
        )
        
        return new_context

    def post(self, request):
        print("Hay datos")
        
        nombre_usuario = request.session['user']

        idUsuario = User.objects.get(username = nombre_usuario).pk
        idProducto= request.POST['idProducto']
        precioProducto = request.POST['precio']

        if carritoDeCompras.objects.filter(producto_id = idProducto, usuario_id = idUsuario).exists() :
            print("existe")
            

            producto = carritoDeCompras.objects.get(producto_id = idProducto, usuario_id = idUsuario)

            if producto.cantidadProducto + 1 <= producto.cantidad:
                producto.cantidadProducto = producto.cantidadProducto + 1
            else:
                print("Supera la cantidad maxima")

            cant = producto.cantidadProducto
            
            producto.total = float(precioProducto) * cant
            tot = producto.total

            print("cantidad: ",cant)
            print("total: ",tot)

            producto.save()

        else:
            print("no existe")

            carritoDeCompras.objects.create(
                producto_id = idProducto,
                usuario_id = idUsuario,
                cantidadProducto = 1,
                total = precioProducto
            )

        
        return redirect("productos")

class ServiciosPageView(TemplateView):
    template_name = 'servicios.html'

class ContactenosPageView(CreateView):
    template_name = 'contactenos.html'
    model = mensajeContacto
    form_class = mensajeContactoForm
    success_url = reverse_lazy('index')

class CarritoDeComprasPageView(ListView):
    template_name = 'carritoCompras.html'
    model = carritoDeCompras


    def post(self, request):
        print(request.POST)
        metodo = request.POST['metodo']
        
        if metodo == 'eliminar':
            print("Eliminando Producto ...")

            if 'idCarrito' in request.POST:
                print('hay dato')

                carrito = carritoDeCompras.objects.get(id = request.POST['idCarrito'])
                carrito.delete()

            else:
                print('no hay')



        elif metodo == 'actualizar':
            print('Actualizando Producto ...')

            if 'cantidadProducto' in request.POST:
                print("hay dato")

                cantidad = request.POST['cantidadProducto']
                precioProducto = request.POST['precioProducto']
                
                
                carrito = carritoDeCompras.objects.get(id = request.POST['idCarrito'])
                carrito.cantidadProducto = cantidad
                carrito.total = float(precioProducto) * float(cantidad)
                carrito.save()
            else:
                print("No hay")

        else:
            print('ERROR')     

        return redirect('carritoCompras')

    def get_queryset(self):

        nombre_usuario = self.request.session['user']
        idUsuario = User.objects.get(username = nombre_usuario).pk
        
        new_context = carritoDeCompras.objects.filter(
            usuario_id = idUsuario
        )

        return new_context

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        nombre_usuario = self.request.session['user']
        idUsuario = User.objects.get(username = nombre_usuario).pk

        context['suma'] = carritoDeCompras.objects.filter(usuario_id = idUsuario).aggregate(Sum('total'))
        
        return context
    


class IniciarSesionPageView(FormView):
    template_name = 'iniciarSesion.html'
    
    form_class = AuthenticationForm

    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        

        if form.is_valid():
            ip, public_or_private = get_client_ip(request)
            nombre_usuario = form.cleaned_data.get("username")


            if str(nombre_usuario) != str(ip):

                password = form.cleaned_data.get("password")
                usuario = authenticate(username=nombre_usuario, password=password)
                if usuario is not None:
                    
                    login(request, usuario)
                    print("INICIO")
                    request.session['user'] = nombre_usuario
                    return redirect("crear")
                else:
                    print("datos no correctos")   
                    
            else:
                
                print("NO PUEDES")    
                return redirect("iniciarSesion")    
        else:
            #print("error")
            #print(form.errors.as_data())
            print("error")
    


class RegistrarsePageView(CreateView):
    template_name = 'registrarse.html'
    model = User
    form_class = UserCreationForm

    def post(self, request):
        
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save() 
            return redirect('index') 
        else:
            
            print("NO REGISTRADO")
    
    

def salir(request):
    logout(request)
    ip, public_or_private = get_client_ip(request)
    request.session['user'] = ip
    return redirect("iniciarSesion")



def crear(request):
    usuarios = User.objects.all()
    ip, public_or_private = get_client_ip(request)

    if 'username' in request.POST and 'password' in request.POST:
        print('hay datos post')
    
    elif 'user' in request.session:
        print('hay sesion aun')

    else:
        print('no hay sesion, creando...')
        request.session['user'] = ip
        band = 0
        for i in usuarios:
            if str(ip) == str(i):
                band = 1 

        if band == 1:
            print("YA EXISTE")
            
        else:
            print("NO EXISTE")
            User.objects.create_user(
                username = ip,
                password = '1234'
            )  
    
    
    
    return redirect("index")   
        

class PagoInformacionPageView(ListView):
    
    template_name = 'pagoInformacion.html'
    model = informacionPago

    def get_context_data(self, **kwargs):
        ip, public_or_private = get_client_ip(self.request)
        context = super().get_context_data(**kwargs)
        nombre_usuario = self.request.session['user']
        idUsuario = User.objects.get(username = nombre_usuario).pk

        if informacionPago.objects.filter(usuario_id = idUsuario).exists():
            print('hay dato')
        else:
            print("no existe")
            informacionPago.objects.create(
                nombre = '',
                apellido = '',
                direccion = '',
                apartamento = '',
                distrito = '',
                region = '',
                celular = '',
                correo = '',
                metodo = '',
                ip = ip,
                usuario_id = idUsuario,
                dni = '',
            )
        
        context['productos'] = carritoDeCompras.objects.filter(usuario_id = idUsuario)
        context['informacionUsuario'] = informacionPago.objects.filter(usuario_id = idUsuario)
        context['suma'] = carritoDeCompras.objects.filter(usuario_id = idUsuario).aggregate(Sum('total'))
        
        return context

    def post(self, request):



        nombre_usuario = self.request.session['user']
        idUsuario = User.objects.get(username = nombre_usuario).pk
        usuarioInformacion = informacionPago.objects.get(usuario_id = idUsuario)

        usuarioInformacion.correo = request.POST['correo']
        usuarioInformacion.celular = request.POST['celular']
        usuarioInformacion.nombre = request.POST['nombre']
        usuarioInformacion.apellido = request.POST['apellido']
        usuarioInformacion.direccion = request.POST['direccion']
        usuarioInformacion.apartamento = request.POST['apartamento']
        usuarioInformacion.distrito = request.POST['distrito']
        usuarioInformacion.region = request.POST['region']
        usuarioInformacion.dni = request.POST['dni']

        usuarioInformacion.save()

        return redirect('pagoEnvio')

class PagoEnvioPageView(ListView):
    template_name = 'pagoEnvio.html'
    model = informacionPago
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        nombre_usuario = self.request.session['user']
        idUsuario = User.objects.get(username = nombre_usuario).pk

        if informacionPago.objects.filter(usuario_id = idUsuario).exists():
            print('hay dato')
        else:
            print("no existe")
        
        context['productos'] = carritoDeCompras.objects.filter(usuario_id = idUsuario)
        context['informacionUsuario'] = informacionPago.objects.filter(usuario_id = idUsuario)
        context['suma'] = carritoDeCompras.objects.filter(usuario_id = idUsuario).aggregate(Sum('total'))
        
        return context

    def post(self, request):

        nombre_usuario = self.request.session['user']
        idUsuario = User.objects.get(username = nombre_usuario).pk
        usuarioInformacion = informacionPago.objects.get(usuario_id = idUsuario)

        usuarioInformacion.metodo = request.POST['metodo']

        usuarioInformacion.save()

        return redirect('pagoFinal')


class PagoFinalPageView(ListView):
    template_name = 'pagoFinal.html'
    model = informacionPago



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        nombre_usuario = self.request.session['user']
        idUsuario = User.objects.get(username = nombre_usuario).pk

        if informacionPago.objects.filter(usuario_id = idUsuario).exists():
            print('hay dato')
        else:
            print("no existe")

        

        context['productos'] = carritoDeCompras.objects.filter(usuario_id = idUsuario)
        context['informacionUsuario'] = informacionPago.objects.filter(usuario_id = idUsuario)
        context['suma'] = carritoDeCompras.objects.filter(usuario_id = idUsuario).aggregate(Sum('total'))
        

        productos = []

        for i in context['productos']:
            
            producto = {
                    "price": i.stripe_id,
                    "quantity": i.cantidadProducto,
                    }

            print(i.stripe_id)
            productos.append(producto)

        stripe.api_key = settings.STRIPE_PRIVATE_KEY

        print("tipo:",type(producto))

        session = stripe.checkout.Session.create(
            line_items=productos,

            mode='payment',
            success_url = self.request.build_absolute_uri(reverse('payment-success'))+'?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = self.request.build_absolute_uri(reverse('payment-failed')),
        )

        context['session_id'] = session.id
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY


        return context

    



class PaymentSuccessPageView(TemplateView):
    template_name = 'payment-success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ip, public_or_private = get_client_ip(self.request)

        nombre_usuario = self.request.session['user']
        idUsuario = User.objects.get(username = nombre_usuario).pk
        context['informacionUsuario'] = informacionPago.objects.filter(usuario_id = idUsuario)
        context['productos'] = carritoDeCompras.objects.filter(usuario_id = idUsuario)

        for i in context['productos']:
            
            for j in context['informacionUsuario']:
                idUser = 15
                print(idUser)
                ventas.objects.create(
                    estadoPago = 'Pagado',
                    cantidadProducto = i.cantidadProducto,
                    total = i.total,
                    nombre = j.nombre,
                    apellido = j.apellido,
                    direccion = j.direccion,
                    apartamento = j.apartamento,
                    distrito = j.distrito,
                    region = j.region,
                    celular = j.celular,
                    correo = j.correo,
                    metodo = j.metodo,
                    dni = j.dni,
                    estadoEntrega = 'En Proceso',
                    ip = ip,
                    producto_id = i.producto_id,
                    usuario_id = i.usuario_id,
                )

                idCarrito = carritoDeCompras.objects.filter(producto_id = i.producto_id, usuario_id = i.usuario_id)
                idCarrito.delete()

                idInformacion = informacionPago.objects.filter(usuario_id = i.usuario_id)
                idInformacion.delete()

        return context



class PaymentFailedPageView(TemplateView):
    template_name = 'payment-failed.html'

class PedidoPageView(TemplateView):
    template_name = 'pedido.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ip, public_or_private = get_client_ip(self.request)

        nombre_usuario = self.request.session['user']
        idUsuario = User.objects.get(username = nombre_usuario).pk
        context['informacionUsuario'] = informacionPago.objects.filter(usuario_id = idUsuario)
        context['productos'] = carritoDeCompras.objects.filter(usuario_id = idUsuario)

        for i in context['productos']:
            
            for j in context['informacionUsuario']:

                ventas.objects.create(
                    estadoPago = 'No Pagado',
                    cantidadProducto = i.cantidadProducto,
                    total = i.total,
                    nombre = j.nombre,
                    apellido = j.apellido,
                    direccion = j.direccion,
                    apartamento = j.apartamento,
                    distrito = j.distrito,
                    region = j.region,
                    celular = j.celular,
                    correo = j.correo,
                    metodo = j.metodo,
                    dni = j.dni,
                    estadoEntrega = 'En Proceso',
                    ip = ip,
                    producto_id = i.producto_id,
                    usuario_id = i.usuario_id,
                )

                idCarrito = carritoDeCompras.objects.filter(producto_id = i.producto_id, usuario_id = i.usuario_id)
                idCarrito.delete()

                idInformacion = informacionPago.objects.filter(usuario_id = i.usuario_id)
                idInformacion.delete()

        return context

         
class CuentaPageView(TemplateView):

    template_name = 'miCuenta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        nombre_usuario = self.request.session['user']
        idUsuario = User.objects.get(username = nombre_usuario).pk
        
        context['historial'] = ventas.objects.filter(usuario_id = idUsuario)

        for i in context['historial']:


            print(i.nombreProducto)

        return context
    
    
