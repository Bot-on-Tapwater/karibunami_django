from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

def home_page(request):
    return HttpResponse("Default landing/home page")

@require_http_methods(["GET", "POST"])
@csrf_exempt
def register_user(request):
    if request.method =="GET":
        return
    return HttpResponse("Register User Accounts")

def verify_user(request):
    return HttpResponse("Verify User Accounts")

@require_http_methods(["GET", "POST"])
@csrf_exempt
def resend_link(request):
    return HttpResponse("Resend verification link to user")

@require_http_methods(["GET", "POST"]) # Consider using a PUT request instead
@csrf_exempt
def reset_password(request):
    return HttpResponse("Reset User Accounts Passwords")

@require_http_methods(["GET", "POST"])
@csrf_exempt
def reset_password_link(request):
    return HttpResponse("Helper function for 'reset_password'")

@require_http_methods(["GET", "POST"])
@csrf_exempt
def login(request):
    return HttpResponse("Login User Accounts")

def logout(request):
    return HttpResponse("Logout User Accounts")

@require_http_methods(["POST"])
@csrf_exempt
def get_places(request):
    return HttpResponse("Return results for nearby places")

@require_http_methods(["GET"])
def get_place_details(request, place_id: str):
    return HttpResponse("Return more details about a specific place using google place id ")

@require_http_methods(["PUT"])
@csrf_exempt
def bookmark_place(request, place_id: str):
    return HttpResponse("Allows user to bookmark a place for future reference")

@require_http_methods(["GET"])
def bookmarked_places(request):
    return HttpResponse("Return places that a signed in user has bookmarked")

'''CSRF TOKEN'''
from django.http import JsonResponse

def get_csrf_token(request):
    csrf_token = request.COOKIES.get('csrftoken', '')
    return JsonResponse({'csrf_token': csrf_token})

