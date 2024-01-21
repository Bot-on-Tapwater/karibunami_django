from django.urls import path
from . import views

app_name = "karibunami"
urlpatterns = [
    # ex: /karibunami/
    path("", views.index, name="index"),
    # ex: /karibunami/verify_user
    # path("verify_user", views.verify_user, name="verify"),
    # ex: /karibunami/register
    # path("register", views.register_user, name="register"),
    # ex: /karibunami/reset_password
    # path("reset_password", views.reset_password, name="reset"),
    # ex: /karibunami/reset_password_link
    # path("reset_password_link", views.reset_password_link, name="password_link"),
    # ex: /karibunami/login
    path("login", views.login, name="login"),
    # ex /karibunami/place
    path("place", views.get_places, name='places'),
    # ex /karibunami/place/27
    path("place/<str:place_id>", views.get_place_details, name='place_details'),
    # ex /karibunami/saved_places
    path("saved_places", views.bookmarked_places, name="bookmarks"),
    # ex /karibunami/bookmark/<place_id>
    path("bookmark/<str:place_id>", views.bookmark_place, name="bookmark"),
    # ex /karibunami/logout
    path("logout", views.logout, name="logout"),
    # ex /karibunami/csrf
    path("csrf", views.get_csrf_token),
    # ex /karibunami/callback
    path("callback", views.callback, name="callback"),
]