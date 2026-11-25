from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import SolicitudVacaciones
from .forms import SolicitudVacacionesForm, ComentarioSolicitudForm
from openpyxl import Workbook
from openpyxl.styles import Font
from django.http import HttpResponse


@login_required
def lista_solicitudes(request):
    q = request.GET.get("q", "")
    solicitudes = SolicitudVacaciones.objects.all().order_by("-fecha_solicitud")
    if q:
        solicitudes = solicitudes.filter(empleado__username__icontains=q)
    return render(request, "vacaciones/solicitud_list.html", {"solicitudes": solicitudes, "q": q})

@login_required
def detalle_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudVacaciones, pk=pk)
    form = ComentarioSolicitudForm()

    if request.method == "POST":
        form = ComentarioSolicitudForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.solicitud = solicitud
            comentario.save()
            return redirect("vacaciones:detalle", pk=solicitud.pk)

    return render(request, "vacaciones/solicitud_detail.html", {"solicitud": solicitud, "form": form})

@login_required
def crear_solicitud(request):
    if request.method == "POST":
        form = SolicitudVacacionesForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.empleado = request.user
            solicitud.save()
            form.save_m2m()
            return redirect("vacaciones:detalle", pk=solicitud.pk)
    else:
        form = SolicitudVacacionesForm()

    return render(request, "vacaciones/solicitud_form.html", {"form": form})

@login_required
def editar_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudVacaciones, pk=pk)
    if solicitud.empleado != request.user:
        return redirect("vacaciones:lista")

    form = SolicitudVacacionesForm(request.POST or None, instance=solicitud)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("vacaciones:detalle", pk=solicitud.pk)

    return render(request, "vacaciones/solicitud_form.html", {"form": form})

@login_required
def eliminar_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudVacaciones, pk=pk)
    if solicitud.empleado != request.user:
        return redirect("vacaciones:lista")

    if request.method == "POST":
        solicitud.delete()
        return redirect("vacaciones:lista")

    return render(request, "vacaciones/solicitud_confirm_delete.html", {"solicitud": solicitud})

@login_required
def exportar_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Solicitudes"

    headers = ["Empleado", "Tipo", "Fecha inicio", "Fecha fin", "Días", "Estado", "Motivo"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)

    solicitudes = SolicitudVacaciones.objects.all().order_by("-fecha_solicitud")
    q = request.GET.get("q", "")
    if q:
        solicitudes = solicitudes.filter(empleado__username__icontains=q)

    for row, s in enumerate(solicitudes, 2):
        ws.cell(row=row, column=1, value=s.empleado.username)
        ws.cell(row=row, column=2, value=s.tipo.nombre)
        ws.cell(row=row, column=3, value=s.fecha_inicio.strftime("%d/%m/%Y"))
        ws.cell(row=row, column=4, value=s.fecha_fin.strftime("%d/%m/%Y"))
        ws.cell(row=row, column=5, value=s.dias_totales())
        ws.cell(row=row, column=6, value=s.get_estado_display())
        ws.cell(row=row, column=7, value=s.motivo)

    for col, width in enumerate([20, 20, 15, 15, 10, 15, 40], 1):
        ws.column_dimensions[chr(64 + col)].width = width

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="solicitudes.xlsx"'
    wb.save(response)
    return response



# Create your views here.
