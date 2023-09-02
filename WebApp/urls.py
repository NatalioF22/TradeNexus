from django.urls import path
from . import views


urlpatterns = [
    # Account views
    path('', views.home, name='home'),
     path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/<str:username>', views.profile_detail_view, name='profile'),
    path('about/', views.about_us, name='about_us'),
    # ... other URL patterns
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),

    # Product CRUD views
    path('product/add/', views.add_product, name='product_add'),
   
    path('products/', views.product_list_view, name='product_list'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('product/<int:pk>/update/', views.update_product, name='update_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),

    path('search/', views.search_view, name='search'),

    path('category/<str:category_name>/', views.category_view, name='category_view'),
    path('send_message/<str:receiver_username>/', views.send_message, name='send_message'),

    # Message views
    path('chat_with/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),
    path('users/', views.list_of_users, name='list_of_users'),

    # ... more url patterns as needed ...
]