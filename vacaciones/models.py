from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TipoLicencia(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    remunerada = models.BooleanField(default=True)
    dias_maximos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class SolicitudVacaciones(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("aprobada", "Aprobada"),
        ("rechazada", "Rechazada"),
    ]

    empleado = models.ForeignKey(User, on_delete=models.CASCADE, related_name="solicitudes_vacaciones")
    tipo = models.ForeignKey(TipoLicencia, on_delete=models.PROTECT, related_name="solicitudes")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    fecha_solicitud = models.DateField(auto_now_add=True)
    companeros_asignados = models.ManyToManyField(
        User,
        blank=True,
        related_name="coberturas_vacaciones",
    )
    class Meta:
        verbose_name = "solicitud de vacaciones"
        verbose_name_plural = "solicitudes de vacaciones"

    def dias_totales(self):
        if self.fecha_inicio and self.fecha_fin:
            return (self.fecha_fin - self.fecha_inicio).days + 1
        return 0

    def clean(self):
        super().clean()
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")

    def __str__(self):
        return f"{self.empleado.username} - {self.fecha_inicio} a {self.fecha_fin}"

class ComentarioSolicitud(models.Model):
    solicitud = models.ForeignKey(
        SolicitudVacaciones,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "comentario de solicitud"
        verbose_name_plural = "comentarios de solicitudes"

    def __str__(self):
        return f"{self.autor.username} en {self.solicitud}"

# Create your models here.
