from django.contrib import admin
from django.urls import path,include
from . import views
# from recipe_data.views import search
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('search/',include('recipe_data.urls'),name='search'),
    path('calculator/',include('calaries_tracker.urls'),name='calculator'),
    path('users/', include('user_auth.urls'),name='users'),
    path('navbar/',views.navbar,name='navbar'),
    # path('account/',include('accounts.urls')),
    # path('search/',search)
]