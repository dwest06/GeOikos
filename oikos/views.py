from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "oikos/home.html")

def noikos(request):
    return render(request, "oikos/n-oikos.html")

def nmiembros(request):
    miembros_list = {
        "name":['Francisco Marcos',
                'Carlos Sivira'],
        "picture":['../../static/img/miembros/profile-francisco.jpg',
                  '../../static/img/miembros/profile-carlos.jpg'],
        "carrera":["Cohorte '11 USB",
                   "Cohorte '15 USB"],
        "instagram":['https://www.instagram.com/wrancisco/',
                     ''],
        "twitter":['https://twitter.com/wrancisco', 
                     '']
    }
    return render(request, "oikos/n-miembros.html",miembros_list)

'''
- name: Michael Sanchez
  picture: /assets/img/miembros/profile-michael.jpg
  carrera: Cohorte '09 USB

- name: Orlando Perez
  picture: /assets/img/miembros/profile-orlando.jpg
  carrera: Cohorte '12 USB


- name: Daniela Torres
  picture: /assets/img/miembros/profile-daniela.jpg
  carrera: UNIMET

- name: Nicolas Jaua
  picture: /assets/img/miembros/profile-nico.jpg
  carrera: Cohorte '15 USB

- name: Paola Proietti
  picture: /assets/img/miembros/profile-pao.jpg
  carrera: UCAB


- name: Luis Carlos Marval
  picture: /assets/img/miembros/profile-luiski.jpg
  carrera: Cohorte '12 USB
  instagram: https://www.instagram.com/lcmarval/
  twitter: https://twitter.com/luiscamarval

- picture: /assets/img/miembros/profile-nina.jpg
  name: Valentina González
  carrera: Cohorte '13 USB
  instagram: https://www.instagram.com/niina_hood/
  twitter: https://www.instagram.com/niina_hood/

- picture: /assets/img/miembros/profile-esteban.jpg
  name: Esteban Camargo
  carrera: Cohorte '11 USB
  instagram: https://www.instagram.com/estebmaister/
  twitter: https://twitter.com/Estebmaister

- picture: /assets/img/miembros/profile-jeral.jpg
  name:  Jeraldine Aparicio
  carrera: Cohorte '14 USB
  instagram: https://www.instagram.com/jeraldine12/'''

def njd(request):
    return render(request, "oikos/n-jd.html")

def nhonorarios(request):
    return render(request, "oikos/n-honorarios.html")

def cursos(request):
    return render(request, "oikos/cursos.html")

def calta(request):
    return render(request, "oikos/c-alta.html")

def cbaja(request):
    return render(request, "oikos/c-baja.html")

def croca(request):
    return render(request, "oikos/c-roca.html")

def contacto(request):
    return render(request, "oikos/contacto.html")

def expediciones(request):
    return render(request, "oikos/expediciones.html")

def blog(request):
    return render(request, "oikos/blog.html")

