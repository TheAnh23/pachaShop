from pyexpat.errors import messages
from django.shortcuts import render,redirect
import requests
from django.http import JsonResponse,HttpResponse
from .models import Banner,Category,Brand,Product,Collection,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook,BlogList,Shipment,Payment,Voucher
from django.db.models import Max,Min,Count,Avg
from django.db.models.functions import ExtractMonth, ExtractDay
from django.template.loader import render_to_string
from .forms import SignupForm,ReviewAdd,AddressBookForm,ProfileForm,VoucherForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
# Home Page
def home(request):
	banners=Banner.objects.all().order_by('-id').reverse()
	collection_new=Collection.objects.get(id=2)
	data = Product.objects.filter(collection=collection_new, is_featured=True).order_by('-id')
	for product in data:
		product_reviews = ProductReview.objects.filter(product=product)
		avg_rating = product_reviews.aggregate(avg_rating=Avg('review_rating'))['avg_rating']
		star = round(avg_rating) if avg_rating else 5.0
		product.avg_rating = round(avg_rating, 1) if avg_rating else 5.0
		product.star = star
		price_discount = int(round(product.productattribute_set.first().price * (100 + product.productattribute_set.first().discount)/100,0))
		price_discount = format(price_discount,",").replace(',', '.')
		product.discount = price_discount

	category=Category.objects.order_by('-id')
	category_1=Category.objects.order_by('-id').reverse()[:3]
	category_2=Category.objects.order_by('-id').reverse()[3:]

	collection_hot=Collection.objects.get(id=1)
	hot_products=Product.objects.filter(collection=collection_hot, is_featured=True).order_by('-id')
	for product in hot_products:
		product_reviews = ProductReview.objects.filter(product=product)
		avg_rating = product_reviews.aggregate(avg_rating=Avg('review_rating'))['avg_rating']
		star = round(avg_rating) if avg_rating else 5.0
		product.avg_rating = round(avg_rating, 1) if avg_rating else 5.0
		product.star = star
		price_discount = int(round(product.productattribute_set.first().price * (100 + product.productattribute_set.first().discount)/100,0))
		price_discount = format(price_discount,",").replace(',', '.')
		product.discount = price_discount

	return render(request,'index.html',{'data':data,'banners':banners,'category_1':category_1,'category_2':category_2,'category':category,'hot_products':hot_products})
# About us
def about_us(request):
	category=Category.objects.order_by('-id')
	return render(request, 'aboutus.html', {'category': category})
# Blog list
def blog_list(request):
	category=Category.objects.order_by('-id')
	blog_list = BlogList.objects.all()
	return render(request, 'blog_list.html', {'blog_list': blog_list, 'category':category})
# Blog detail
def blog_detail(request):
	category=Category.objects.order_by('-id')
	return render(request, 'blog_detail.html', {'category': category})
# Contact
def contact(request):
	category=Category.objects.order_by('-id')
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data['user']
			message = form.cleaned_data['message']
			from_email = form.cleaned_data['email']
			recipient_list = [settings.EMAIL_HOST_USER]
			send_mail(user, message, from_email, recipient_list)
			return redirect('contact')
	else:
		form = ContactForm()
	return render(request, 'contact.html', {'form': form, 'category': category})
# Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data})

# Brand
def brand_list(request):
    data=Brand.objects.all().order_by('-id')
    return render(request,'brand_list.html',{'data':data})

# Product List
def product_list(request):
	total_data=Product.objects.count()
	category=Category.objects.order_by('-id')
	data=Product.objects.all().order_by('-id')[:9]
	for product in data:
		product_reviews = ProductReview.objects.filter(product=product)
		avg_rating = product_reviews.aggregate(avg_rating=Avg('review_rating'))['avg_rating']
		star = round(avg_rating) if avg_rating else 5.0
		product.avg_rating = round(avg_rating, 1) if avg_rating else 5.0
		product.star = star
		price_discount = int(round(product.productattribute_set.first().price * (100 + product.productattribute_set.first().discount)/100,0))
		price_discount = format(price_discount,",").replace(',', '.')
		product.discount = price_discount
	min_price=ProductAttribute.objects.aggregate(Min('price'))
	max_price=ProductAttribute.objects.aggregate(Max('price'))
	return render(request,'product_list.html',
		{
			'data':data,
			'total_data':total_data,
			'min_price':min_price,
			'max_price':max_price,
			'category':category
		}
		)

