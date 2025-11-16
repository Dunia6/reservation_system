from datetime import datetime, timezone
from django.conf import settings


def set_refresh_cookie(response, refresh_token):
    """ Set the refresh token in an HttpOnly cookie. """
    expire_time = datetime.now(timezone.utc) + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        expires=expire_time,
        httponly=True,
        secure=settings.DEBUG is False,  # True en production, False en développement
        samesite='Lax',  # 'Lax' pour développement local, 'None' avec secure=True pour HTTPS
        path='/',  # Disponible sur tout le site
    )


def delete_refresh_cookie(response):
    """ Delete the refresh token cookie. """
    response.delete_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        path='/',
        samesite='Lax'
    )