from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import * 
from guest_user.decorators import allow_guest_user
from django.contrib.auth.decorators import login_required
import datetime
from content.forms import OrderForm 
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
# def video_upload(request):
    # if request.method == 'Get':
    #     return render(request,'content/video_upload.html')
    # else:
    #     try:
    #         container_name = "testing-bodhiai"
    #         account_name = 'bodhiaigeneral'
    #         account_key = 'zpXD7cmZ4jDnpn/7a/KkZ6Bqia8zRQ+8f7YukTRnS6+njD99758lMWpJPLwZl9KdJKVevXy6XseyrdJMUIfbMA=='
    #         file = request.FILES['file']
    #         filename = file.name
    #         file_upload_name = str(uuid.uuid4()) + file.name
    #         blob_service_client = BlockBlobService(account_name = account_name, account_key=account_key)
    #         blob_service_client.create_blob_from_bytes( container_name = 'testing-bodhiai', blob_name = file_upload_name, blob = file.read())
    #         uploaded_file_url = f"https://bodhiuploadbucket.azureedge.net/{container_name}/{file_upload_name}"
    #         messages.success(request, 'Successfully Uploaded')
    #         return render(request,'content/video_upload.html',{"uploaded_file_url": uploaded_file_url})
    #     except Exception as e:
    #         messages.error(request, str(e))
    #         return render(request,'content/video_upload.html')


    
def Home(request):
    user = request.user
    all_packages = Content.objects.filter(home = True)
    return render(request,'content/index.html',{'all_packages':all_packages})

def CategoryPackages(request,cat_id):
    if request.method == "GET":
        # cat_id = request.GET.get('cat_id')
        all_packages = Content.objects.filter(category = cat_id)

        return render(request,'content/package.html',{'all_packages':all_packages})
    
def PremiumPackage(request):
    if request.method == "GET":
        all_packages = Content.objects.filter(is_locked = True)
        return render(request,'content/premium.html',{'all_packages':all_packages})
    
def Details(request,content_id):
    if request.method == "GET":
        user = request.user
        # content_id = request.GET.get('content_id')
        content = Content.objects.get(id = content_id)
        all_comments = ContentComments.objects.filter(content=content).order_by('-id')[:5]
        user_like = ContentLikes.objects.filter(user=user,content=content).first()
        count_likes = ContentLikes.objects.filter(content=content,likes=True).count()
        context = {
            'content': content,
            'all_comments': all_comments,
            'user_like': user_like,
            'count_likes': count_likes,
        }

        return render(request,'content/details.html',context)

@allow_guest_user    
def AddComents(request):
    try:
        user = request.user
        content_id = request.GET.get('content_id')
        comment_text = request.GET.get('comment_text')
        content = Content.objects.get(id = content_id)
        user_comment = ContentComments()
        user_comment.user = user
        user_comment.content = content
        user_comment.comment = comment_text
        user_comment.save()
        data = [{'username': user_comment.user.username, 'comment': user_comment.comment}]
                
        return JsonResponse(data,safe=False)
    except Exception as e:
        messages.error(request, str(e))
        return JsonResponse(safe=False,data="Something Went Wrong")

@allow_guest_user    
def AddLikes(request):
    try:
        user = request.user
        content_id = request.GET.get('content_id')
        like_btn = request.GET.get('like_btn')
        content = Content.objects.get(id = content_id)
        try:
            new_likes = ContentLikes.objects.get(user=user,content=content)
            if new_likes.likes == True:
                new_likes.likes = False
            else:
                new_likes.likes = True
            new_likes.save()

        except ContentLikes.DoesNotExist:
            new_likes = ContentLikes()
            new_likes.user = user
            new_likes.content = content
            if like_btn:
                new_likes.likes = True
            new_likes.save()

        count_likes = ContentLikes.objects.filter(content=content,likes=True).count()  
        data = [count_likes] 

        return JsonResponse(data,safe=False)

    except:
        return JsonResponse(data="Something Went Wrong.",safe=False)

