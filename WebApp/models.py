from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from datetime import datetime

PRODUCT_CATEGORIES = {
    'electronics': 'Electronics',
    'clothing_men': 'Men’s Clothing',
    'clothing_women': 'Women’s Clothing',
    'clothing_children': 'Children’s Clothing',
    'food': 'Food',
    'toys': 'Toys',
    'books': 'Books',
    'furniture': 'Furniture',
    'sports': 'Sports & Outdoors',
    'beauty': 'Beauty & Personal Care',
    'automotive': 'Automotive',
    'home_garden': 'Home & Garden',
    'office_supplies': 'Office Supplies',
    'musical_instruments': 'Musical Instruments',
    'pet_supplies': 'Pet Supplies',
    'jewelry': 'Jewelry',
    'art_crafts': 'Arts & Crafts',
    'health': 'Health & Household',
    'computers': 'Computers & Accessories',
    'shoes': 'Shoes',
    'bags': 'Handbags & Wallets',
    'watches': 'Watches',
    'baby': 'Baby Products',
    'kitchen': 'Kitchen & Dining',
    'tools': 'Tools & Home Improvement',
    'video_games': 'Video Games',
    'industrial': 'Industrial & Scientific',
    'movies_tv': 'Movies & TV',
    'digital_music': 'Digital Music',
    'toiletries': 'Toiletries',
    'appliances': 'Appliances',
    'smart_home': 'Smart Home',
    'travel': 'Travel Gear',
    'cameras': 'Cameras & Photography',
    'collectibles': 'Collectibles & Fine Art',
    'software': 'Software',
    'cellphones': 'Cell Phones & Accessories',
    'audio': 'Audio & Home Theatre',
    'pharmacy': 'Pharmacy',
    'musical_equipment': 'DJ, Electronic Music & Karaoke',
    'magazines': 'Magazines',
    'gift_cards': 'Gift Cards',
    'wine': 'Wine',
    'farming': 'Farming & Agricultural',
    'outdoor_recreation': 'Outdoor Recreation',
    'home_decor': 'Home Décor',
    'bed_bath': 'Bed & Bath',
    'stationery': 'Stationery & Gift Wrapping',
    'hobbies': 'Hobbies',
    'motorcycles': 'Motorcycles & Powersports',
    'vintage_antiques': 'Vintage & Antiques',
    'education': 'Educational Supplies',
    'garden_tools': 'Gardening Tools',
    'luxury_brands': 'Luxury Brands',
    'comics': 'Comic Books',
    'graphic_novel':'Graphic Novel',
    'renewable_energy': 'Renewable Energy',
    'vehicles': 'Vehicles',
    # Add more categories as needed...
}
PRODUCT_CATEGORIES_TUPLES = tuple((k, v) for k, v in PRODUCT_CATEGORIES.items())

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)

    product_description = models.TextField(max_length=5000, default="", null=True, blank=True)
    
    product_price = models.CharField(max_length=500, default="", null=True)
    
    category = models.CharField(max_length=50, choices=PRODUCT_CATEGORIES_TUPLES, default='electronics')
    
    product_link = models.CharField(max_length=500, default="", null=True)
    image = models.ImageField(upload_to='static', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    favorited_by = models.ManyToManyField(User, related_name='favorite_products', blank=True, through='ProductFavorite')

    def __str__(self):
        return self.name

   

class Profile(models.Model):
    STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, blank=True, max_length=20)
    last_name = models.CharField(null=True, blank=True, max_length=50)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    profile_bio = models.CharField(max_length=100, null=True, blank=True)
    website_link = models.CharField(max_length=100, null=True, blank=True)
    facebook_link = models.CharField(max_length=100, null=True, blank=True)
    instagram_link = models.CharField(max_length=100, null=True, blank=True)
    linkedIn_link = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    address = models.CharField(null=True, blank=True, max_length=100)
    profession = models.CharField(null=True, blank=True, max_length=50)
    zip_code = models.CharField(null=True, blank=True, max_length=500)
    city = models.CharField(null=True, blank=True, max_length=20)
    country = models.CharField(null=True, blank=True, max_length=20)
    email = models.EmailField( max_length=500,null=True, blank=True)
    
    phone_number = models.CharField(max_length=100, null=True, blank=True)

    
    def __str__(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        else:
            return  self.user.username
@receiver(pre_save, sender=Profile)
def set_default_profile_image(sender, instance, **kwargs):
    if not instance.profile_image:
        instance.profile_image = 'profile_pics/default_profile_img.png'
    
# Create Profile When New User Signs Up


def delete_user(user_id):
    try:
        user = User.objects.get(id=user_id)
       
        user.delete()  # Delete the user
        return True
    except User.DoesNotExist:
        return False

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)


class Conversation(models.Model):
    sender = models.ForeignKey(User, related_name='sent_conversations', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_conversations', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    history = models.TextField(blank=True, null=True)  # This can store the conversation history in text format or you could design it differently depending on the requirement

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} on {self.timestamp}"



class ProductFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)



