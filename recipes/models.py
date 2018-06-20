from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class RecipesIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]

    # def get_context(self, request):
    #     context = super().get_context(request)
    #     recipepages = self.get_children().live().order_by('-first_published_at')
    #     context['recipepages'] = recipepages
    #     return context


class RecipesPage(Page):
    date = models.DateField("recipe date")
    utensils = models.CharField(max_length=250)
    description = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('utensils'),
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('utensils'),
        FieldPanel('description', classname="full"),
        InlinePanel('gallery_images', label="Gallery images")
    ]


class RecipesPageGalleryImage(Orderable):
    page = ParentalKey(RecipesPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption')
    ]
