from django.http import JsonResponse

def api_home(request):
    return JsonResponse({"message": "Welcome to the USTP Commerce API!"})

def protected_view(request):
    firebase_user = getattr(request, 'firebase_user', None)
    if not firebase_user:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    return JsonResponse({'message': f'Hello {firebase_user["email"]}, you are authenticated!'})

def login_or_register(request):
    firebase_user = getattr(request, 'firebase_user', None)
    if not firebase_user:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    uid = firebase_user['uid']
    email = firebase_user['email']

    user, created = UserProfile.objects.get_or_create(uid=uid, defaults={
        'email': email,
        'full_name': firebase_user.get('name', 'Anonymous')
    })

    return JsonResponse({'message': 'Login successful', 'user': {
        'email': user.email,
        'full_name': user.full_name,
        'created': user.created_at
    }})
