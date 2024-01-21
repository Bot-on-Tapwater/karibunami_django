from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
import json
import requests
from .models import Place, Bookmark
from django.http import JsonResponse

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def index(request):
    return render(
        request,
        "karibunami/index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )

""" 
DEPRECATED BY AUTH0!!!

@require_http_methods(["GET", "POST"])
@csrf_exempt
def register_user(request):
    return HttpResponse("Register User Accounts")

def verify_user(request):
    return HttpResponse("Verify User Accounts")

@require_http_methods(["GET", "POST"])
@csrf_exempt
def resend_link(request):
    return HttpResponse("Resend verification link to user")

@require_http_methods(["GET", "POST"]) # Consider using a PUT request instead
@csrf_exempt
def reset_password(request):
    return HttpResponse("Reset User Accounts Passwords")

@require_http_methods(["GET", "POST"])
@csrf_exempt
def reset_password_link(request):
    return HttpResponse("Helper function for 'reset_password'")

DEPRECATED BY AUTH0!!!
"""

"""START OF AUTHO"""
@require_http_methods(["GET", "POST"])
@csrf_exempt
def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("karibunami:callback"))
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("karibunami:index")))

def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("karibunami:index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )
"""END OF AUTHO"""

@require_http_methods(["POST"])
@csrf_exempt
def get_places(request):
    all_nearby_places = []
    new_places = []
    new_bookmarks = []

    # Get user session for checking if user signed in
    session = request.session.get("user")

    # From Frontend
    PLACE = request.POST["place_name"]
    # LATITUDE = request.POST["location-lat"]
    # LONGITUDE = request.POST["location-long"]
    # LOCATION = "{},{}".format(LATITUDE, LONGITUDE)

    # Parameters for places photos api
    MAXWIDTH = 400
    PHOTO_REFERENCE = ""
    

    # Westlands location placeholder as Frontend gets built
    # PLACE = "shop"
    LOCATION = "-1.2519923507234287, 36.805050379582305"
    SEARCH_RADIUS = 1000
    API_KEY = settings.GOOGLE_API_KEY

    nearby_places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword={PLACE}&location={LOCATION}&radius={SEARCH_RADIUS}&type=&key={API_KEY}"

    try:
        response = requests.get(nearby_places_url).json()["results"]
    except Exception:
        return HttpResponse("API call to Google (Nearby Places) failed")
    

    for place in response:
        # print(f"place: {place}")
        single_place_result = {}
        name = place["name"]
        place_id = place["place_id"]
        rating = place["rating"]
        location = place["geometry"]['location']
        loc_lat = location['lat']
        loc_long = location['lng']
        maps_url = f'https://www.google.com/maps?q={loc_lat},{loc_long}'

        # Get contact info and open/close status from places details api
        try:
            PLACE_ID = place_id

            # This is a repetition of the URL provided above, resolve duplicates
            response = requests.get(f"https://maps.googleapis.com/maps/api/place/details/json?placeid={PLACE_ID}&fields=&key={API_KEY}")
            response.raise_for_status()
            place_id_data = response.json()

            if "formatted_phone_number" in place_id_data["result"]:
                contacts = place_id_data["result"]["formatted_phone_number"]
            else:
                contacts = None
            
            if "current_opening_hours" in place_id_data["result"]:
                if "open_now" in place_id_data["result"]["current_opening_hours"]:
                    open_now = place_id_data["result"]["current_opening_hours"]["open_now"]
                else:
                    open_now = None
            else:
                open_now = None
            
            if "photos" in place_id_data["result"]:
                count = 0
                photographs = []
                for photo in place_id_data["result"]["photos"]:
                    if count > 2:
                        break
                    else:
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={MAXWIDTH}&photo_reference={photo['photo_reference']}&key={API_KEY}"
                        photographs.append(photo_url)
                        count += 1
            else:
                # set a default image for places with none
                photographs = ["https://media.istockphoto.com/id/1392182937/vector/no-image-available-photo-coming-soon.jpg?s=612x612&w=0&k=20&c=3vGh4yj0O2b4tPtjpK-q-Qg0wGHsjseL2HT-pIyJiuc="]
                # photographs = None


            # get the place's reviews
            place_reviews = []
            if "reviews" in place_id_data["result"]:
                reviews = place_id_data["result"]["reviews"]
                for review in reviews:
                    place_reviews.append({
                        "author_name": review.get("author_name", "name undisclosed"),
                        "author_dp": review.get("profile_photo_url", "https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png"),
                        "rating": review.get("rating", 3),
                        "time_posted": review.get("relative_time_description", "a while ago"),
                        "review_text": review.get("text", "No comment")
                    })

        except Exception as e:
            print(f"Request failed: {e}")
        
        single_place_result["place_name"] = name
        single_place_result["rating"] = rating
        single_place_result["open_now"] = open_now
        single_place_result["mobile_number"] = contacts
        single_place_result["location"] = maps_url
        single_place_result["photos"] = photographs
        single_place_result["reviews"] = place_reviews
        single_place_result["google_api_place_id"] = place_id

        if session:
            single_place_result["bookmarked"] = False
        
        all_nearby_places.append(single_place_result)

        if not Place.objects.filter(google_api_place_id=place_id).exists():
            new_place = Place(
                    google_api_place_id=place_id,
                    name=name,   rating=rating,
                    open_now=open_now,
                    mobile_number=contacts,
                    location=maps_url,
                    photos=json.dumps(photographs),
                    reviews=json.dumps(place_reviews)
                    )
            new_places.append(new_place)
    
    # Create all new records in DB at once
    Place.objects.bulk_create(new_places)

    for place in all_nearby_places:
        if session and not (Bookmark.objects.filter(place_id=place["google_api_place_id"], user_id=session["userinfo"]["sub"])):
            # print(f"User is signed in, add bookmarks")
            new_bookmark = Bookmark(
                user_id=session["userinfo"]["sub"],
                user_name=session["userinfo"]["name"],
                place_id=get_object_or_404(Place, google_api_place_id=place["google_api_place_id"]),
                bookmarked=False
            )
            new_bookmarks.append(new_bookmark)

    Bookmark.objects.bulk_create(new_bookmarks)

    return JsonResponse(all_nearby_places, safe=False)


@require_http_methods(["GET"])
def get_place_details(request, place_id: str):
    try:
        place_details = Place.objects.get(pk=place_id)
        return JsonResponse(place_details.to_dict(), safe=False)
    except Exception:
        return HttpResponse(f"Place with PLACE ID: {place_id} not found")    

# @require_http_methods(["PUT"])
@csrf_exempt
def bookmark_place(request, place_id: str):
    # return HttpResponse("Allows user to bookmark a place for future reference")
    session = request.session.get("user")
    if session:
        bookmark = Bookmark.objects.filter(place_id=place_id, user_id=session["userinfo"]["sub"]).first()
        # print(f"{bookmark}")
        if bookmark.bookmarked is False:
            bookmark.bookmarked = True
            bookmark.save()
        else:
            bookmark.bookmarked = False
            bookmark.save()
        return HttpResponse("Bookmark Works")
    return HttpResponse("Bookmark Doesn't Work")

@require_http_methods(["GET"])
def bookmarked_places(request):
    session = request.session.get("user")
    if session:
        bookmarked_places = []
        bookmarks = Bookmark.objects.filter(user_id=session["userinfo"]["sub"], bookmarked=True)

        for bookmark in bookmarks:
            bookmarked_places.append(bookmark.to_dict())
        
        return JsonResponse(bookmarked_places, safe=False)

    # return HttpResponse("Return places that a signed in user has bookmarked")

'''CSRF TOKEN'''

def get_csrf_token(request):
    csrf_token = request.COOKIES.get('csrftoken', '')
    return JsonResponse({'csrf_token': csrf_token})

