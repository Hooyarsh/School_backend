from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import InvoiceSerializer
from rest_framework.views import APIView
import re


@api_view(['POST'])
def submit_invoice(request):
    cleaned_data = clean_json(request.data)
    serializer = InvoiceSerializer(data=cleaned_data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Invoice saved successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def elementary_form(request):
    return render(request, 'invoices/ElementarySchoolInvoiceForm.html')

def middle_form(request):
    return render(request, 'invoices/MiddleSchoolInvoiceForm.html')

def high_form(request):
    return render(request, 'invoices/HighSchoolInvoiceForm.html')

def api_home(request):
    return render(request, 'invoices/api_home.html')

class InvoiceSubmitView(APIView):
    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def clean_string(s):
    if not isinstance(s, str):
        return s
    # Remove invisible/control unicode characters and non-breaking spaces
    return re.sub(r'[\u200c\u200e\u202c\u202d\u202e\uFEFF\u2007\u2000\xa0]', '', s)

def clean_json(data):
    if isinstance(data, dict):
        return {k: clean_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_json(i) for i in data]
    elif isinstance(data, str):
        return clean_string(data)
    else:
        return data
