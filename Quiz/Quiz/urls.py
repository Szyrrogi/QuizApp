from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView  # Dodaj ten import
from accounts.views import CustomLoginView, SignUpView

handler404 = 'quizzes.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ścieżki autentykacji
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Aplikacja quizzes
    path('', include('quizzes.urls')),
]