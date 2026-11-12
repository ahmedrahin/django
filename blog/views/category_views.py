from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from blog.models import Category
from blog.forms import CategoryForm


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    ordering = ['name']


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all().order_by('-created_at')
        return context


class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category/category_form.html'
    success_url = reverse_lazy('category_list')
    success_message = 'Category "%(name)s" created successfully.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Category'
        context['button_text'] = 'Create Category'
        return context


class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category/category_form.html'
    success_url = reverse_lazy('category_list')
    success_message = 'Category "%(name)s" updated successfully.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Category: {self.object.name}'
        context['button_text'] = 'Update Category'
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'blog/category/category_confirm_delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('category_list')

    def post(self, request, *args, **kwargs):
        category = self.get_object()
        messages.success(request, f'Category "{category.name}" deleted successfully.')
        return super().post(request, *args, **kwargs)

