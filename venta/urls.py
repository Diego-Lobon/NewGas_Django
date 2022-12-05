from django.urls import path
from venta.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', crear, name='crear'),
    path('home', HomePageView.as_view(), name="index"),
    path('empresa/', EmpresaPageView.as_view(), name="empresa"),
    path('productos/', ProductosPageView.as_view(), name="productos"),
    path('servicios/', ServiciosPageView.as_view(), name="servicios"),
    path('contactenos/', ContactenosPageView.as_view(), name="contactenos"),
    path('carritoCompras/', CarritoDeComprasPageView.as_view(), name="carritoCompras"),
    path('iniciarSesion/', IniciarSesionPageView.as_view(), name="iniciarSesion"),
    #path('iniciarSesion/', auth_views.LoginView.as_view(template_name='iniciarSesion.html'), name="iniciarSesion"),
    path('registrarse/', RegistrarsePageView.as_view(), name="registrarse"),
    path('salir/', salir, name="logout"),
    path('pagoInformacion/', PagoInformacionPageView.as_view(), name="pagoInformacion"),
    path('pagoEnvio/', PagoEnvioPageView.as_view(), name="pagoEnvio"),
    path('pagoFinal/', PagoFinalPageView.as_view(), name="pagoFinal"),
    path('payment-success/', PaymentSuccessPageView.as_view(), name="payment-success"),
    path('payment-failed/', PaymentFailedPageView.as_view(), name="payment-failed"),
    path('pedido/', PedidoPageView.as_view(), name="pedido"),
    path('miCuenta/', CuentaPageView.as_view(), name="miCuenta"),
]