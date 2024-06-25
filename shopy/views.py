
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTM.Checksum import generate_checksum
# from paytmchecksum import PaytmChecksum
# from PayTM.Checksum import generateSignature, verifySignature
# from PayTM.Checksum import generateSignature, verifySignature, calculateChecksum
# from PayTM.Checksum import generate_checksum

# Test credentials for Paytm
MERCHANT_ID = 'WorldP64425807474247'
MERCHANT_KEY = '0123456789abcdef'

# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    products = Product.objects.all()
    print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4) - (n//4))
    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides), 'product':products}
    # allProd = [[products, range(1,nSlides), nSlides],
    #            [products, range(1,nSlides), nSlides]]
    allProds = []
    categoryProducts = Product.objects.values('category', 'id')
    categorys = {item['category'] for item in categoryProducts}
    for cat in categorys:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1,nSlides), nSlides])
    params = {'allProd': allProds}
    return render(request, 'shopy/index.html',params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.product_desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds, "msg": ""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    # print(params)

    return render(request, 'shopy/search.html', params)

def about(request):
    return render(request, 'shopy/about.html')

def contact(request):
    if request.method=="POST":
        # print(request)
        name = request.POST.get('name')
        # print(name)
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')

        # Validate the Contact data
        if not name or not email or not phone or not desc:
            error_message = "All fields are required."
            print(error_message)
            return render(request, 'shopy/contact.html', {'error': error_message})

        # Save the contact data if valid
        print("Saving Contact: ", name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()

        # Redirect to a success page or render a success message
        success_message = "Your message has been sent successfully."
        return render(request, 'shopy/contact.html', {'success': success_message})
    return render(request, 'shopy/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                    response = json.dumps({"status":"success", "updates":updates, "itemsJson":order[0].ItemJson}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shopy/tracker.html')

def productView(request, myid):
    # product=Product.objects.filter(id=myid)
    product = get_object_or_404(Product, id=myid)
    print(product)
    content = {'product': product}
    return render(request, "shopy/prodView.html", content)

def checkout(request):
    if request.method=="POST":
        # print(request)
        ItemJson = request.POST.get('ItemJson','')
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        address = request.POST.get('address')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # Validate the form data
        if not name or not email or not phone:
            error_message = "All fields are required."
            print(error_message)
            return render(request, 'shopy/checkout.html', {'error': error_message})

        # If the Order is valid, create a new Order record with all this fields
        order = Order(ItemJson=ItemJson, name=name, amount=amount, email=email, address=address, address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()

        # Redirect to a success page or render a success message
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shopy/checkout.html', {'thank': thank, 'id': id})

        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {
            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': 'email',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shopy/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, '0123456789abcdef')
        return render(request, 'shopy/paytm.html', {'param_dict': param_dict})
    return render(request, 'shopy/checkout.html')

@csrf_exempt
def handlerequest(request):
        return render(request, 'shopy/paymentsucessfull.html')
