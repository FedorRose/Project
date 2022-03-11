from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'total_rating']
    list_filter = ['available', 'created']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'publish', 'photo', 'status')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('status',)
    list_filter = ('publish',)
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'text', 'created', 'active')
    readonly_fields = ('post', 'name', 'text', 'created',)
    list_display_links = ('post', 'name', 'text',)
    list_editable = ('active',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'title', 'text', 'rating', 'created', 'active')
    readonly_fields = ('product', 'name', 'title', 'text', 'rating', 'created')
    list_display_links = ('product', 'name', 'title', 'text')
    list_editable = ('active',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
