from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.get_test),
    path('buy/<int:id>/', views.get_buy),
    path('item/<int:id>/', views.get_item),

]


