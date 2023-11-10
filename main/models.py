from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.

class Cart(models.Model):

    # Each User has a Singular Cart, hence why I used a OneToOne Field. One User has One Field.

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Product', through='CartItem')


    def __str__(self):
        return f"{self.user.username} Cart"
    
class Product(models.Model):

    # But a User can have multiple products. So I used a OneToMany Field, in dJango it is achieved through a ForeignKey.

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name

# This is the code that deletes the image file associated with the Product
@receiver(pre_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    # Delete the image file associated with the Product
    if instance.image:
        instance.image.delete(False)  # Passing False ensures that the file is deleted from storage

# Connect the signal handler
pre_delete.connect(delete_product_image, sender=Product)

# For a Singular Cart Item
class CartItem(models.Model):
    # Use a ForeignKey for a Cart. Each Cart can have many CartItems.
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart}"

# For an Order
class Order(models.Model):
    # Use a ForeignKey for a User. Each User can have many Orders
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Use a ManyToManyField for a Product. Each Order can have many Products
    products = models.ManyToManyField(Product, through='OrderItem')
    

    def __str__(self):
        return f"{self.user.username}'s Order"

# For an Singular Order Item
class OrderItem(models.Model):
    # Use a ForeignKey for an Order. Each Order can have many OrderItems
    # Use a ForeignKey for a Product. Each OrderItem can have one Product

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.order}"
