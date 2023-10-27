from rest_framework import status


INTERNER_ERROR = {
    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    "message": "Interner Error",
}
