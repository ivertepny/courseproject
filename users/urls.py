# Мій файл urls

from django.urls import path

from users.views import login, registration

app_name = 'users' # Не зрозумів для чого

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
]

