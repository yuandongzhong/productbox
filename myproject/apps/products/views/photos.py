from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from ..forms import PhotoForm
from ..models import Category, Product, ProductPhoto


@login_required
def category_photos(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = category.products.all().order_by('-created_at')
    return render(request, 'products/category_photos.html', {'category': category, 'products': products})


@login_required
def product_photos(request, category_id, product_id):
    category = get_object_or_404(Category, pk=category_id)
    product = get_object_or_404(Product, pk=product_id)
    photos = product.photos.all().order_by('-created_at')
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(product, request.user)
            return redirect('products:product_photos', category_id, product_id)
    else:
        form = PhotoForm()
    return render(request, 'products/product_photos.html',
                  {'form': form, 'category': category, 'product': product, 'photos': photos})


@login_required
def photo_delete(request, category_id, product_id):
    data = dict()
    if request.method == 'POST':
        photo_id_list = request.POST.getlist('photos[]')
        photos = ProductPhoto.objects.filter(id__in=photo_id_list)
        print(photos)
        for photo in photos:
            photo.image_file.delete()
            photo.delete()
        data['success'] = True
        product = get_object_or_404(Product, pk=product_id)
        photos = product.photos.all().order_by('-created_at')
        context = {'photos': photos}
        data['html_photo_list'] = render_to_string('products/includes/partial_photo_list.html',
                                                   context,
                                                   request=request)
    else:
        context = {'category_id': category_id, 'product_id': product_id}
        data['html_form'] = render_to_string('products/includes/partial_photo_delete.html',
                                             context,
                                             request=request)
    return JsonResponse(data)
