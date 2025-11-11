from rest_framework.response import Response

def success_response(data=None, message="Opération réussie", status=200):
    return Response({
        'suscess': True,
        'message': message,
        'data': data
    }, status=status)


def error_response(message="Erreur lors de l'opération", status=400):
    return Response({
        'success': False,
        'message': message,
        'data': None
    }, status=status)