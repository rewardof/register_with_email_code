import smtplib

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User, Code
from .forms import UserRegistrationForm
from .serializers import UserRegisterSerializer
from random import randint
from .serializers import CodeSerializer
from rest_framework import generics, status


class UserRegisterView(generic.CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user/templates/register.html'
    success_url = 'home/'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     return context

    def form_valid(self, form):
        password = form.data.get('password')
        password2 = form.data.get('password2')
        if password2 != password:
            messages.error(self.request, 'Passwords do not match')
            return redirect('register')
        # send_mail('salom', 'qalesan', 'tohirbeksoliyev88@gmail.com', ['rewardof99@gmail.com', ], fail_silently=False)
        return super().form_valid(form)


def checking_code_view(request):
    pass

def sending_email(to=[], code=None):
    subject = "Activating Account"
    msg = f"Please to activate your account, enter the code: {code}"
    res = send_mail(subject, msg, 'tohirbeksoliyev88@gmail.com', to, fail_silently=False)
    if (res == 1):
        msg = "Mail Sent Successfully."
    else:
        msg = "Mail Sending Failed."
    return Response({'message': msg})


class UserRegisterViewSet(ModelViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def get_rand_num():
        # bool = True
        # while bool:
        #     random_num = randint(10000000, 99999999)
        #     if random_num not in Code.objects.all():
        #         bool = False
        random_num = randint(10000000, 99999999)
        return random_num

    code = get_rand_num()
    save_code = code

    def create(self, request, *args, **kwargs):
        response = super(UserRegisterViewSet, self).create(request, *args, **kwargs)
        sending_email(to=[self.request.data.get('email'), ], code=self.code)  # sending mail
        print('sent successfully')
        return redirect('activate_account')


# @api_view(['POST', 'Get'])
# def activate_account(request):
#     if request.method == "POST":
#         serializer = CodeSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#     else:
#         data = Code.objects.all()
#         serializer = CodeSerializer(data, many=True)
#         return Response(serializer.data)


class CodeApiView(generics.CreateAPIView):
    code = UserRegisterViewSet.save_code
    serializer_class = CodeSerializer
    queryset = Code.objects.all()

    def create(self, request, *args, **kwargs):
        code = UserRegisterViewSet.code
        serializer = CodeSerializer(data=request.data, context={'code': code})
        print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

