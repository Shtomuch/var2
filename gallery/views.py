from django.shortcuts import render, get_object_or_404

from .models import Category, Image


def gallery_view(request):
    """
    Показує усі категорії разом із їхніми зображеннями.
    """
    categories = Category.objects.prefetch_related("image_set")
    return render(request, "gallery.html", {"categories": categories})

def image_detail(request, pk):
    """
    Показує одне конкретне зображення за його первинним ключем.
    """
    image = get_object_or_404(Image, pk=pk)
    return render(request, "image_detail.html", {"image": image})