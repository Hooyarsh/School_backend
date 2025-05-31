from django.urls import path
from .views import elementary_form, middle_form, high_form, submit_invoice, api_home
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('', api_home),
    path('form/elementary/', elementary_form),
    path('form/middle/', middle_form),
    path('form/high/', high_form),
    path('submit-invoice/', submit_invoice),
    path("api/submit-invoice/", views.submit_invoice, name="submit_invoice"),
]
