from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Carrera
from .vistas import FormCarrera
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

def index(request):
    return HttpResponse("Hello, world!")

class HomePageView(TemplateView):
    template_name = "home.html"
    model = Carrera
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ["saludo"] = "Hola de nuevo"
        context["lista"] = [carrera for carrera in self.model.objects.all()]
        return context
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AboutPageView(TemplateView):
    template_name = "about.html"

@method_decorator(permission_required('tutorial.add_carrera', login_url="/", raise_exception=False), name='dispatch')
class CarrerasCreateViewPage(TemplateView):
    template_name = "carreras_form.html"
    def get(self, request, *args, **kwargs):
        form = FormCarrera()
        context = {'form': form}
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        form = FormCarrera(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return self.render_to_response({'form':form})

class CarrerasEditarViewPage(TemplateView):
    template_name = "carreras_form.html"
    def get(self, request, pk, *args, **kwargs):
        carrera = get_object_or_404(Carrera, pk=pk)
        form = FormCarrera(instance= carrera)
        return self.render_to_response({'form': form, 'has_permission': request.user.has_perm('tutorial.change_carrera')})
    
    @method_decorator(permission_required('tutorial.change_carrera', login_url="/", raise_exception=False), name='dispatch')
    def post(self, request, pk, *args, **kwargs):
        carrera = get_object_or_404(Carrera, pk=pk)
        form = FormCarrera(request.POST, instance=carrera)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})
        
class CarrerasEliminarViewPage(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        carrera = get_object_or_404(Carrera, pk=pk)
        carrera.delete()
        return redirect('/')

class WebSocketView(TemplateView):
    template_name = "websocket.html"