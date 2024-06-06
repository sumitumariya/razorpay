from django.shortcuts import render,redirect
from .models import ItemInfo,Product
from .forms import ItemInfoForm
# Create your views here.

import razorpay
from django.views.decorators.csrf import csrf_exempt
def home(request):
    if request.method=="POST":
        form = ItemInfoForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        data = ItemInfo.objects.all()
        return render(request,'userform.html',{'form':form,'data':data})
    form = ItemInfoForm()
    data = ItemInfo.objects.all()
    if data:
        return render(request,'userform.html',{'form':form,'data':data})
    else:
        return render(request,'userform.html',{'form':form})


def addtocard(request,pk):
    if request.method == 'POST':
        quantity = request.session.get('quantity', [])
        quantity1 =int(request.POST.get('quantity'))
        quantity.append(quantity1)
        # print("quantity :",quantity)
        request.session['quantity'] = quantity
        cart = request.session.get('cart', [])
        cart.append(pk)
        request.session['cart'] = cart
        form = ItemInfoForm()
        data = ItemInfo.objects.all()
        return render(request,'userform.html',{'form':form,'data':data})
        # return redirect('home')

def cart(request):
    cart = request.session.get('cart',[])
    quantity = request.session.get('quantity',[])
    # print("Cart :",cart)
    # print("Quantity :",quantity)
    # print(len(cart))
    alldata = []
    i=0
    j=0
    total=0
    while i < len(cart):
        data = ItemInfo.objects.get(id=cart[i])
        print(quantity[j])
        total = total + (data.item_price)*quantity[j]
        # print(data.id)
        # print(data.iten_name)
        # print(data.item_desc)
        # print(data.item_price)
        # print(data.item_image)
        alldata.append({
            'id':data.id,
            'iten_name':data.iten_name,
            'item_desc':data.item_desc,
            'item_price':data.item_price,
            'item_image':data.item_image,
            'item_quantity':quantity[j]
        })
        i+=1
        j+=1
    # print("Total Amount = ",total)
    # print(alldata)
    return render(request,'cart.html',{'key':alldata,'amount':total})

def deletecart(request,pk):
    cart = request.session.get('cart',[])
    quantity = request.session.get('quantity',[])
    print("Cart :",cart)
    print("Quantity :",quantity)
    print("pk=",pk)
    x = cart.index(pk)
    # print("Cart index no:",x)
    # y = quantity[x]
    # print("Quantity of that card index:",y)
    cart1=[]
    y = len(cart)   
    i=0
    while i<y:
        if i==x:
            pass
        else:
            cart1.append(cart[i])
        i+=1
    print(cart1)
    request.session['cart']=cart1
    quantity1=[]
    z = len(quantity)
    j=0
    while j<z:
        if j==x:
            pass
        else:
            quantity1.append(quantity[j])
        j+=1
    print(quantity1)
    request.session['quantity']=quantity1
    # ----------------------------------------------------
    cart = request.session.get('cart',[])
    quantity = request.session.get('quantity',[])
    print("Cart :",cart)
    print("Quantity :",quantity)
    # print(len(cart))
    alldata = []
    i=0
    j=0
    total=0
    while i < len(cart):
        data = ItemInfo.objects.get(id=cart[i])
        print(quantity[j])
        total = total + (data.item_price)*quantity[j]
        # print(data.id)
        # print(data.iten_name)
        # print(data.item_desc)
        # print(data.item_price)
        # print(data.item_image)
        alldata.append({
            'id':data.id,
            'iten_name':data.iten_name,
            'item_desc':data.item_desc,
            'item_price':data.item_price,
            'item_image':data.item_image,
            'item_quantity':quantity[j]
        })
        i+=1
        j+=1
    # print("Total Amount = ",total)
    print(alldata)
    return render(request,'cart.html',{'key':alldata,'amount':total})

def payment(request):
    global payment
    if request.method=="POST":
        # amount in paisa
        amount = int(request.POST.get('amount')) * 100
        
        client = razorpay.Client(auth =("rzp_test_pr99iascS1WRtU" , "UTDIzPGwICnAssu3Q3lk7zUi"))
        # create order
        
        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        product = Product.objects.create( amount =amount , order_id = payment['id'])
        cart = request.session.get('cart',[])
        quantity = request.session.get('quantity',[])
        alldata = []
        i=0
        j=0
        total=0
        while i < len(cart):
            data = ItemInfo.objects.get(id=cart[i])
            total = total + (data.item_price)*quantity[j]
            alldata.append({
                'id':data.id,
                'iten_name':data.iten_name,
                'item_desc':data.item_desc,
                'item_price':data.item_price,
                'item_image':data.item_image,
                'item_quantity':quantity[j]
            })
            i+=1
            j+=1
        # print(payment)
        return render(request,'cart.html',{'key':alldata,'amount':total,'payment':payment})
    
@csrf_exempt
def payment_status(request):
       if request.method=="POST": 
        response = request.POST
        print(response) #  
        print(payment)

        razorpay_data = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }

        # client instance
        client = razorpay.Client(auth =("rzp_test_pr99iascS1WRtU" , "UTDIzPGwICnAssu3Q3lk7zUi"))

        try:
            status = client.utility.verify_payment_signature(razorpay_data)
            product = Product.objects.get(order_id=response['razorpay_order_id'])
            product.razorpay_payment_id = response ['razorpay_payment_id']
            product.paid = True
            product.save()
            
            return render(request, 'success.html', {'status': True})
        except:
            return render(request, 'success.html', {'status': False})