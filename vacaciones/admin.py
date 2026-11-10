from django.contrib import admin
from .models import TipoLicencia, SolicitudVacaciones, ComentarioSolicitud

admin.site.register(TipoLicencia)
admin.site.register(SolicitudVacaciones)
admin.site.register(ComentarioSolicitud)
# Register your models here.
