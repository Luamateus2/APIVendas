from django.contrib import admin

from django.contrib import admin
from .models import Produto, Venda, ItemVenda

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'preco'] 
    search_fields = ['codigo', 'nome']  

@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ['venda', 'produto', 'quantidade', 'preco_unitario', 'subtotal']
    search_fields = ['produto__nome', 'venda__id']  
    list_filter = ['venda'] 

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['id', 'data', 'total']
    search_fields = ['id']
    list_filter = ['data'] 
