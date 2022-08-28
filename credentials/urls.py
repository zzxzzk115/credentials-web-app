from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_handler, name='index'),
    path('CGI-BIN/PDFCGI2.pgm', views.pdfcgi2_handler, name='PDFCGI2'),
    path('CGI-BIN/SendEmail', views.send_email_handler, name='send_email')
]