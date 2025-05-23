import tempfile
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Category, Image


TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class GalleryViewsTest(TestCase):
    def setUp(self):
        # Готуємо тимчасовий файл-зображення (1×2 px GIF)
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x4C"
            b"\x01\x00\x3B"
        )
        image_file = SimpleUploadedFile(
            "test.gif", small_gif, content_type="image/gif"
        )

        # Створюємо моделі
        self.cat_nature = Category.objects.create(name="Nature")
        self.cat_city = Category.objects.create(name="City")

        self.img_tree = Image.objects.create(
            title="Tree",
            image=image_file,
            created_date=timezone.now().date(),
            age_limit=0,
        )
        self.img_city = Image.objects.create(
            title="Skyscraper",
            image=image_file,
            created_date=timezone.now().date(),
            age_limit=0,
        )

        self.img_tree.categories.add(self.cat_nature)
        self.img_city.categories.add(self.cat_city)



    def test_gallery_view_status_and_template(self):
        resp = self.client.get(reverse("gallery:gallery_view"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "gallery.html")

    def test_gallery_view_context_contains_categories(self):
        resp = self.client.get(reverse("gallery:gallery_view"))
        self.assertIn("categories", resp.context)
        self.assertEqual(resp.context["categories"].count(), 2)

    def test_image_detail_status_and_template(self):
        resp = self.client.get(
            reverse("gallery:image_detail", args=[self.img_tree.pk])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "image_detail.html")
        self.assertEqual(resp.context["image"], self.img_tree)

    def test_image_detail_returns_404_for_unknown_id(self):
        resp = self.client.get(reverse("gallery:image_detail", args=[9999]))
        self.assertEqual(resp.status_code, 404)