from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from imgstegno import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage


@login_required
def home(request):
    # count = User.objects.count()
    # return render(request, 'home.html', {
    #     'count': count
    # })


    # if request.method == 'POST' and request.FILES['myfile']:
    #     myfile = request.FILES['myfile']
    #     txtdata = request.POST['txtdata']
    #     fs = FileSystemStorage()
    #     filename = fs.save(myfile.name, myfile)
    #     uploaded_file_url = fs.url(filename)
    #     return render(request, 'uploadfile.html', {
    #         'uploaded_file_url': uploaded_file_url
    #     })
    # return render(request, 'uploadfile.html')

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            savDa = form.save()
            imgPath = savDa.document.path
            imgData = savDa.txtdata
            print("imgpath", imgPath, imgData)
            encode2(imgPath, imgData)
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'uploadfile2.html', {
        'form': form
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })


@login_required
def decrypt(request):
    docObj = Document.objects.filter(uploaded_by = request.user.id)
    return render(request, 'decLst.html', {'docObj':docObj})

@login_required
def imgdec(request, num):
    dataObj = Document.objects.get(id = num)
    print("request.user", request.user, dataObj.uploaded_by)
    if dataObj.uploaded_by == request.user:
        filename, file_extension = os.path.splitext(dataObj.document.path)
        img = str(filename) + "_enc" + file_extension
        do = decode2(img)
    else:
        do = "UnAuthorized User"
    return render(request, 'decData.html', {'do':do})


class SecretPage(LoginRequiredMixin, TemplateView):
    template_name = 'secret_page.html'