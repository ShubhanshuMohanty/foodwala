from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user_auth.middlewares import auth
import json
import os
import requests
from django.conf import settings
from django.contrib import messages
from .models import Meal
from urllib.parse import unquote_plus
from django.db.models import Sum
# Create your views here.
@auth
def search(request):
    return render(request, 'search.html')

def sm(request):
    return render(request, 'sm.html')

def ingridient_search_sugguestions(request):
    query=request.GET.get('q','').lower()
    
    file_path = os.path.join(settings.BASE_DIR, "recipe_data", "unique_ingridients.json")
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

    
    params = {
        "ingredients": ingredients,  
        "number": 10,                
        "apiKey": api_key            
    }

    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        # **Filtered Data**
        filtered_data = []
        for recipe in data:
            all_ingredients = [
                ing["name"] for ing in recipe.get("usedIngredients", [])
            ] + [
                ing["name"] for ing in recipe.get("missedIngredients", [])
            ]

            filtered_data.append({
                "id": recipe["id"],
                "title": recipe["title"],
                "image": recipe["image"],
                "ingredients": all_ingredients
        })
        # return JsonResponse({"recipes": filtered_data})
        return render(request, "recipeList.html", {"recipes": filtered_data})
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def recipe_details(request, id):
    api_url = f"https://api.spoonacular.com/recipes/{id}/information"
    url = f"https://api.spoonacular.com/recipes/{id}/nutritionWidget.json"
    api_key = "e1567f12699e4d64b65deff4634c8b1b"

    params = {
        "apiKey": api_key 
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  

        data = response.json()
        response=requests.get(url, params=params)
        response.raise_for_status() 
        n_data=response.json()
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

        nutrition_data={
            "calories":n_data["calories"],
            "fat":n_data["fat"],
            "protein":n_data["protein"],
            "carbs":n_data["carbs"]
        }

        # if request.method == "POST":
            # messages.success(request, "Recipe saved successfully!")
            # return redirect("/food_table/")

        # return JsonResponse(recipe_info)
        return render(request, "recipe.html", {"recipe": recipe_info,"nutrition":nutrition_data})

    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    
    
def food_table(request):
    meal_data = Meal.objects.filter(user=request.user)
    meal=meal_data.aggregate(
        tot_calories=Sum('calories'),
        tot_protein=Sum('protein')
    )

    total_data={
        "tot_calories":meal['tot_calories'],
        "tot_protein":meal['tot_protein'],
    }
    # print("Meal Data:", meal_data)
    print("Total Data:",total_data)
    return render(request, 'food_table.html', {"meals": meal_data,"total_data":total_data})
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
            print('\n\n\n\n Meal:', meal)
            return JsonResponse({"message": "Recipe added successfully!"})

        return JsonResponse({"error": "Invalid request"}, status=400)

        # return JsonResponse({"error": "Invalid request"}, status=400)

    except Exception as e:
        print("error",e)
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def delete_meal(request,title):
    decoded_title = unquote_plus(title) 
    print("\n\n\ntitle=",title)
    print("\n\n\ndecoded_title=",decoded_title)
    try:
        if request.method=="DELETE":
            meal=get_object_or_404(Meal,user=request.user,recipe_title=title)
            # meal = Meal.objects.get(title=decoded_title)
            # meal = Meal.objects.filter(title=decoded_title, user=request.user)
            print("\n\n\nmeal=",meal)

            meal.delete()
            print("\n\n\nmeal deleted")
            return JsonResponse({"message":"Meal deleted successfully!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
