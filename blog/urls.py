from django.urls import path
from .views import post_views, comment_views, category_views


urlpatterns = [
    # Post URLs
    path('', post_views.list, name="list"),
    path('create/', post_views.create, name="blog_create"),
    path('details/<int:id>', post_views.details, name="blog_details"),
    path('edit/<int:id>', post_views.edit, name="blog_edit"),
    path('delete/<int:id>', post_views.delete, name="blog_delete"),

    # Category CBV URLs
    path('categories/', category_views.CategoryListView.as_view(), name="category_list"),
    path('categories/create/', category_views.CategoryCreateView.as_view(), name="category_create"),
    path('categories/<int:pk>/', category_views.CategoryDetailView.as_view(), name="category_detail"),
    path('categories/<int:pk>/edit/', category_views.CategoryUpdateView.as_view(), name="category_edit"),
    path('categories/<int:pk>/delete/', category_views.CategoryDeleteView.as_view(),name="category_delete"),
]
