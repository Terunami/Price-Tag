from django.urls import path

from .models import Item
from .views import ItemFilterView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView, ItemPriceUpdateView, ItemSearchCreateView

# アプリケーションのルーティング設定

urlpatterns = [
    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    path('price_update/', ItemPriceUpdateView.price_update, name='price_update'),
    path('search_create/', ItemSearchCreateView.search_title, name='search_title'),
    path('', ItemFilterView.as_view(), name='index'),
]
