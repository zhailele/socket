from django.shortcuts import render

def chat(request):
    return render(request, 'chat/index.html')

def socket(request):
    return render(request, 'chat/socket.html')

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import HttpResponse

from .models import User

class Test_demo(APIView):
    def get(self, request):
        name = request.GET.get("name")
        print(name)
        user = User.objects.filter(id=5).first().name
        print(user)

        a = User.objects.only("name")
        print("only----->",a)
        # user.name = name
        # user.save()
        return HttpResponse("ok")