# Product List According to Category
def category_product_list(request,cat_id):
	categories=Category.objects.order_by('-id')
	category=Category.objects.get(id=cat_id)
	data=Product.objects.filter(category=category).order_by('-id')
	for product in data:
		product_reviews = ProductReview.objects.filter(product=product)
		avg_rating = product_reviews.aggregate(avg_rating=Avg('review_rating'))['avg_rating']
		star = round(avg_rating) if avg_rating else 5.0
		product.avg_rating = round(avg_rating, 1) if avg_rating else 5.0
		product.star = star
		price_discount = int(round(product.productattribute_set.first().price * (100 + product.productattribute_set.first().discount)/100,0))
		price_discount = format(price_discount,",").replace(',', '.')
		product.discount = price_discount
	return render(request,'category_product_list.html',{
			'data':data, 'category':categories
			})

# Product List According to Brand
def brand_product_list(request,brand_id):
	brand=Brand.objects.get(id=brand_id)
	data=Product.objects.filter(brand=brand).order_by('-id')
	return render(request,'category_product_list.html',{
			'data':data,
			})

# Product Detail
def product_detail(request,slug,id):
	product=Product.objects.get(id=id)
	category=Category.objects.order_by('-id')
	related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
	for product in related_products:
		product_reviews = ProductReview.objects.filter(product=product)
		avg_rating = product_reviews.aggregate(avg_rating=Avg('review_rating'))['avg_rating']
		star = round(avg_rating) if avg_rating else 5.0
		product.avg_rating = round(avg_rating, 1) if avg_rating else 5.0
		product.star = star
		price_discount = int(round(product.productattribute_set.first().price * (100 + product.productattribute_set.first().discount)/100,0))
		price_discount = format(price_discount,",").replace(',', '.')
		product.discount = price_discount
	colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
	sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__title','price','color__id').distinct()
	reviewForm=ReviewAdd()
	
	price_discount = int(round(product.productattribute_set.first().price * (100 + product.productattribute_set.first().discount)/100,0))
	price_discount = format(price_discount,",").replace(',', '.')

	# Check
	canAdd=True
	reviewCheck=ProductReview.objects.filter(user=request.user,product=product).count()
	if request.user.is_authenticated:
		if reviewCheck > 0:
			canAdd=False
	# End

	# Fetch reviews
	reviews=ProductReview.objects.filter(product=product)
	# End

	# Fetch avg rating for reviews
	avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	if avg_reviews['avg_rating'] is None or avg_reviews['avg_rating'] == 0:
			avg_reviews['avg_rating'] = 5.0
	avg_reviews['avg_rating'] = round(avg_reviews['avg_rating'],1)
	star = round(avg_reviews['avg_rating'])

	count_review = ProductReview.objects.filter(product=product).count()

	if count_review > 0:
		count_reviews = str(count_review)+ ' bình luận'
	else:
		count_reviews = "Trở thành người bình luận đầu tiên"
	# End

	return render(request, 'product_detail.html',{'data':product,'related':related_products,'colors':colors,'sizes':sizes,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews,'count_reviews':count_reviews, 'star':star,'category':category,'price_discount':price_discount})

# Search
def search(request):
	category=Category.objects.order_by('-id')
	q=request.GET['q']
	data=Product.objects.filter(title__icontains=q).order_by('-id')
	for product in data:
		product_reviews = ProductReview.objects.filter(product=product)
		avg_rating = product_reviews.aggregate(avg_rating=Avg('review_rating'))['avg_rating']
		star = round(avg_rating) if avg_rating else 5.0
		product.avg_rating = round(avg_rating, 1) if avg_rating else 5.0
		product.star = star
		price_discount = int(round(product.productattribute_set.first().price * (100 + product.productattribute_set.first().discount)/100,0))
		price_discount = format(price_discount,",").replace(',', '.')
		product.discount = price_discount
	return render(request,'search.html',{'data':data, 'category': category})

