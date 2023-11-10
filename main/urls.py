from django import urls

from . import views

urlpatterns = [
    urls.path('', views.index, name='index'),
    urls.path('login/', views.login_view, name='login'),
    urls.path('logout/', views.logout_view, name='logout'),
    urls.path('register/', views.register_view, name='register'),
    urls.path('view-cart/', views.view_cart, name='view_cart'),
    urls.path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    urls.path('sub-from-cart/<int:product_id>/', views.sub_from_cart, name='sub_from_cart'),
    urls.path('del-from-cart/<int:product_id>/', views.delete_from_cart, name='del_from_cart'),
    urls.path('add-product/', views.add_product, name='add_product'),
    urls.path('view-product/<int:product_id>', views.view_product, name='view_product'),
    urls.path('view-my-products/', views.view_my_product, name='view_my_product'), 
    urls.path('delete-my-product/<int:product_id>', views.delete_my_product, name='delete_my_product'),
    urls.path('buy-product/<int:product_id>/', views.buy_product, name='buy_product'),
    urls.path('view-orders/', views.view_orders, name='view_orders'),
    urls.path('save-to-orders/', views.save_to_orders, name='save_to_orders'),
    urls.path('complete-orders/<int:order_id>/', views.complete_orders, name='complete_order'),
]
