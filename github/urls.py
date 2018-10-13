from django.urls import path

from github.views import homePageView

urlpatterns = [
    path('', homePageView, name='home')
]
