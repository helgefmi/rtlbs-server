def response_payload_handler(token, user, request):
    return {
        'token': token,
        'player': {
            'id': user.id,
            'username': user.username,
        },
    }