# Filter Data
def filter_data(request):
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	collections=request.GET.getlist('collection[]')
	sizes=request.GET.getlist('size[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	allProducts=Product.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(productattribute__price__gte=minPrice)
	allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
	if len(colors)>0:
		allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(category__id__in=categories).distinct()
	if len(collections)>0:
		allProducts=allProducts.filter(collection__id__in=collections).distinct()
	if len(sizes)>0:
		allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
	for product in allProducts:
		product_reviews = ProductReview.objects.filter(product=product)
		avg_rating = product_reviews.aggregate(avg_rating=Avg('review_rating'))['avg_rating']
		star = round(avg_rating) if avg_rating else 5.0
		product.avg_rating = round(avg_rating, 1) if avg_rating else 5.0
		product.star = star
		price_discount = int(round(product.productattribute_set.first().price * (100 + product.productattribute_set.first().discount)/100,0))
		price_discount = format(price_discount,",").replace(',', '.')
		product.discount = price_discount
	t=render_to_string('ajax/product-list.html',{'data':allProducts})
	return JsonResponse({'data':t})

# Load More
def load_more_data(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data=Product.objects.all().order_by('-id')[offset:offset+limit]
	for product in data:
		product_reviews = ProductReview.objects.filter(product=product)
		avg_rating = product_reviews.aggregate(avg_rating=Avg('review_rating'))['avg_rating']
		star = round(avg_rating) if avg_rating else 5.0
		product.avg_rating = round(avg_rating, 1) if avg_rating else 5.0
		product.star = star
		price_discount = int(round(product.productattribute_set.first().price * (100 + product.productattribute_set.first().discount)/100,0))
		price_discount = format(price_discount,",").replace(',', '.')
		product.discount = price_discount
	t=render_to_string('ajax/product-list.html',{'data':data})
	return JsonResponse({'data':t}
)

# Add to cart
def add_to_cart(request):
	# del request.session['cartdata']
	cart_p={}
	cart_p[str(request.GET['id'])]={
		'image':request.GET['image'],
		'title':request.GET['title'],
		'qty':request.GET['qty'],
		'price':request.GET['price'],
	}
	if 'cartdata' in request.session:
		if str(request.GET['id']) in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
			cart_data.update(cart_data)
			request.session['cartdata']=cart_data
		else:
			cart_data=request.session['cartdata']
			cart_data.update(cart_p)
			request.session['cartdata']=cart_data
	else:
		request.session['cartdata']=cart_p
	return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

# Cart List Page
def cart_list(request):
	total_amt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			if item['price']:
				total_amt+=int(item['qty'])*float(item['price'])
			else:
				total_amt+=0
		return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	else:
		return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})


# Delete Cart Item
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		if item['price']:
				total_amt+=int(item['qty'])*float(item['price'])
		else:
			total_amt+=0
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Update Cart Item
def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		if item['price']:
				total_amt+=int(item['qty'])*float(item['price'])
		else:
			total_amt+=0
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Signup Form
def signup(request):
	if request.method=='POST':
		form=SignupForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			pwd=form.cleaned_data.get('password1')
			user=authenticate(username=username,password=pwd)
			login(request, user)
			return redirect('home')
	else:
		form=SignupForm
	return render(request, 'registration/signup.html',{'form':form})


# Checkout
from django.shortcuts import render, redirect
from .forms import AddressBookForm  # Make sure to import your AddressBookForm

