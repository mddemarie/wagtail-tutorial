from django.contrib import admin
from modeltranslation.translator import register, TranslationOptions
from modeltranslation.admin import TranslationAdmin

from wagtail.core.models import Page
from .models import (
    RecipesIndexPage, RecipesPageTag, RecipesPage,
    RecipesPageGalleryImage, RecipesCategory
    )


@register(Page)
class PageTR(TranslationOptions):
    pass


@register(RecipesIndexPage)
class RecipesIndexPageTranslationOptions(TranslationOptions):
    fields = ('title', 'intro', 'slug')


class RecipesIndexPageAdmin(TranslationAdmin):
    pass


admin.site.register(RecipesIndexPage, RecipesIndexPageAdmin)



# fields = ('title', 'intro', 'draft_title', 'slug', 'content_type', 'live',
#               'has_unpublished_changes', 'url_path', 'owner', 'seo_title',
#               'show_in_menus_default', 'show_in_menus', 'search_description', 'go_live_at'
#               'expire_at', 'expired', 'locked', 'first_published_at', 'last_published_at',
#               'latest_revision_created_at', 'live_revision', 'search_fields', 'is_creatable',
#               'exclude_fields_in_copy', 'content_panels', 'promote_panels', 'settings_panels')

# @register(RecipesPageTag)
# class RecipesPageTagTranslationOptions(TranslationOptions):
#     fields = ('content_object',)
#
#
# @register(RecipesPage)
# class RecipesPageTranslationOptions(TranslationOptions):
#     fields = ('date', 'utensils', 'description', 'tags', 'categories')

#
# @register(RecipesPageGalleryImage)
# class RecipesPageGalleryImageTranslationOptions(TranslationOptions):
#     fields = ('page', 'image', 'caption')
#
#
# @register(RecipesCategory)
# class RecipesCategoryTranslationOptions(TranslationOptions):
#     fields = ('name', 'icon')
