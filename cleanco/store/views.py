from django.shortcuts import render
from django.http import JsonResponse
from .models import Category, Product

from django.shortcuts import get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
import re


def store(request):
    all_products = Product.objects.all()
    # Define the number of products per page
    products_per_page = 8

    # Create a Paginator instance
    paginator = Paginator(all_products, products_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get("page")

    try:
        # Get the products for the current page
        all_products = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        all_products = paginator.page(1)
    except EmptyPage:
        # If the page parameter is out of range, show the last page
        all_products = paginator.page(paginator.num_pages)
    context = {
        "my_products": all_products,
    }

    return render(request, "store/store.html", context)


def categories(request):
    all_categories = Category.objects.all()

    return {"all_categories": all_categories}


def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    # Define the number of products per page
    products_per_page = 8

    # Create a Paginator instance
    paginator = Paginator(products, products_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get("page")

    try:
        # Get the products for the current page
        products = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        products = paginator.page(1)
    except EmptyPage:
        # If the page parameter is out of range, show the last page
        products = paginator.page(paginator.num_pages)

    return render(
        request,
        "store/list-category.html",
        {"category": category, "products": products},
    )


def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    context = {"product": product}

    return render(request, "store/product-info.html", context)


def search(request):
    query = request.GET.get("q", "")

    products = Product.objects.filter(Q(title__iregex=r"^.*%s.*$" % re.escape(query)))
    product_count = products.count()
    context = {
        "products": products,
        "query": query,
        "product_count": product_count,
    }

    return render(request, "store/search-results.html", context)


def search_suggestions(request):
    query = request.GET.get("q", "")
    suggestions = Product.objects.filter(
        title__iregex=r"^.*%s.*$" % re.escape(query)
    ).values_list("title", flat=True)
    return JsonResponse(list(suggestions), safe=False)
