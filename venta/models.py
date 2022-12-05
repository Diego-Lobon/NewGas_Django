from django.db import models
from django.contrib.auth.models import User
#from django.forms import model_to_dict
# Create your models here.

class mensajeContacto(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correoElectronico = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255)
    dni = models.BigIntegerField()
    celular = models.BigIntegerField()
    consulta= models.CharField(max_length=500)
    fecha = models.DateTimeField(auto_now_add=True)

class productos(models.Model):
    nombre = models.CharField(max_length=255)
    cantidad = models.BigIntegerField()
    precio = models.FloatField()
    peso = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255)
    descripcion = models.TextField()
    stripe_id = models.CharField(max_length=1000)

class carritoDeCompras(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(productos, on_delete=models.CASCADE)
    cantidadProducto = models.BigIntegerField()
    total = models.FloatField()

    @property
    def nombre(self):
        return self.producto.nombre

    @property
    def cantidad(self):
        return self.producto.cantidad

    @property
    def precio(self):
        return self.producto.precio

    @property
    def peso(self):
        return self.producto.peso

    @property
    def categoria(self):
        return self.producto.categoria

    @property
    def descripcion(self):
        return self.producto.descripcion

    @property
    def stripe_id(self):
        return self.producto.stripe_id

class informacionPago(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    apartamento = models.CharField(max_length=255)
    distrito = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    celular = models.CharField(max_length=255)
    correo = models.CharField(max_length=255)
    metodo = models.CharField(max_length=255)
    dni = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    


class ventas(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(productos, on_delete=models.CASCADE)
    estadoPago = models.CharField(max_length=255)
    cantidadProducto = models.BigIntegerField()
    total = total = models.FloatField()
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    apartamento = models.CharField(max_length=255)
    distrito = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    celular = models.BigIntegerField()
    correo = models.CharField(max_length=255)
    metodo = models.CharField(max_length=255)
    dni = models.BigIntegerField()
    estadoEntrega = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

    @property
    def nombreProducto(self):
        return self.producto.nombre

    @property
    def cantidad(self):
        return self.producto.cantidad

    @property
    def precio(self):
        return self.producto.precio

    @property
    def peso(self):
        return self.producto.peso

    @property
    def categoria(self):
        return self.producto.categoria

    @property
    def descripcion(self):
        return self.producto.descripcion

    @property
    def stripe_id(self):
        return self.producto.stripe_id



