from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from ..forms import CategoryForm
from ..models import Category, Product


@login_required
def home(request):
    categories = Category.objects.order_by('-created_at').annotate(
        number_of_products=Count('products'))
    return render(request, 'home.html', {'categories': categories})


def save_category_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            categories = Category.objects.order_by('-created_at').annotate(
                number_of_products=Count('products'))
            data['html_category_list'] = render_to_string(
                'products/includes/partial_category_list.html', {
                    'categories': categories
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
    else:
        form = CategoryForm()
    return save_category_form(request, form, 'products/includes/partial_category_create.html')


@login_required
def category_update(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
    else:
        form = CategoryForm(instance=category)
    return save_category_form(request, form, 'products/includes/partial_category_update.html')


@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    data = dict()
    if request.method == 'POST':
        category.delete()
        data['form_is_valid'] = True
        categories = Category.objects.order_by('-created_at').annotate(
            number_of_products=Count('products'))
        data['html_category_list'] = render_to_string('products/includes/partial_category_list.html', {
            'categories': categories
        })
    else:
        context = {'category': category}
        data['html_form'] = render_to_string('products/includes/partial_category_delete.html',
                                             context,
                                             request=request)
    return JsonResponse(data)
