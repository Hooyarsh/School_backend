from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import InvoiceSerializer

@api_view(['POST'])
def submit_invoice(request):
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Invoice saved successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render

def elementary_form(request):
    return render(request, 'invoices/ElementarySchoolInvoiceForm.html')

def middle_form(request):
    return render(request, 'invoices/MiddleSchoolInvoiceForm.html')

def high_form(request):
    return render(request, 'invoices/HighSchoolInvoiceForm.html')