@login_required
def checkout(request):
    total_amt = 0
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            saveForm.save()
            msg = 'Địa chỉ đã được lưu'
        else:
            # Handle the case where the form is not valid
            # You might want to add some logic here, e.g., log errors or provide additional context
            pass
    else:
        form = AddressBookForm()  # Instantiate the form here

    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty']) * float(item['price'])
        
        # Order
        order = CartOrder.objects.create(
            user=request.user,
            total_amt=total_amt,
			address = UserAddressBook.objects.filter(user=request.user, status=True).first(),
			shipment = Shipment.objects.first(),
			payment = Payment.objects.first(),
        )
        # End

        for p_id, item in request.session['cartdata'].items():
            # total_amt += int(item['qty']) * float(item['price'])
            # OrderItems
            items = CartOrderItems.objects.create(
                order=order,
                invoice_no='INV-' + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            )
            # End
			 
    return render(request, 'checkout.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt, 'form': form, 'msg': msg})



@csrf_exempt
def payment_done(request):
	returnData=request.POST
	return render(request, 'payment-success.html',{'data':returnData})


@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')


# Save Review
def save_review(request,pid):
	product=Product.objects.get(pk=pid)
	user=request.user
	review=ProductReview.objects.create(
		user=user,
		product=product,
		review_text=request.POST['review_text'],
		review_rating=request.POST['review_rating'],
		)
	data={
		'user':user.username,
		'review_text':request.POST['review_text'],
		'review_rating':request.POST['review_rating']
	}

	# Fetch avg rating for reviews
	avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})

# User Dashboard
import calendar
def my_dashboard(request):
	category=Category.objects.order_by('-id')
	orders = CartOrder.objects.annotate(day=ExtractDay('order_dt')).values('day').annotate(count=Count('id')).values('day', 'count')
	dayNumber=[]
	totalOrders=[]
	for d in orders:
		dayNumber.append(d['day'])
		totalOrders.append(d['count'])
	return render(request, 'user/dashboard.html',{'dayNumber':dayNumber,'totalOrders':totalOrders, 'category': category})

# My Orders
def my_orders(request):
	orders=CartOrder.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/orders.html',{'orders':orders})

# Order Detail
def my_order_items(request,id):
	order=CartOrder.objects.get(pk=id)
	orderitems=CartOrderItems.objects.filter(order=order).order_by('-id')
	return render(request, 'user/order-items.html',{'orderitems':orderitems})

# Wishlist
def add_wishlist(request):
	pid=request.GET['product']
	product=Product.objects.get(pk=pid)
	data={}
	checkw=Wishlist.objects.filter(product=product,user=request.user).count()
	if checkw > 0:
		data={
			'bool':False
		}
	else:
		wishlist=Wishlist.objects.create(
			product=product,
			user=request.user
		)
		data={
			'bool':True
		}
	return JsonResponse(data)

# My Wishlist
def my_wishlist(request):
	wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/wishlist.html',{'wlist':wlist})

# My Reviews
def my_reviews(request):
	reviews=ProductReview.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/reviews.html',{'reviews':reviews})

# My AddressBook
def my_addressbook(request):
	addbook=UserAddressBook.objects.filter(user=request.user).order_by('-id')
	for add in addbook:
		add.ship_address = f"{add.street}, {add.ward}, {add.district}, {add.province}"
	return render(request, 'user/addressbook.html',{'addbook':addbook})

# Save addressbook
def save_address(request):
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Địa chỉ đã được lưu'
	form=AddressBookForm
	return render(request, 'user/add-address.html',{'form':form,'msg':msg})

# Activate address
def activate_address(request):
	a_id=str(request.GET['id'])
	UserAddressBook.objects.update(status=False)
	UserAddressBook.objects.filter(id=a_id).update(status=True)
	return JsonResponse({'bool':True})

# Edit Profile
def edit_profile(request):
	msg=None
	if request.method=='POST':
		form=ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=ProfileForm(instance=request.user)
	return render(request, 'user/edit-profile.html',{'form':form,'msg':msg})

# Update addressbook
def update_address(request,id):
	address=UserAddressBook.objects.get(pk=id)
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST,instance=address)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm(instance=address)
	return render(request, 'user/update-address.html',{'form':form,'msg':msg})

