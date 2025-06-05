from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user_auth.middlewares import auth
import json
import os
import requests
from django.conf import settings
from django.contrib import messages
from .models import Meal, premium_member
from urllib.parse import unquote_plus
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from user_auth.models import CustomUser as User,Profile

# from django.views.decorators.csrf import csrf_exempt
import razorpay

# Create your views here.
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@auth
def search(request):
    return render(request, "search.html")


def sm(request):
    return render(request, "sm.html")


def ingridient_search_sugguestions(request):
    query = request.GET.get("q", "").lower()

    file_path = os.path.join(
        settings.BASE_DIR, "recipe_data", "unique_ingridients.json"
    )
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Search logic
        results = [item for item in data if query in item["name"].lower()][:10]

        return JsonResponse({"suggestions": results})
        # return JsonResponse([results])
    except FileNotFoundError:
        return JsonResponse({"error": "File not found"}, status=500)


def fetch_recipes(request):
    api_url = "https://api.spoonacular.com/recipes/findByIngredients"
    api_key = "e1567f12699e4d64b65deff4634c8b1b"

    ingredients = request.GET.get("ingredients", "")

    if not ingredients:
        return JsonResponse({"error": "No ingredients provided"}, status=400)

    params = {"ingredients": ingredients, "number": 10, "apiKey": api_key}

    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        # **Filtered Data**
        filtered_data = []
        for recipe in data:
            all_ingredients = [
                ing["name"] for ing in recipe.get("usedIngredients", [])
            ] + [ing["name"] for ing in recipe.get("missedIngredients", [])]

            filtered_data.append(
                {
                    "id": recipe["id"],
                    "title": recipe["title"],
                    "image": recipe["image"],
                    "ingredients": all_ingredients,
                }
            )
        # return JsonResponse({"recipes": filtered_data})
        return render(request, "recipeList.html", {"recipes": filtered_data})
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def recipe_details(request, id):
    api_url = f"https://api.spoonacular.com/recipes/{id}/information"
    url = f"https://api.spoonacular.com/recipes/{id}/nutritionWidget.json"
    api_key = "e1567f12699e4d64b65deff4634c8b1b"

    params = {"apiKey": api_key}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        data = response.json()
        response = requests.get(url, params=params)
        response.raise_for_status()
        n_data = response.json()
        # Extract required fields
        recipe_info = {
            "image": data.get("image"),
            "title": data.get("title"),
            "readyInMinutes": data.get("readyInMinutes"),
            "vegetarian": data.get("vegetarian"),
            "servings": data.get("servings"),
            "dishTypes": data.get("dishTypes"),
            "diets": data.get("diets"),
            "summary": data.get("summary"),
            "instructions": [
                {"number": step["number"], "step": step["step"]}
                for instruction in data.get("analyzedInstructions", [])
                for step in instruction.get("steps", [])
            ],
        }

        nutrition_data = {
            "calories": n_data["calories"],
            "fat": n_data["fat"],
            "protein": n_data["protein"],
            "carbs": n_data["carbs"],
        }

        # if request.method == "POST":
        # messages.success(request, "Recipe saved successfully!")
        # return redirect("/food_table/")

        # return JsonResponse(recipe_info)
        obj=premium_member.objects.get(user=request.user)
        return render(
            request, "recipe.html", {"recipe": recipe_info, "nutrition": nutrition_data,"is_paid":obj.is_paid}
        )

    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def food_table(request):
    meal_data = Meal.objects.filter(user=request.user)
    meal = meal_data.aggregate(tot_calories=Sum("calories"), tot_protein=Sum("protein"))

    total_data = {
        "tot_calories": meal["tot_calories"],
        "tot_protein": meal["tot_protein"],
    }
    # print("Meal Data:", meal_data)
    print("Total Data:", total_data)
    return render(
        request, "food_table.html", {"meals": meal_data, "total_data": total_data}
    )
    # return render(request, 'food_table.html')


