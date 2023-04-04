from .models import *

def content_category(request):
    categories = Category.objects.all()

    return {'categories':categories}