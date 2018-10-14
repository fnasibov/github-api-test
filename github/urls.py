from django.urls import path

from github.views import show_issues

urlpatterns = [
    path('', show_issues, name='home')
]
