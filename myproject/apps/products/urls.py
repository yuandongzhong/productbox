from django.urls import path

from .views import categories, photos, products

app_name = "products"


'''
Categories
'''
urlpatterns = [
    path('categories/create/',
         categories.category_create, name='category_create'),
    path('categories/<int:category_id>/update/',
         categories.category_update, name='category_update'),
    path('categories/<int:category_id>/delete/',
         categories.category_delete, name='category_delete'),
]

'''
Products
'''
urlpatterns += [
    path('categories/<int:category_id>/',
         products.category_products, name='category_products'),
    path('categories/<int:category_id>/create/',
         products.product_create, name='product_create'),
    path('categories/<int:category_id>/<int:product_id>/update/',
         products.product_update, name='product_update'),
    path('categories/<int:category_id>/<int:product_id>/delete/',
         products.product_delete, name='product_delete'),
]

'''
Photos
'''
urlpatterns += [
    path('categories/<int:category_id>/photos/',
         photos.category_photos, name='category_photos'),
    path('categories/<int:category_id>/photos/<int:product_id>/',
         photos.product_photos, name='product_photos'),
    path('categories/<int:category_id>/photos/<int:product_id>/delete',
         photos.photo_delete, name='photo_delete'),
]