def add_cart(request,content_id):
    if request.user.is_authenticated:
        user = request.user
        content = Content.objects.filter(id=content_id).first()
        cp = Cart.objects.filter(user=user, content=content).first()
        if cp:
            messages.error(request,'Already added in Cart.')
            return redirect("/content/details/"+ str(content_id))
        else:
            Cart.objects.create(user=user, content=content)
            messages.success(request,'Successfully added in Cart.')
            return redirect("/content/details/"+ str(content_id))
    else:  
        messages.success(request,'You have to Login to add items in cart')
        return redirect("/content/details/"+ str(content_id))

def delete_cart_item(request):
    user = request.user
    try:
        cart_id = request.GET.get('cart_id')
        Cart.objects.get(id = cart_id).delete()
        return JsonResponse(safe=False,data="Delete Successfully")
    except:
        return JsonResponse(safe=False,data="Something Went Wrong")

@login_required(login_url='/',)
def view_cart(request):
    user = request.user
    cart_data = Cart.objects.filter(user=user)
    total_price = 0  
    for i in cart_data:
        total_price += i.content.price
    context = {
      'cart_data':cart_data,
      'total_price':total_price,
    }
    return render(request,'content/cart.html',context)

def checkout(request):
    user = request.user
    if request.method == 'GET':
        cart_data = Cart.objects.filter(user=user)
        total_price = 0  
        for i in cart_data:
            total_price += i.content.price

        context = {
        'cart_data':cart_data,
        'total_price':total_price,
        }
        return render(request,'content/checkout.html',context)
    
    else:
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = user
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.total_amount = form.cleaned_data['total_amount']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user = user,is_ordered = False,order_number = data.order_number)
            cart_data = Cart.objects.filter(user=user)
            total_price = 0  
            for i in cart_data:
                total_price += i.content.price

            context = {
            'order':order,
            'cart_data':cart_data,
            'total_price':total_price,
            }
            return render(request,'content/payment.html',context)
    
def payment(request):
    # The json. loads() is used to convert the JSON String document into the Python dictionary.
    # body = json.loads(request.body)
    payment_method= request.POST.get('payment_method')
    order_number = request.POST.get('order_number')
    txn_id = request.POST.get('txn_id')
    status = request.POST.get('status')

    order = Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)

    payment = Payment()
    payment.txn_id = txn_id
    payment.amount_paid = order.total_amount
    payment.payment_method = payment_method
    payment.status = status
    payment.save()

    # after payment update order model
    order.payment = payment
    order.is_ordered = True
    order.status = 'Completed'
    order.save()

    # move cart items in order contents model
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        order_content = OrderContent()
        order_content.order = order 
        order_content.content = item.content
        order_content.ordered = True
        order_content.save()

    # clear cart iteams from cart after payment
    cart_items.delete()

    # send mail to user after order
    # mail_subject = 'Thank You!'
    # message = render_to_string('content/order_recieved_mail.html',{
    #     'user': request.user,
    #     'order': order,
    # })
    # to_email = 'sonikagarsha16@gmail.com'
    # send_email = EmailMessage(mail_subject, message, to=[to_email])
    # send_email.send()

    # send back data in json response to page
    data = {
        'success': True,
        'order_number': order.order_number,
        'txn_id': payment.txn_id,
    }

    return JsonResponse(data, safe=False)

def success(request):
    user = request.user
    order_number = request.GET.get('order_number')
    txn_id = request.GET.get('txn_id')
    try:
        order = Order.objects.get(order_number = order_number, is_ordered = True)
        ordered_content = OrderContent.objects.filter(order=order)
        payment = Payment.objects.get(txn_id = txn_id)
        total_price = 0  
        for i in ordered_content:
            total_price += i.content.price

        context = {
            'order': order,
            'payment':payment,
            'ordered_content': ordered_content,
            'order_number': order_number,
            'total_price': total_price,
        }
        return render(request,'content/success.html',context)
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('/content')

    


    
