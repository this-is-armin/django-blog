from django.urls import path
from . import views


app_name = 'app'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.DetailView.as_view(), name='detail'),
    
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
]