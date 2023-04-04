from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages
from datetime import datetime
from .models import * 
from django.views.generic.base import View
from django.http import HttpResponseRedirect,JsonResponse
from guest_user.decorators import allow_guest_user
import random
import string

# Create your views here.
def Testing(request):
    if request.method == "GET":
        # user = request.user
        categories = Category.objects.all()
        context = {
            'categories':categories,
            'hours' : range(1,12),
            'minutes': range(0,60,5),
        }
        return render(request,'content/testing.html',context)
    else:
        print(request.POST)
        meeting_name = request.POST.get('meeting_name')
        batch_ids = request.POST.getlist('batch_checkbox')
        package_ids = request.POST.getlist('package_checkbox')
        duration_hr = request.POST.get('duration_hr')
        duration_min = request.POST.get('duration_min')

        return render(request,'content/testing.html')
        # return JsonResponse(safe=False,data="Done")

def Home(request):
    user = request.user
    all_packages = Content.objects.filter(home = True)
    return render(request,'content/index.html',{'all_packages':all_packages})

def Services(request):
    user = request.user
    return render(request,'content/services.html')

def About(request):
    user = request.user
    return render(request,'content/about.html')

def Shop(request):
    user = request.user
    return render(request,'content/shop.html')

def Contact(request):
    user = request.user
    return render(request,'content/contact.html')

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

    