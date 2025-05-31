# invoices/models.py
from django.db import models
from django_jalali.db import models as jmodels

class Student(models.Model):
    national_id = models.CharField(max_length=10, unique=True)
    grade = models.CharField(max_length=10)
    subgroup = models.CharField(max_length=50)
    register_date = jmodels.jDateTimeField()
    deregister_date = jmodels.jDateTimeField()
    tan_khah_total = models.FloatField(default=0)

class TanKhahEntry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

class StdEntry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    invoice_tag = models.CharField(max_length=50)

class Invoice(models.Model):
    objects = jmodels.jManager()
    invoice_number = models.CharField(max_length=20)
    invoice_date = models.DateTimeField(null = True)
    total_amount = models.BigIntegerField()
    supplier_details = models.TextField()
    description = models.TextField(blank=True, null=True)
    submit_timestamp = models.DateTimeField(auto_now_add=True)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    count = models.IntegerField()
    level = models.CharField(max_length=20)
    invoice_type = models.CharField(max_length=50)
    subgroup_language = models.CharField(max_length=50, blank=True, null=True)
    student_national_id = models.CharField(max_length=10, blank=True, null=True)
    category = models.CharField(max_length=100)
    sub_code = models.CharField(max_length=100)
    detail_code = models.CharField(max_length=100)
    other_detail_code = models.CharField(max_length=255, blank=True, null=True)
    unit_price = models.BigIntegerField()
    matched_student_count = models.IntegerField(default=0)
    price_per_person = models.FloatField(default=0)


# invoices/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice, InvoiceItem, Student, TanKhahEntry, StdEntry
from django.utils.dateparse import parse_date
from django.db import transaction

def format_id(id_str):
    return str(id_str).zfill(10)

@api_view(['POST'])
@transaction.atomic
def submit_invoice(request):
    data = request.data

    invoice = Invoice.objects.create(
        invoice_number=data.get('invoiceNumber'),
        #invoice_date=parse_date(data.get('invoiceDate')),
        total_amount=data.get('totalAmount'),
        supplier_details=data.get('finalSupplierDetails'),
        description=data.get('finalDescription')
    )

    for i, item in enumerate(data.get('items', []), start=1):
        count = int(item.get('count', 0))
        unit_price = int(item.get('unitPrice', 0))
        level = item.get('level')
        invoice_type = item.get('invoiceType')
        subgroup = item.get('subgroupLanguage', '')
        national_id = format_id(item.get('nationalID', ''))
        matched_students = []

        students = Student.objects.filter(grade=level)

        if invoice_type == 'فردی':
            students = students.filter(national_id=national_id)
        elif invoice_type == 'زیرگروه زبان':
            students = students.filter(subgroup=subgroup)

        #students = students.filter(
        #    register_date__lte=invoice.invoice_date,
        #    deregister_date__gte=invoice.invoice_date
        #)

        matched_count = students.count()
        price_per_person = (count * unit_price / matched_count) if matched_count > 0 else 0

        for student in students:
            # Update TanKhah total
            student.tan_khah_total += price_per_person
            student.save()

            # Add entry to TanKhah table
            TanKhahEntry.objects.create(
                student=student,
                value=price_per_person,
                description=f"{invoice.invoice_number}-{i}"
            )

            # Add invoice entry in STD table
            StdEntry.objects.create(
                student=student,
                invoice_tag=f"{invoice.invoice_number}-{i}"
            )

        InvoiceItem.objects.create(
            invoice=invoice,
            count=count,
            unit_price=unit_price,
            level=level,
            invoice_type=invoice_type,
            subgroup_language=subgroup,
            student_national_id=national_id,
            category=item.get('category'),
            sub_code=item.get('subCode'),
            detail_code=item.get('detailCode'),
            other_detail_code=item.get('otherDetailCode'),
            matched_student_count=matched_count,
            price_per_person=price_per_person
        )

    return Response({'message': 'Invoice successfully submitted.'}, status=status.HTTP_201_CREATED)
