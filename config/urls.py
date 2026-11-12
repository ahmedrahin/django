"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.contrib import messages
from blog.models import Post, Category


def home(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'set':
            val = request.POST.get('session_value', '').strip()
            if val:
                request.session['test_value'] = val
                messages.success(request, f'Session set: "{val}"')
        elif action == 'delete':
            if 'test_value' in request.session:
                del request.session['test_value']
                messages.info(request, 'Session value deleted.')
        return redirect('home')

    session_value = request.session.get('test_value')
    recent_posts = Post.objects.all().order_by('-created_at')[:3]
    categories = Category.objects.all()[:6]
    return render(request, 'home.html', {
        'recent_posts': recent_posts,
        'categories': categories,
        'session_value': session_value,
    })


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('shop/', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)