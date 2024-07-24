import hashlib
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Dummy data for demonstration purposes
users = {
    "908484157": {
        "sub_status": "trial",
        "first_name": "Haitham",
        "is_subscribed": False
    }
}

link_mapping = {}

@csrf_exempt
def short(request):
    link = request.GET.get('link')
    username = request.GET.get('username')
    first_name = request.GET.get('first_name')
    chat_id = request.GET.get('chat_id')

    # Generate a shortened link code
    short_code = hashlib.md5(link.encode()).hexdigest()[:6]

    # Store the mapping from short_code to original link
    link_mapping[short_code] = link

    # Generate the shortened link using the server's address
    shortened_link = f"http://127.0.0.1:8000/{short_code}/"

    return JsonResponse({'status': 'success', 'shortened_link': shortened_link})

def redirect_to_link(request, short_code):
    # Retrieve the original link from the mapping
    original_link = link_mapping.get(short_code)
    if original_link:
        return HttpResponseRedirect(original_link)
    else:
        return JsonResponse({'status': 'error', 'message': 'Link not found'}, status=404)

@csrf_exempt
def check_user(request):
    chat_id = request.GET.get('chat_id')
    user = users.get(chat_id)
    if user:
        return JsonResponse({'sub_status': user['sub_status']})
    else:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

@csrf_exempt
def subscribe(request):
    user_id = request.GET.get('user_id')
    first_name = request.GET.get('first_name')

    user = users.get(user_id)
    if user:
        user['is_subscribed'] = True
        user['sub_status'] = 'subscribed'
        return JsonResponse({'status': 'success', 'message': f'Thank you {first_name} for subscribing!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
