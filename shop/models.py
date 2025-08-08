from django.db import models
from django.contrib.auth.models import User  # For linking CartItem to a user

# ------------------------
# Category Model
# ------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ------------------------
# Product Model
# ------------------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')  # stored in MEDIA folder
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    # ------------------------
# Cart Item Model
# ------------------------
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # One user can have many cart items
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Linked product
    quantity = models.PositiveIntegerField(default=1)  # Must be >= 1

    def total_price(self):
        """Calculate total price for this cart item."""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"