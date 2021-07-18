from django.urls import path

from core import views

urlpatterns = [
    path(
        r"return-highest-buyer",
        views.ShowHighestBuyer.as_view(),
        name="return-highest-buyer",
    ),
    path(
        r"return-highest-buy",
        views.ShowHighestBuy.as_view(),
        name="return-highest-buy",
    ),
    path(
        r"return-favorite-client",
        views.ShowFavoriteClient.as_view(),
        name="return-favorite-client",
    ),
    path(
        r"return-most-buy-wine-by-client",
        views.ShowMostBuyWineByClient.as_view(),
        name="return-most-buy-wine-by-client",
    ),    
]