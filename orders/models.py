from django.db import models
from accounts.models import Account
from store.models import Product, Variation
# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=50)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        
        return self.payment_id
    
class Order(models.Model):
        STATUS = (
            ('Nuevo', 'Nuevo'),
            ('Aceptedado', 'Aceptedado'),
            ('Completado', 'completado'),
            ('Cancelado', 'Cancelado'),
        )
        user = models.ForeignKey(Account, on_delete=models.CASCADE)
        payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
        order_number = models.CharField(max_length=20, unique=True)
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        phone = models.CharField(max_length=15)
        email = models.EmailField(max_length=100)
        address_line_1 = models.CharField(max_length=100)
        address_line_2 = models.CharField(max_length=100, blank=True)
        country = models.CharField(max_length=50)
        state = models.CharField(max_length=50)
        city = models.CharField(max_length=50)
        order_note = models.TextField(blank=True)
        order_total = models.DecimalField(max_digits=10, decimal_places=2)
        tax = models.DecimalField(max_digits=10, decimal_places=2)
        status = models.CharField(max_length=20, choices=STATUS, default='Nuevo')
        ip = models.GenericIPAddressField(blank=True, null=True)
        is_ordered = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def full_name(self):
            return f'{self.first_name} {self.last_name}'
        def full_address(self):
            return f'{self.address_line_1} {self.address_line_2}'
        def __str__(self):
            return self.user.first_name
        

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        
        return self.product.product_name