def add_to_meal(request):
    try:
        if request.method == "POST":
            # JSON body ko parse karein
            data = json.loads(request.body)

            recipe_title = data.get("recipe_title")
            calories = data.get("calories")
            protein = data.get("protein")[0:-1]
            fat = data.get("fat")[0:-1]
            carbs = data.get("carbs")[0:-1]

            # Validate data
            if not recipe_title or not calories or not protein or not fat or not carbs:
                return JsonResponse({"error": "Invalid data"}, status=400)

            # Save to database
            meal = Meal.objects.create(
                user=request.user,
                recipe_title=recipe_title,
                calories=int(calories),
                protein=float(protein),
                fat=float(fat),
                carbs=float(carbs),
            )
            print("\n\n\n\n Meal:", meal)
            return JsonResponse({"message": "Recipe added successfully!"})

        return JsonResponse({"error": "Invalid request"}, status=400)

        # return JsonResponse({"error": "Invalid request"}, status=400)

    except Exception as e:
        print("error", e)
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def delete_meal(request, title):
    # decoded_title = unquote_plus(title)
    print("\n\n\ntitle=", title)
    # print("\n\n\ndecoded_title=", decoded_title)
    try:
        if request.method == "DELETE":
            meal = get_object_or_404(Meal, user=request.user, id=title)
            # meal = Meal.objects.get(title=decoded_title)
            # meal = Meal.objects.filter(title=decoded_title, user=request.user).first()
            print("\n\n\nmeal=", meal)

            if meal:
                meal.delete()
                print("\n\n\nmeal deleted")
                return JsonResponse({"message": "Meal deleted successfully!"})
            else:
                return JsonResponse({"error": "Meal not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class CreatePaymentView(LoginRequiredMixin, View):
    def post(self, request):
        # user = get_object_or_404(User, email=request.user.email)
        data = json.loads(request.body)
        return_url = data.get('return_url')
        # response.set_cookie(return_url)
        if return_url:
            request.session['return_url'] = return_url
        # request.session['return_url'] = request.build_absolute_uri()
        print("\n\n\nrequest.session['return_url']=", request.session['return_url'])
        order_data = {
            "amount": int(200 * 100),
            "currency": "INR",
            "payment_capture": "1",
        }
        razorpay_order = client.order.create(order_data)
        pm_object = premium_member.objects.filter(user=request.user).first()
        if pm_object:
            pm_object.razorpay_order_id = razorpay_order["id"]
            pm_object.amount=200
            pm_object.save()
        # premium_member.objects.create(
        #     user=request.user,
        #     # product = product,
        #     amount=200,
        #     razorpay_order_id=razorpay_order["id"],
        # )
        profile_data=Profile.objects.get(user__email=request.user.email)
        response= JsonResponse(
            {
                "order_id": razorpay_order["id"],
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "product_name": request.user.email,
                "amount": order_data["amount"],
                "razorpay_callback_url": settings.RAZORPAY_CALLBACK_URL,
                "name": profile_data.name,
                "phone": profile_data.phone,
                "return_url":return_url,
            }
        )
        response.set_cookie('return_url', return_url)
        return response

@method_decorator(csrf_exempt, name='dispatch')
class PaymentCallbackView(View):
    def post(self, request):
        if "razorpay_signature" in request.POST:
            order_id = request.POST.get("razorpay_order_id")
            payment_id = request.POST.get("razorpay_payment_id")
            signature = request.POST.get("razorpay_signature")
            return_url=request.POST.get("return_url")
            order = get_object_or_404(premium_member, razorpay_order_id=order_id)
            print("\n\n\norder=", order)
            print("\n\n\nreturn_url=", return_url)


            if client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }):

                order.razorpay_payment_id = payment_id
                order.razorpay_signature = signature
                order.is_paid = True
                order.save()
                # return redirect(return_url)
                # return_url = request.session.pop("return_url", "/search/")
                return_url = request.COOKIES.get('return_url')
                return redirect(return_url)
            else:
                order.is_paid = False
                order.save()
                return JsonResponse({"status": "failed"})
        else:
            return JsonResponse({"status": "failed!!"})
        

def fetch_dishes(request):
    query= request.GET.get("query", "").lower()
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)
    api_url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}"
    api_key = "e1567f12699e4d64b65deff4634c8b1b"
    try:
        response = requests.get(api_url, params={"apiKey": api_key})
        data = response.json()
        # **Filtered Data**
        filtered_data = []
        for recipe in data["results"]:
            filtered_data.append(
                {
                    "id": recipe["id"],
                    "title": recipe["title"],
                    "image": recipe["image"],
                }
            )
        return render(request, "recipeList.html", {"recipes": filtered_data})
        # return JsonResponse({"recipes": filtered_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
