from django.contrib.postgres.fields import ArrayField
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Link(BaseModel):
    JOBINJA = 0
    JOBVISION = 1
    QUERA = 2
    SOURCE_CHOICES = (
        (JOBINJA, 'جابینجا'),
        (JOBVISION, 'جاب ویژن'),
        (QUERA, 'کوئرا')
    )

    source = models.PositiveSmallIntegerField(choices=SOURCE_CHOICES, default=JOBINJA)
    url = models.TextField(unique=True)
    crawled = models.BooleanField(default=False)


class Tag(BaseModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.title}'


class Company(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/companies/')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'companies'


class Advertisement(BaseModel):
    JOBINJA = 0
    JOBVISION = 1
    QUERA = 2
    SOURCE_CHOICES = (
        (JOBINJA, 'جابینجا'),
        (JOBVISION, 'جاب ویژن'),
        (QUERA, 'کوئرا')
    )

    source = models.PositiveSmallIntegerField(choices=SOURCE_CHOICES, default=JOBINJA)
    url = models.TextField(unique=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    remaining_days = models.PositiveIntegerField(verbose_name='remaining days', null=True, blank=True)
    company = models.ForeignKey(Company, related_name='advertisements', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.title}'


class TagValue(BaseModel):
    tag = models.ForeignKey(Tag, related_name='values', on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, related_name='tag_values', on_delete=models.CASCADE)
    value = ArrayField(models.CharField(max_length=50, blank=True))

    def __str__(self):
        return f'{self.value}'

    class Meta:
        unique_together = ('tag', 'advertisement')


class CrawlerConfig(BaseModel):
    TEHRAN = 0
    ALBORZ = 1
    ESFEHAN = 2
    CITY_CHOICES = (
        (TEHRAN, 'تهران'),
        (ALBORZ, 'البرز'),
        (ESFEHAN, 'اصفهان')
    )

    JOBINJA = 0
    JOBVISION = 1
    QUERA = 2
    SOURCE_CHOICES = (
        (JOBINJA, 'جابینجا'),
        (JOBVISION, 'جاب ویژن'),
        (QUERA, 'کوئرا')
    )

    source = models.PositiveSmallIntegerField(choices=SOURCE_CHOICES, default=JOBINJA)
    city = models.PositiveSmallIntegerField(choices=CITY_CHOICES, default=TEHRAN)
    url = models.TextField(unique=True)
