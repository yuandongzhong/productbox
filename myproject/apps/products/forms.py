from django import forms
from PIL import Image

from .models import Category, Product, ProductPhoto


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'title',
            'description',
            'price',
            'color',
            'model_number',
            'category',
            'power',
            'capacity',
            'certificate',
            'accessory',
            'fob',
            'cif',
            'product_dimension',
            'giftbox_dimension',
            'master_carton_dimension',
            'net_weight',
            'gross_weight',
            'cap_20gp',
            'cap_40gp',
            'cap_40hq',
            'is_available')
        labels = {
            'title': 'Title',
            'description': 'Description',
            'price': 'Price',
            'color': 'Color',
            'model_number': 'Model Num',
            'category': 'Category',
            'power': 'Power',
            'capacity': 'Capacity',
            'certificate': 'Certificate',
            'accessory': 'Accessory',
            'fob': 'FOB Price',
            'cif': 'CIF Price',
            'product_dimension': 'Product Dimension',
            'giftbox_dimension': 'Package Dimension',
            'master_carton_dimension': 'Carton Dimension',
            'net_weight': 'Net Weight',
            'gross_weight': 'Gross Weight',
            'cap_20gp': '20GP CAP',
            'cap_40gp': '40GP CAP',
            'cap_40hq': '40HQ CAP',
            'is_available': 'Availability'}


class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = ProductPhoto
        fields = ('image_file', 'x', 'y', 'width', 'height', )
        labels = {
            'image_file': 'Product Image',
        }

    def save(self, product, user):
        photo = super(PhotoForm, self).save(commit=False)
        photo.product = product
        photo.created_by = user
        photo.save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.image_file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((600, 600), Image.ANTIALIAS)
        resized_image.save(photo.image_file.path)
        return photo
