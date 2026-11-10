from django import forms
from .models import SolicitudVacaciones, ComentarioSolicitud

class SolicitudVacacionesForm(forms.ModelForm):
    class Meta:
        model = SolicitudVacaciones
        fields = ["tipo", "fecha_inicio", "fecha_fin", "motivo", "companeros_asignados"]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
            "motivo": forms.Textarea(attrs={"rows": 3}),
        }

class ComentarioSolicitudForm(forms.ModelForm):
    class Meta:
        model = ComentarioSolicitud
        fields = ["texto"]