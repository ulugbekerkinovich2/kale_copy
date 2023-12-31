from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from common.product.models import Product
from common.users.base import BaseModel

User = get_user_model()


class CheckoutProductStatus(models.IntegerChoices):
    PENDING = 1, "PENDING"
    WAITING = 2, "WAITING"
    CLOSED = 3, "CLOSED"


class OrderStatus(models.IntegerChoices):
    PENDING = 1, "PENDING"
    WAITING = 2, "WAITING"
    ORDERED = 3, "ORDERED"


class OrderedProductStatus(models.IntegerChoices):
    PENDING = 1, "PENDING"
    WAITING = 2, "WAITING"
    DELIVERED = 3, "DELIVERED"
    CANCELED = 4, "CANCELED"
    IN_PROGRESS = 5, "IN_PROGRESS"


class Cart(BaseModel):
    user = models.ForeignKey(User, related_name='userCart', on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return self.user.name


class CartProduct(BaseModel):
    cart = models.ForeignKey(Cart, related_name='cartCartProduct', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cartProduct', on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)
    orderPrice = models.FloatField(default=0)

    @property
    def add(self):
        self.quantity = self.quantity + 1
        self.orderPrice = self.quantity * self.product.price * (1 - self.product.discount / 100)
        self.save()

    @property
    def sub(self):
        if self.quantity > 1:
            self.quantity = self.quantity - 1
            self.orderPrice = self.quantity * self.product.price * (1 - self.product.discount / 100)
            self.save()

    @property
    def basePrice(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"Cart #{self.cart.id} {self.product.title} {self.quantity}"


class PaymentTypes(models.IntegerChoices):
    CASH = 0, "CASH"
    PAYME = 1, "PAYME"
    CLICK = 2, "CLICK"
    UZUM = 3, "UZUM"


class Checkout(BaseModel):
    user = models.ForeignKey(User, related_name='userCheckout', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, related_name='checkoutCartProduct', blank=True)
    paymentType = models.IntegerField(choices=PaymentTypes.choices, default=PaymentTypes.CASH)
    installation = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)
    isNewAddress = models.BooleanField(default=False)
    region = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)

    @property
    def amount(self):
        return sum(map(lambda i: i.product.price * i.quantity, self.products.select_related('cart', 'product').all()))

    def __str__(self):
        return f"Order #{self.id} User: {self.user.phone}"


class Order(BaseModel):
    checkout = models.ForeignKey(Checkout, related_name='checkoutOrder', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orderedProduct', on_delete=models.SET_NULL, null=True,
                                blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    totalAmount = models.FloatField(default=0)
    isDelivery = models.BooleanField(default=False)
    orderedTime = models.DateTimeField(default=timezone.now)
    deliveredTime = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=OrderedProductStatus.choices, default=OrderStatus.PENDING)

    def __str__(self):
        return f"Order #{self.id} Status: {self.status}"


class Wishlist(BaseModel):
    user = models.ForeignKey(User, related_name='userWishlist', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlistProducts', blank=True)

    def __str__(self):
        return self.user.name


class Comparison(BaseModel):
    user = models.ForeignKey(User, related_name='userComparison', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='comparisonProducts', blank=True)

    def __str__(self):
        return self.user.name
