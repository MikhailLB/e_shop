from lib2to3.fixes.fix_input import context

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category

class ProductListView(ListView):
    context_object_name = 'products'
    template_name = 'shop/product/list.html'

    def get_queryset(self):
        # Основной фильтр для доступных продуктов
        queryset = Product.objects.filter(available=True)

        # Если передан slug, фильтруем по категории
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        # Добавляем категории в контекст
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        if slug:
            category = get_object_or_404(Category, slug=slug)
            context['category'] = category
        return context

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product_detail'
    template_name = 'shop/product/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('id')
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, id=id, slug=slug)
        context['product'] = product
        return context

#405