from django import template

register = template.Library()


@register.simple_tag
def get_cover_photo_url(product_instance, model_number):
    cover_photo = product_instance.get_cover_photo(model_number)
    if cover_photo is None:
        return product_instance.get_default_cover_url()
    return cover_photo.image_file.url
