from django.contrib import admin
from .models import Product, Profile, Conversation

# Admin class for Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)

# Admin class for Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'user__username')

# Admin class for ProductPost model
from django.contrib import admin
from .models import Conversation

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp',)
    list_filter = ('sender', 'receiver', 'timestamp', )
    search_fields = ('sender__username', 'receiver__username', 'text')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    
    # If you wish to see the full text content in the admin change form


    

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Profile, ProfileAdmin)