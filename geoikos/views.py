from django.shortcuts import render

def home(request):
    return render(request,'oikos/home.html')

def image_gallery(request):
    images = Image.objects.all()
    print(images)
    return render(request, './')