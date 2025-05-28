from django.db import models

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20)
    invoice_date = models.DateField()
    total_amount = models.BigIntegerField()
    supplier_details = models.TextField()
    description = models.TextField(blank=True, null=True)
    submit_timestamp = models.DateTimeField(auto_now_add=True)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    count = models.IntegerField()
    level = models.CharField(max_length=20)
    invoice_type = models.CharField(max_length=50)
    subgroup_language = models.CharField(max_length=10, blank=True, null=True)
    student_national_id = models.CharField(max_length=10, blank=True, null=True)
    category = models.CharField(max_length=100)
    sub_code = models.CharField(max_length=100)
    detail_code = models.CharField(max_length=100)
    other_detail_code = models.CharField(max_length=255, blank=True, null=True)
    unit_price = models.BigIntegerField()
