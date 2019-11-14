from django.urls import path
from .views import home, noikos, nmiembros, njd, nhonorarios, cursos, calta, cbaja, croca, contacto, expediciones, blog
from django.conf.urls.static import static
from django.conf import settings

app_name = "oikos"

urlpatterns = [
    path('', home, name="home"),
    path('noikos/', noikos , name="noikos"),
    path('nmiembros/', nmiembros , name="nmiembros"),
    path('njd/',njd,name="njd"),
    path('nhonorarios/',nhonorarios,name="nhonorarios"),
    path('cursos/',cursos,name="cursos"),
    path('calta/',calta,name="calta"),
    path('cbaja/',cbaja,name="cbaja"),
    path('croca/',croca,name="croca"),
    path('contacto/',contacto,name="contacto"),
    path('expediciones/',expediciones,name="expediciones"),
    path('blog/',blog,name="blog")

]
