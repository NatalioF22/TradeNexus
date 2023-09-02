from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Product, Profile, Conversation, User
from .forms import ProductForm, ProfileForm, UserForm, ConversationForm  # You'll need to create these forms
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.db.models import Q, Sum
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Conversation
from django.http import JsonResponse
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Profile
from .forms import ProfileForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError, transaction
from .models import Profile  # Import your Profile model appropriately
 # Import at the top of your file




from .models import PRODUCT_CATEGORIES_TUPLES
from .models import PRODUCT_CATEGORIES

ERROR_MESSAGE = ""

def your_main_view_function(request):
    # ... your other logic here
    categories = dict(PRODUCT_CATEGORIES_TUPLES)
    context = {
        'categories': categories,
        # ... your other context variables
    }
    return render(request, 'header.html', context)


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
   
    # Ensure the user editing is the owner of the profile
    if request.user != user:
        ERROR_MESSAGE = "You don't have permission to edit this profile."
       
        return render(request, 'index.html', {'error_message': ERROR_MESSAGE})

    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username) # Assuming you have a profile_detail view
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


# ...

def home(request):
    products = Product.objects.all().order_by('-created_at')
    profile = None  # Initialize as None
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except ObjectDoesNotExist:
            profile = None  # If profile doesn't exist, keep it as None or handle it otherwise
    return render(request, 'index.html', {'products': products, 'profile': profile})




@transaction.atomic  # Ensures atomicity
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Assign the newly created user to the 'user' variable
            
            # Only create a new profile if the user doesn't have one yet
            if not hasattr(user, 'profile'):
                try:
                    Profile.objects.create(user=user)  # Create a profile for the newly created user
                except IntegrityError:
                    # Roll back the transaction in case of error
                    transaction.rollback()
                    form.add_error(None, 'There was an error creating your profile.')
                    return render(request, 'register_user.html', {'form': form})
                    
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register_user.html', {'form': form})

def login_user(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password"
    return render(request, 'login_user.html', {'error_message': error_message})


def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def profile_detail_view(request, username):
    # Get the user instance
    user = get_object_or_404(User, username=username)
    if user.is_authenticated == False:
        ERROR_MESSAGE = "You Must be logged in to view this profile" 
        return render(request, 'login_user.html', {'error_message': "You don't have permission to edit this profile."})
    # Filter products by the user
    products = Product.objects.filter(owner=user).order_by('-created_at')

    user_instance = User.objects.get(username=username)
    conversations = Conversation.objects.filter(
        Q(sender=request.user, receiver=user_instance) | 
        Q(sender=user_instance, receiver=request.user)
    ).order_by('-timestamp')
    
    # Get the associated profile for that user
    profile = user.profile

    return render(request, 'profile.html', {
        'profile': profile, 
        'conversations': conversations,
        'user_instance': user,
        'products': products   # Pass the filtered products to the template
    })


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile_edit.html', {'form': form})



def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_details.html', {'product': product})


@login_required
def conversation(request):
    if request.method == "GET":
        search_conversation = request.GET.get('q', '')
        conversation = Conversation.objects.filter(
            Q(sender__username__icontains=search_conversation) |
            Q(receiver__username__icontains=search_conversation) |
            Q(text__icontains=search_conversation) |
            Q(timestamp__icontains=search_conversation)
        )
        return render(request, 'conversation.html', {'search_conversation': search_conversation, 'conversation': conversation})
    users = User.objects.all().exclude(id=request.user.id)  # All users except the current one
    for user in users:
        user.unread_count = Conversation.objects.filter(receiver=request.user, sender=user, is_read=False).count()

    # Fetch messages and other required data...

    context = {
        'users': users,
        # other context data
    }

    return render(request, 'conversation.html', context)



@login_required
def send_message(request, receiver_username):
    if request.method == 'POST':
        receiver = User.objects.get(username=receiver_username)
        sender = request.user
        text = request.POST.get('text')
        message = Conversation(sender=sender, receiver=receiver, text=text)
        message.save()
        return redirect('chat_with_user', user_id=receiver.id)
    else:
        return HttpResponse("Invalid Request", status=400)

def search_view(request):
    if request.method == "GET":
        searched = request.GET.get('q', '')
        products = Product.objects.filter(
            Q(name__icontains=searched) |
            Q(product_description__icontains=searched) |
            Q(product_price__icontains=searched) |  # Assuming you want to search within the price as text.
            Q(category__icontains=searched)  # Since category is a CharField with choices.
        )
        # Since you don't have a Category model or an average_rating function in the provided model, I've removed those parts.
        return render(request, 'searched.html', {'searched': searched, 'products': products})
    else:
        return render(request, 'searched.html', {'searched': ""})


from django.shortcuts import render
from django.utils.text import slugify

def category_view(request, category_name):
    decoded_category_name = slugify(category_name)
    category_value = PRODUCT_CATEGORIES.get(decoded_category_name, 'Unknown Category')
    
    products = Product.objects.filter(category=decoded_category_name)
    
    context = {
        'products': products,
        'category_name': category_value
    }
    
    return render(request, 'category.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user  # Assign the owner
            product.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})
@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Ensure the user updating is the owner of the product
    if request.user != product.owner:
        messages.error(request, "You don't have permission to update this product.")
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'update_product.html', {'form': form})

from django.http import JsonResponse

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.owner:
        return JsonResponse({'success': False, 'message': 'Permission denied.'})

    if request.method == 'POST':
        product.delete()
        return JsonResponse({'success': True, 'redirect_url': 'index.html'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation

@login_required
def chat_with_user(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = Conversation.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('-timestamp')

    context = {
        'messages': messages,
        # Add other necessary context variables
    }
    return render(request, 'conversation_history.html', context)

from django.http import JsonResponse

@login_required
def send_message(request, receiver_username):
    
    if request.method == 'POST':
        receiver = User.objects.get(username=receiver_username)
        sender = request.user
        text = request.POST.get('text')
        message = Conversation(sender=sender, receiver=receiver, text=text)
        message.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request'})



from django.db.models import Q

def list_of_users(request):
    query = request.GET.get('search', '')
    profiles = Profile.objects.exclude(user=request.user).filter(
        Q(user__username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    )
    paginator = Paginator(profiles, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list_of_users.html', {'page_obj': page_obj, 'query': query})



def search_users(request):
    query = request.GET.get('query')
    profiles = Profile.objects.exclude(user=request.user)  # exclude the current user from the results
    if query:
        profiles = profiles.filter(user__username__icontains=query)

    paginator = Paginator(profiles, 2)  # Show 2 profiles per page (change this as needed)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list_of_users.html', {'page_obj': page_obj})

def about_us(request):
    return render(request, "about_us.html",{})