from django.db.models import Q
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .wishlist import Wishlist
from .forms import *
from cart.forms import CartAddProductForm


def index(request):
    if request.method == 'POST':
        form = ContactFormLetter(request.POST)
        if form.is_valid():
            sub = 'Subscribe'
            message = 'Join to our Newsletter this email: '
            sender = form.cleaned_data['email']
            send_mail(sub, message + sender, sender, ['fserlisiy@yandex.ru'])
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ContactFormLetter()

    last_blog = Post.objects.filter(status=True).order_by('-publish')[:2]
    products = Product.objects.filter(available=True)
    last_products = products.order_by('-created')[:6]
    recent = products.order_by('total_rating')[:12]
    wishlist = Wishlist(request).list()
    cart_product_form = CartAddProductForm()
    categories = Category.objects.all()

    return render(request, 'main/index.html', {'form': form,
                                               'blog': last_blog,
                                               'last': last_products,
                                               'recent': recent,
                                               'wishlist': wishlist,
                                               'cart_product_form': cart_product_form,
                                               'categories': categories,
                                               'title': "Main"})


def shop(request, category_slug):
    category = None
    products = Product.objects.filter(available=True)
    if category_slug != 'all':
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    sort = sort_mapping.get("Rating")
    sort_form = request.GET.get('sort')
    if sort_form:
        sort_need = sort_mapping.get(sort_form)
    else:
        sort_need = sort
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(Q(name__icontains=search_query) |
                                   Q(description__icontains=search_query))

    products = products.order_by(sort_need, sort)
    categories = Category.objects.all()
    cart_product_form = CartAddProductForm()
    wishlist = Wishlist(request).list()
    p = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, 'main/shop.html', {'el': page_obj,
                                              'categories': categories,
                                              'category': category,
                                              'products': products,
                                              'sm': sort_mapping,
                                              'cart_product_form': cart_product_form,
                                              'wishlist': wishlist,
                                              'title': "Shop"})


def shop_single(request, product_slug, category_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    reviews = product.Reviews.filter(active=True).order_by('-created')
    s, c, total_rating = 0, 0, 0
    lr = []
    for i in reviews:
        s += sum(i.return_rating())
        c += 1
    if c:
        total_rating = round(s/c)

    if total_rating == 5:
        lr = [1, 1, 1, 1, 1]
    elif total_rating == 4:
        lr = [1, 1, 1, 1, 0]
    elif total_rating == 3:
        lr = [1, 1, 1, 0, 0]
    elif total_rating == 2:
        lr = [1, 1, 0, 0, 0]
    elif total_rating == 1:
        lr = [1, 0, 0, 0, 0]

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.save()
            product.total_rating = product.total_rating + review_form.cleaned_data['rating']
            product.save()

        return HttpResponseRedirect(reverse('shop_single', args=[category_slug, product_slug]))
    else:
        review_form = ReviewForm()
    cart_product_form = CartAddProductForm()
    categories = Category.objects.all()
    wishlist = Wishlist(request).list()

    return render(request, 'main/shop-single-product.html', {'product': product,
                                                             'form': review_form,
                                                             'reviews': reviews,
                                                             'total_rating': lr,
                                                             'count': c,
                                                             'cart_product_form': cart_product_form,
                                                             'categories': categories,
                                                             'wishlist': wishlist,
                                                             'title': "Product"})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            send_mail(name, message, sender, ['fserlisiy@yandex.ru'])
            return HttpResponseRedirect(reverse('contact'))
    else:
        form = ContactForm()
    categories = Category.objects.all()

    return render(request, 'main/contact.html', {'form': form, 'categories': categories, 'title': "Contact"})


def about(request):
    categories = Category.objects.all()
    return render(request, 'main/about.html', {'categories': categories, 'title': "About"})


def wishlist_view(request):
    wishlist = Wishlist(request)
    cart_product_form = CartAddProductForm()
    categories = Category.objects.all()
    return render(request, 'main/shop-wishlist.html', {'wishlist': wishlist,
                                                       'cart_product_form': cart_product_form,
                                                       'categories': categories,
                                                       'title': "Wishlist"})


def wishlist_add(request, product_id):
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'GET':
        wishlist.add(product=product)
    return redirect('wishlist_view')


def wishlist_remove(request, product_id):
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    wishlist.remove(product)
    return redirect('wishlist_view')


def blog(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(text__icontains=search_query))
    else:
        posts = Post.objects.filter(status=True)
    recent = Post.objects.all().order_by('-views')[:3]
    p = Paginator(posts, 3)
    page_number2 = request.GET.get('page')
    page_obj2 = p.get_page(page_number2)
    categories = Category.objects.all()

    return render(request, 'main/blog.html', {'el': page_obj2,
                                              'posts': posts,
                                              'recent': recent,
                                              'categories': categories,
                                              'title': "Blog"})


def blog_single(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = post.Comments.filter(active=True)
    count = comments.count()
    obj = post
    obj.views = obj.views+1
    obj.save()
    recent = Post.objects.all().order_by('-views')[:3]
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return HttpResponseRedirect(reverse('blog_single', args=[post_slug]))
    else:
        comment_form = CommentForm()
    categories = Category.objects.all()

    return render(request, 'main/blog-details.html', {'post': post,
                                                      'comments': comments,
                                                      'count': count,
                                                      'comment_form': comment_form,
                                                      'recent': recent,
                                                      'categories': categories,
                                                      'title': "Page"})

