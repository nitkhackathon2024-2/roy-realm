from django.urls import path
from .views import register_view, login_view, logout_view, profile_view, home_view

urlpatterns = [
    # Home page
    path('', home_view, name='home'),

    # Registration page
    path('register/', register_view, name='user-register'),

    # Login page
    path('login/', login_view, name='user-login'),

    # Logout page
    path('logout/', logout_view, name='user-logout'),

    # Profile page (for logged-in users)
    path('profile/', profile_view, name='user-profile'),
]
