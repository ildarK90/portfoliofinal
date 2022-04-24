import json

import requests
from django.core.mail.backends.smtp import EmailBackend
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from rest_framework import generics, status
from .serializers import *
from .forms import *
from django.shortcuts import render


class ProjectList(generics.ListCreateAPIView):
    """
    Выводим список проектов
    """
    queryset = Project.objects.all().prefetch_related('skills').prefetch_related('id_teamlist').select_related(
        'id_category').select_related('id_view').order_by('p_sorting', '-id').filter(p_status=True)
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save()


class CatSkiList(generics.ListCreateAPIView):
    """
    Выводим список категорий навыков
    """
    queryset = CatSkill.objects.all().prefetch_related('skills').order_by('cs_sorting')
    serializer_class = CatSkillSerializer

    def perform_create(self, serializer):
        serializer.save()


class ProjectDetailed(RetrieveAPIView):
    """
    Выводим проект детально
    """
    serializer_class = ProjectDet

    def get_queryset(self, **kwargs):
        return Project.objects.filter(pk=self.kwargs['pk']).prefetch_related('skills').prefetch_related(
            'id_teamlist').select_related(
            'id_category').select_related('id_view')


# def messagesend(request):
#
#     if request.method == 'POST':
#         form = MailForm(request.POST)
#         if form.is_valid():
#             name = request.POST['name']
#             email = request.POST['email']
#             message = request.POST['message']
#             message = 'Письмо от ' + email + '\n' + message
#             send_mail(
#                 name,
#                 message,
#                 'abraklionchik@gmail.com',
#                 ['ildar.light@yandex.ru']
#             )
#     else:
#         form = MailForm
#     return render(request, 'mail.html',{'form': form})
#     # return render(request,'mail.html', {'form':form})

@csrf_exempt
def messagesend(request):
    name = request.data.get('name')
    email = request.data.get('email')
    message = request.data.get('message')
    message = 'Письмо от ' + name + '\n' + email + '\n' + message
    send_mail(
        name,
        message,
        'abraklionchik@gmail.com',
        ['ildar.light@yandex.ru']
    )
    return HttpResponse('OK')
    # return render(request,'mail.html', {'form':form})


class Sendemail(APIView):
    def post(self,request):
        # text = request.data.get('text')
        # print(text)
        name = request.data.get('name')
        email = request.data.get('email')
        message = request.data.get('message')
        message = 'Имя: ' + name + '\n\n' + 'Почта: ' + email + '\n\n' + 'Тема сообщения: ' + message
        send_mail(
            name,
            message,
            'abraklionchik@gmail.com',
            ['abraklion@gmail.com']
        )
        return Response({"answer": "Письмо отправлено"}, status=status.HTTP_201_CREATED)


# @csrf_exempt
# def messagesend(request):
#
#     name = request.GET.get('name')
#     email = request.GET.get('email')
#     message = request.GET.get('message')
#     message = 'Письмо от ' + email + '\n' + message
#     send_mail(
#         name,
#         message,
#         'abraklionchik@gmail.com',
#         ['abraklion@gmail.com']
#     )
#     return HttpResponse('OK')
#     # return render(request,'mail.html', {'form':form})
