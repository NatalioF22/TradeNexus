from .models import PRODUCT_CATEGORIES

def categories_processor(request):
    return {
        'categories': PRODUCT_CATEGORIES
    }
# context_processors.py

def profile_image(request):
    if request.user.is_authenticated:
        profile = request.user.profile  # Assuming the user has a related 'profile' model.
        return {'profile': profile}
    return {}
