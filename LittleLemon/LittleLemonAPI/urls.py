from django.urls import path
from . import views

urlpatterns = [
 path('menu-items/', views.menu_items, name='menu_items'),
 path('menu-items/<int:pk>',views.SingleMenuItemView.as_view()),

]