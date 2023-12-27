from django.db import models
# from djongo import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.utils import timezone
import requests

# Banner
class Banner(models.Model):
    media = models.FileField(upload_to="banner_media/",null=True)
    alt_text = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'Banners'

    def display_media(self):
        if self.media:
            if self.media.name.endswith('.mp4'):
                return mark_safe(f'<video width="100%" loop autoplay controlslist="nodownload"><source src="{self.media.url}" type="video/mp4"></video>')
            elif self.media.name.endswith(('.webp','.jpg')):
                return mark_safe(f'<img src="{self.media.url}" style="width: 100%;" />')
        return "No media"

    def __str__(self):
        return self.alt_text

# Category
class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_imgs/")

    class Meta:
        verbose_name_plural='Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

# Brand
class Brand(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.title

# Color
class Color(models.Model):
    title=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Colors'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title

# Collection
class Collection(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Collections'

    def __str__(self):
        return self.title
    
# Size
class Size(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Sizes'

    def __str__(self):
        return self.title


# Product Model
class Product(models.Model):
    title=models.CharField(max_length=200)
    slug=models.CharField(max_length=400)
    detail=models.TextField(default='')
    ingredient=models.TextField(default='')
    using=models.TextField(default='')
    benefit=models.TextField(default='')
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    collection=models.ManyToManyField(Collection)
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='Products'

    def __str__(self):
        return self.title

# Image
class Image(models.Model):
    image = models.ImageField(upload_to="product_imgs/")

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

# Product Attribute
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveBigIntegerField(default=0)
    images = models.ManyToManyField(Image)

    class Meta:
        verbose_name_plural = 'ProductAttributes'

    def __str__(self):
        return self.product.title

# AddressBook
class UserAddressBook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    email=models.CharField(max_length=100, null=True)
    phone=models.CharField(max_length=100, null=True)
    recipient=models.CharField(max_length=100, null=True)
    province = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    ward = models.CharField(max_length=100, null=True)
    street=models.CharField(max_length=200, null=True)
    note=models.CharField(max_length=200, null=True)
    status=models.BooleanField(default=True)

    class Meta:
        verbose_name_plural='Address Book'

# Shipment
class Shipment(models.Model):
    image = models.ImageField(upload_to="ship_imgs/", null=True, blank=True)
    title = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=200,null=True)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural='Shipment'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

# Payment
class Payment(models.Model):
    image = models.ImageField(upload_to="payment_imgs/", null=True, blank=True)
    title = models.CharField(max_length=200,null=True)

    class Meta:
        verbose_name_plural='Payment'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title
    
# Order
status_choice=(
        ('process','In Process'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
    )
class CartOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey(UserAddressBook,on_delete=models.CASCADE,null=True)
    shipment=models.ForeignKey(Shipment,on_delete=models.CASCADE,null=True)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,null=True)
    total_amt=models.FloatField()
    paid_status=models.BooleanField(default=False)
    order_dt=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(choices=status_choice,default='process',max_length=150)

    class Meta:
        verbose_name_plural='Orders'

# OrderItems
class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=150)
    item=models.CharField(max_length=150)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()

    class Meta:
        verbose_name_plural='Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

# Blog List
class BlogList(models.Model):
    image = models.ImageField(upload_to="blog_imgs/", null=True, blank=True)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='Blog List'

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

# Product Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='Reviews'

    def get_review_rating(self):
        return self.review_rating

# WishList
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Wishlist'

# Contact
class Contact(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100)
    message=models.TextField()

    class Meta:
        verbose_name_plural='Contact'

class Voucher(models.Model):
    code = models.CharField(max_length=10,null=True)
    detail = models.CharField(max_length=150, null=True)
    discount_percent = models.IntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    class Meta:
            verbose_name_plural='Voucher'

    def is_valid(self):
        from django.utils import timezone
        return self.valid_from <= timezone.now() <= self.valid_to

    def __str__(self):
        return self.code

    




    