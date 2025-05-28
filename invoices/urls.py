from django.urls import path
from .views import elementary_form, middle_form, high_form, submit_invoice

urlpatterns = [
    path('form/elementary/', elementary_form),
    path('form/middle/', middle_form),
    path('form/high/', high_form),
    path('submit-invoice/', submit_invoice),
]
