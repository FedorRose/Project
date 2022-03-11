from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Name")
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop', kwargs={'category_slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.PROTECT)
    name = models.CharField(max_length=200, db_index=True, verbose_name="Name")
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name="Image")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    sale = models.IntegerField(default=0, verbose_name="Sale")
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    total_rating = models.IntegerField(default=0)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop_single', kwargs={'product_slug': self.slug,
                                              'category_slug': Category.slug,
                                              'product_id': self.pk})


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name="Title")
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="URL")
    text = models.TextField(blank=True, verbose_name="Full Text")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name="Image")
    publish = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True, verbose_name="Is published")
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_single', kwargs={'post_slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='Comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


RATING_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),

]


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='Reviews', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    title = models.CharField(max_length=250)
    text = models.TextField(max_length=1500)
    rating = models.IntegerField(choices=RATING_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('product',)

    def __str__(self):
        return 'Review by {} on {}'.format(self.name, self.product)

    def return_rating(self):
        lr = []
        if self.rating == 5:
            lr = [1, 1, 1, 1, 1]
        elif self.rating == 4:
            lr = [1, 1, 1, 1, 0]
        elif self.rating == 3:
            lr = [1, 1, 1, 0, 0]
        elif self.rating == 2:
            lr = [1, 1, 0, 0, 0]
        elif self.rating == 1:
            lr = [1, 0, 0, 0, 0]

        return lr
