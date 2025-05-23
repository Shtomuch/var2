# gallery/urls.py
from django.urls import path
from .views import gallery_view, image_detail

app_name = "gallery"

urlpatterns = [
    path("", gallery_view, name="gallery_view"),
    path("<int:pk>/", image_detail, name="image_detail")
]