from django.shortcuts import render

from .models import Category


def gallery_view(request):
    """
    Показує усі категорії разом із їхніми зображеннями.
    """
    categories = Category.objects.prefetch_related("image_set")
    return render(request, "gallery.html", {"categories": categories})
