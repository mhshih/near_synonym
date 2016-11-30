from django.conf.urls import url

from . import views

urlpatterns = [
    url('(?P<governor>.+)', views.home, name='home'),
]
