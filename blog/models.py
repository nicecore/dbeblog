from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
                                            .filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                            choices=STATUS_CHOICES,
                            default='draft')
    # Default model manager
    objects = models.Manager()
    # Custom model manager
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
        
        
    def get_absolute_url(self):
        # Return the absolute URL of each individual post object
        # Returns a reverse() to the post_detail view and provides keyword arguments
        # with the times coming from strftime
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.strftime('%m'),
                self.publish.strftime('%d'),
                self.slug
            ]
        )
