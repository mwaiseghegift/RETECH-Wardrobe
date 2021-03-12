from django.urls import path
from .views import (IndexView,
                    ContactView,
                    BlogView,
                    BlogDetailView,
                    CartView,
                    CheckOut,
                    CustomerReview,
                    Shop,
                    WishList,
                    Team,
                    Portfolio,
                    About,
                    )

app_name="retechecommerce"

urlpatterns = [
    path('', IndexView, name='index'),
    path('contact/', ContactView, name='contact' ),
    path('blog/', BlogView, name="blog"),
    path('cart/', CartView, name="cart"),
    path('checkout/', CheckOut, name="checkout"),
    path('customerreview/', CustomerReview, name='customer-review'),
    path('shop/', Shop, name='shop'),
    path('wishlist/', WishList, name='wishlist'),
    path('team/', Team, name='team'),
    path('portfolio/', Portfolio, name='portfolio'),
    path('about/', About, name='about'),
]
