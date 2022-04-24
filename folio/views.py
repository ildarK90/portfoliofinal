from rest_framework.generics import RetrieveAPIView, get_object_or_404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .serializers import *



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



