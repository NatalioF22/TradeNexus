# TradeNexus


## Introduction

Welcome to the repository for our Django-based E-commerce platform. This project aims to provide a comprehensive and scalable solution for online marketplaces. We have meticulously designed our Django models to capture various aspects of the e-commerce ecosystem, from user profiles and favorites to a wide array of product categories.

## Table of Contents

1. [Features](#features)
2. [Database Models](#database-models)
3. [Installation and Setup](#installation-and-setup)

---

## Features

- **User Authentication**: Utilizes Django's built-in `User` model for secure and reliable authentication.
- **Profiles**: Extended user profiles with additional fields such as social media links, address, and profession.
- **Products**: Rich product listings with categories, descriptions, images, and pricing details.
- **Favoriting**: Users can favorite products.
- **Conversations**: Allows for user-to-user communication.
- **Comprehensive Categories**: Covers a broad range of product categories, from electronics to luxury brands.

---

## Database Models

### 1. Product

- **owner**: Foreign Key to User
- **name**: Product name
- **product_description**: A detailed description of the product
- **product_price**: Price of the product
- **category**: Enumerated choices capturing product categories
- **product_link**: Link to product page
- **image**: Image upload
- **created_at**: Timestamp of product creation
- **favorited_by**: Many-to-Many relationship with Users through 'ProductFavorite'

### 2. Profile

- **user**: One-to-One relationship with Django's User model
- **first_name, last_name**: User's name
- **profile_image**: Profile image upload
- **profile_bio**: A short bio
- **social media links**: Facebook, LinkedIn, Instagram
- **address information**: State, Zip Code, Address, City, Country
- **email**: Email address
- **phone_number**: Contact number
- **profession**: User's profession

### 3. Conversation

- **sender, receiver**: Foreign keys to User
- **text**: Conversation text
- **timestamp**: Timestamp of the conversation
- **history**: Text field to store conversation history

### 4. ProductFavorite

- **user**: Foreign Key to User
- **product**: Foreign Key to Product
- **date_added**: Timestamp when added to favorites

For more details, please refer to the `models.py` file.

---

## Installation and Setup

1. **Clone the repository**
    ```
    git clone https://github.com/NatalioF22/TradeNexus.git
    ```

2. **Navigate to the project directory**
    ```
    cd TradeNexus
    ```

3. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Run Migrations**
    ```
    python manage.py migrate
    ```

5. **Start Development Server**
    ```
    python manage.py runserver
    ```

---

Feel free to use this README as a template for your project. Good luck and happy coding!
