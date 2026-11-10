from django.urls import path
from . import views

app_name = "vacaciones"

urlpatterns = [
    path("", views.lista_solicitudes, name="lista"),
    path("crear/", views.crear_solicitud, name="crear"),
    path("<int:pk>/", views.detalle_solicitud, name="detalle"),
    path("<int:pk>/editar/", views.editar_solicitud, name="editar"),
    path("<int:pk>/eliminar/", views.eliminar_solicitud, name="eliminar"),
]