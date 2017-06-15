from django.conf.urls import url
from . import views

app_name = 'ide'

urlpatterns = [

    url(r'^$', views.ide, name='ide'),
    url(r'^compile-and-run/$', views.compile_and_run),

]