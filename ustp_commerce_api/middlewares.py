from django.http import JsonResponse
from firebase_admin import auth
import json

def firebase_token_required(get_response):
    def middleware(request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'No authentication token provided'}, status=401)

        token = auth_header.split('Bearer ')[1]

        try:
            decoded_token = auth.verify_id_token(token)
            request.firebase_user = decoded_token  # Attach user data to request
        except Exception as e:
            return JsonResponse({'error': f'Invalid or expired token: {str(e)}'}, status=401)

        return get_response(request)

    return middleware
