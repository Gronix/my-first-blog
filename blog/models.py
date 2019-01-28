from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                                            .filter(status='published')


class Post(models.Model):
    # author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # title = models.CharField(max_length=200)
    title = models.CharField(max_length=250)
    # text = models.TextField()
    body = models.TextField()
    # created_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    # published_date = models.DateTimeField(blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    
    #---- new fields:
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager()  # Custom Django's QuerySet manager

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # from previous stage of blog creating:
    def _publish(self):
        self.published_date = timezone.now()
        self.save()
