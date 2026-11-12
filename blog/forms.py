from django import forms
from blog.models import Post, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name',
                'placeholder': 'Enter category name',
                'style': 'width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ddd; border-radius: 4px;',
            }),
        }
        error_messages = {
            'name': {
                'required': 'Category name is required.',
                'unique': 'This category already exists.',
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 2:
            raise forms.ValidationError('Category name must be at least 2 characters long.')
        return name.strip()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'description', 'thumb']
        widgets = {
            'category': forms.Select(attrs={
                'id': 'id_category',
                'style': 'width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ddd; border-radius: 4px;',
            }),
        }
        error_messages = {
            'title': {
                'required': 'Title is required.',
                'unique': 'This title already exists. Please choose a different title.',
            },
        }

    # Custom backend validation example for title
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long.')
        return title
