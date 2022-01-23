from django.contrib import admin

from advertisement.models import Tag, Company, TagValue, Advertisement, CrawlerConfig, Link


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')
    search_fields = ('title',)


class TagValueInline(admin.TabularInline):
    model = TagValue
    can_delete = False
    extra = 0


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'company', 'remaining_days',)
    search_fields = ('title',)
    inlines = [TagValueInline]


@admin.register(CrawlerConfig)
class CrawlerConfigAdmin(admin.ModelAdmin):
    list_display = ('source', 'city')


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('source', 'url', 'crawled')
