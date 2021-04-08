from django.urls import path, include
from .views import (
                    IndexView,
                    ContactView,
                    ItemDetailView,
                    CartView,
                    CheckOut,
                    CustomerReview,
                    Shop,
                    WishList,
                    Team,
                    Portfolio,
                    About,
                    CartView,
                    AddToCart,RemoveFromCart, RemoveItemFromMainCart,
                    AddToWish, RemoveItemFromWishList,
                    ItemQuickView,
                    AddCoupon, ItemCategoryView, ItemSearchResults,
                    LipaNaMpesaView, register_urls,confirmation,validation, call_back, getAccessToken
                    )

app_name="retechecommerce"

urlpatterns = [
    path('', IndexView, name='index'),
    path('contact/', ContactView, name='contact' ),
    path('products/<slug>/', ItemDetailView, name='item-detail'),
    path('products/category/<slug>', ItemCategoryView, name='category-list' ),
    path('quickview/<slug>/', ItemQuickView, name="item-quick-view"),
    path('add-to-cart/<slug>/', AddToCart, name='add-to-cart'),
    path('add-coupon/', AddCoupon, name="add-coupon"),
    path('remove-from-cart/<slug>/', RemoveFromCart, name='remove-from-cart'),
    path('add-to-wishlist/<slug>/', AddToWish, name='add-to-wishlist'),
    path('cart/', CartView, name="cart"),
    path('checkout/', CheckOut, name="checkout"),
    path('customerreview/', CustomerReview, name='customer-review'),
    path('shop/', Shop, name='shop'),
    path('wishlist/', WishList, name='wishlist'),
    path('team/', Team, name='team'),
    path('portfolio/', Portfolio, name='portfolio'),
    path('about/', About, name='about'),
    path('remove-from-main-cart/<slug>/', RemoveItemFromMainCart, name='remove-from-main-cart'),
    path('remove-from-wishlist/<slug>/', RemoveItemFromWishList, name='remove-from-wishlist'),
    path('product/search/', ItemSearchResults, name='search-results'),
    
    #mpesa urls#
    path('checkout/lipa-na-mpesa/', LipaNaMpesaView, name='lipa-na-mpesa'),
    path('c2b/register/', register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation/', confirmation, name="confirmation"),
    path('c2b/validation/', validation, name="validation"),
    path('c2b/callback/', call_back, name="call_back"),
    path('get-token/', getAccessToken, name='accessToken')
   
]