# Shippment
def shipment(request):
	ships = Shipment.objects.all()
	address = UserAddressBook.objects.filter(user=request.user, status=True).first()
	ship_address = f"{address.street}, {address.ward}, {address.district}, {address.province}"
	for ship in ships:
		ship.price = format(ship.price,",").replace(',', '.')
	total_amt=0
	totalAmt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			totalAmt+=int(item['qty'])*float(item['price'])
		total_amt = totalAmt
	return render(request, 'shipment.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'ships':ships,'ship_address':ship_address,'address':address})
#Payment
def payment(request):
	ship = Shipment.objects.first()
	fake_ship_price = '50000.0'
	address = UserAddressBook.objects.filter(user=request.user, status=True).first()
	ship_address = f"{address.street}, {address.ward}, {address.district}, {address.province}"
	payments = Payment.objects.all()
	total_amt=0
	totalAmt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			totalAmt+=int(item['qty'])*float(item['price'])
			originAmt = totalAmt-ship.price
		total_amt = totalAmt
	return render(request, 'payment.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'payments':payments,'ships':ship,'ship_address':ship_address,'address':address,'originAmt':originAmt,'fake_ship_price':fake_ship_price})

# Onl-Payment
def onl_payment(request):
	return render(request, 'onl_payment.html')

# Promotion
def promotion(request):
	collection_new=Collection.objects.get(id=2)
	data = Product.objects.filter(collection=collection_new, is_featured=True).order_by('-id')
	for product in data:
		product_reviews = ProductReview.objects.filter(product=product)
		avg_rating = product_reviews.aggregate(avg_rating=Avg('review_rating'))['avg_rating']
		star = round(avg_rating) if avg_rating else 5.0
		product.avg_rating = round(avg_rating, 1) if avg_rating else 5.0
		product.star = star
		price_discount = int(round(product.productattribute_set.first().price * (100 + product.productattribute_set.first().discount)/100,0))
		price_discount = format(price_discount,",").replace(',', '.')
		product.discount = price_discount

	collection_hot=Collection.objects.get(id=1)
	hot_products=Product.objects.filter(collection=collection_hot, is_featured=True).order_by('-id')
	for product in hot_products:
		product_reviews = ProductReview.objects.filter(product=product)
		avg_rating = product_reviews.aggregate(avg_rating=Avg('review_rating'))['avg_rating']
		star = round(avg_rating) if avg_rating else 5.0
		product.avg_rating = round(avg_rating, 1) if avg_rating else 5.0
		product.star = star
		price_discount = int(round(product.productattribute_set.first().price * (100 + product.productattribute_set.first().discount)/100,0))
		price_discount = format(price_discount,",").replace(',', '.')
		product.discount = price_discount

	voucher = Voucher.objects.all()
	for v in voucher:
		v.valid_from = v.valid_from.strftime("%d/%m/%Y")
		v.valid_to = v.valid_to.strftime("%d/%m/%Y")

	return render(request,'promotion.html', {'data':data,'hot_products':hot_products,'voucher':voucher})

def apply_voucher(request):
    if request.method == 'POST':
        form = VoucherForm(request.POST)
        if form.is_valid():
            voucher_code = form.cleaned_data['code']
            try:
                voucher = Voucher.objects.get(code=voucher_code)
                if voucher.is_valid():
                    # Áp dụng giảm giá cho đơn hàng ở đây
                    discount_percent = voucher.discount_percent
                    request.session['discount_percent'] = discount_percent
                    return redirect('checkout_page')
                else:
                    # Voucher hết hạn
                    form.add_error('code', 'Voucher đã hết hạn.')
            except Voucher.DoesNotExist:
                # Voucher không tồn tại
                form.add_error('code', 'Voucher không hợp lệ.')
        else:
            messages.error(request, 'Vui lòng nhập mã voucher hợp lệ.')
    else:
        form = VoucherForm()

    return render(request, 'order_updated.html', {'voucherform': form})
