from django.urls import path
from . import views
from .views import CreatePaymentView,PaymentCallbackView
urlpatterns = [
    path('',views.search,name="search"),
    path("sm/",views.sm),
    path("search_suggestions/",views.ingridient_search_sugguestions,name="search_suggestions"),
    path("fetch_recipes/",views.fetch_recipes,name="fetch_recipes"),
    path("recipe_details/<int:id>",views.recipe_details,name="recipe_details"),
    path("food_table/",views.food_table,name="food_table"),
    path("add_to_meal/", views.add_to_meal, name="add_to_meal"),
    # path("delete_meal/<str:title>",views.delete_meal,name="delete_meal"),
    path("delete_meal/<int:title>",views.delete_meal,name="delete_meal"),
    path("create-payment/", CreatePaymentView.as_view(), name="create_payment"),
    path("payment-verify/", PaymentCallbackView.as_view(), name="payment_verify"),
    path("fetch_dishes/",views.fetch_dishes,name="fetch_dishes"),
]