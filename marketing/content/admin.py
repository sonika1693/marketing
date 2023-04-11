from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user","content"]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["txn_id","amount_paid","status","created_at"]
    search_fields = ["txn_id","status"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user","order_number","name","email","total_amount"]
    search_fields = ["order_number","name","email","phone"]

@admin.register(OrderContent)
class OrderContentAdmin(admin.ModelAdmin):
    list_display = ["order","content","ordered"]
    search_fields = ["order__order_number"]

@admin.register(ContentLikes)
class ContentLikesAdmin(admin.ModelAdmin):
    list_display = ["user","content","likes","date"]
    search_fields = ["content__category__name"]

@admin.register(ContentComments)
class ContentCommentsAdmin(admin.ModelAdmin):
    list_display = ["user","content","comment","date"]
    search_fields = ["content__category__name"]

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ["title","price","is_locked","home","date"]
    search_fields = ["category__name","title"]
    list_editable = ["is_locked","home","price"]
    