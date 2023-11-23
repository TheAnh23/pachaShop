from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Banner,Category,Brand,Color,Size,Product,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook,Image

# admin.site.register(Banner)
admin.site.register(Brand)
admin.site.register(Size)


class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

class CategoryAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')
admin.site.register(Category,CategoryAdmin)

class ColorAdmin(admin.ModelAdmin):
	list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','category','brand','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Product,ProductAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag')
admin.site.register(Image, ImageAdmin)

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'color', 'size', 'display_images')
    def display_images(self, obj):
        return mark_safe(' '.join([image.image_tag() for image in obj.images.all()]))
admin.site.register(ProductAttribute, ProductAttributeAdmin)

# Order
class CartOrderAdmin(admin.ModelAdmin):
	list_editable=('paid_status','order_status')
	list_display=('user','total_amt','paid_status','order_dt','order_status')
admin.site.register(CartOrder,CartOrderAdmin)

class CartOrderItemsAdmin(admin.ModelAdmin):
	list_display=('invoice_no','item','image_tag','qty','price','total')
admin.site.register(CartOrderItems,CartOrderItemsAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)


admin.site.register(Wishlist)


class UserAddressBookAdmin(admin.ModelAdmin):
	list_display=('user','address','status')
admin.site.register(UserAddressBook,UserAddressBookAdmin)