from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import Student, Extended
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import jwt
from .form import MovieForm


def homepage(request):
    # std = {'name': 'Ali', 'age': 19, 'marks': 90}

    # for std in d:
    #     obj = Student(std['name'], std['age'], std['marks'])

    #     std_list.append(obj)
    # return redirect(reverse('data'))
    return render(request, 'rift_edge.html')


def data(request):
    students = Student.objects.all()
    return render(request, 'data.html', {'stds': students})


def formdata(request):
    if request.method == 'POST':
        name = request.POST['n']
        age = request.POST['a']
        marks = request.POST['m']
        course = request.POST['c']

        std = Student()
        std.name = name
        std.age = age
        std.marks = marks
        std.course = course

        try:
            std.save()
            return redirect(reverse('data'))
        except:
            return HttpResponse('Data not Saved!')
        # return HttpResponse(f'You are with POST Method {name} Age: {age} Marks {marks}')
    return HttpResponse(f'You are with Get Method')


def delete_std(request, id):
    std = Student.objects.get(pk=id)
    std.delete()

    return redirect(reverse('data'))


def update_std(request, id):
    if request.method == 'POST':
        name = request.POST['n']
        age = request.POST['a']
        marks = request.POST['m']

        course = request.POST['c']
        std = Student.objects.get(pk=id)
        std.name = name
        std.age = age
        std.marks = marks
        std.course = course

        try:
            std.save()
            return redirect(reverse('data'))
        except:
            return HttpResponse('Data not Saved!')
    std = Student.objects.get(pk=id)
    return render(request, 'form.html', {'std': std})


@login_required(login_url='/mylogin/')
def admin_panel(request):
    return render(request, 'admin_panel.html')


def mylogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = email.split('@')[0]

        us = authenticate(username=username, password=password)

        if us is not None:
            login(request, us)

            return redirect(reverse('adminpanel'))
        else:
            return render(request, 'login.html', {'mes': 'Wrong Credentials!'})

    if request.user.is_authenticated:
        return redirect(reverse('adminpanel'))
    else:
        return render(request, 'login.html')


def mylogout(request):
    logout(request)
    return redirect(reverse('mylogin'))


def movie_form(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Data Saved..')
        else:
            return HttpResponse(f'{form.errors}')
    fmovie = MovieForm()
    return render(request, 'form.html', {'fmovie': fmovie})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        img = request.FILES['img']

        user = User.objects.create_user(username=username, email=email, password=password, is_active=True)
        ex = Extended()
        ex.id = user
        ex.image = img

        ex.save()

        # enc = jwt.encode(payload={'encid': str(user.pk)}, key='secret', algorithm='HS256')
        # link = f'{request.scheme}://{request.META["HTTP_HOST"]}/activation/{enc}/'
        # em = EmailMessage('Account Activation!', 'Thanks for creating an account!\n'+link,
        #                   from_email='hammadimran85@gmail.com', to=[email])

        # try:
        #     em.send()
        # except:
        #     HttpResponse('Unknown error occured')

        return render(request, 'signup.html', {'mes': 'Account Created Successfully!'})
    return render(request, 'signup.html')


def activation(request, id):
    dec = jwt.decode(id, key='secret', algorithms=['HS256'])
    us = User.objects.get(pk=int(dec['encid']))
    us.is_active = True
    us.save()
    return redirect(reverse('mylogin'))


from .models import Movie
from .serializers import MovieSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def movie_data(request):
    if request.method == 'GET':
        data = Movie.objects.all()
        sr = MovieSerializer(data, many=True)
        # return JsonResponse(sr.data, safe=False)
        return Response(sr.data)

    if request.method == 'POST':
        sr = MovieSerializer(data=request.data)
        if sr.is_valid():
            sr.save()
            data = Movie.objects.all()
            sr = MovieSerializer(data, many=True)
            # return JsonResponse(sr.data, safe=False)
            return Response(sr.data)


from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_movie_data(request, id):
    try:
        movie_obj = Movie.objects.get(pk=id)
    except:
        return Response({'detail': 'Movie object not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        sr = MovieSerializer(movie_obj)
        return Response(sr.data, status=status.HTTP_302_FOUND)

    if request.method == 'PUT':
        sr = MovieSerializer(movie_obj, data=request.data)
        if sr.is_valid():
            sr.save()
            return Response(sr.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f'Movie data is not valid {sr.errors}'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.method == 'DELETE':
        movie_obj.delete()
        return Response({'detail': f'Movie object not found or may be deleted'}, status=status.HTTP_204_NO_CONTENT)



# Create your views here.
