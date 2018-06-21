from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class RecipesIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        recipepages = self.get_children().live().order_by('-first_published_at')
        context['recipepages'] = recipepages
        return context


class RecipesPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'RecipesPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class RecipesTagIndexPage(Page):

    def get_context(self, request):
        tag = request.GET.get('tag')
        recipespages = RecipesPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context['recipepages'] = recipespages
        return context


class RecipesPage(Page):
    date = models.DateField("recipe date")
    utensils = models.CharField(max_length=250)
    description = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=RecipesPageTag, blank=True)
    categories = ParentalManyToManyField('recipes.RecipesCategory', blank=True)

    def main_page(self):
        gallery_item = self.gallery_item.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('utensils'),
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
        ], heading='Recipe information'),
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

@register_snippet
class RecipesCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'recipe categories'
