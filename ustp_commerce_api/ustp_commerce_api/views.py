from django.shortcuts import render

from django.http import JsonResponse

def api_home(request):
    return JsonResponse({"message": "Welcome to the USTP Commerce API!"})  

