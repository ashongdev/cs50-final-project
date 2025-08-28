from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from dotenv import load_dotenv
from rest_framework.decorators import api_view

load_dotenv()


# Create your views here.
def index(request):
    print(request.userx)
    return HttpResponse("http://localhost:5173")


@api_view(["GET"])
def check_user(request):
    user = request.user

    if user.is_authenticated:
        return JsonResponse(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        )

    else:
        return JsonResponse({"message": "Authentication details not provided"})


@api_view(["POST"])
def create_new_note(request):
    content = request.data.get("content")

    print(content)
    if request.user.is_authenticated:
        print("Is authenticated")
    else:
        print("Is not authenticated")
    return HttpResponse("")


def login_view(request):
    print("Yes Ikm hegru")
    if request.user.is_authenticated:
        # return redirect(reverse("index"))
        ...

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponse("index")
        else:
            # return render(
            #     request,
            #     "network/login.html",
            #     {"message": "Invalid username and/or password."},
            # )
            ...

    else:
        ...
        # return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponse("index")


def register(request):
    if request.user.is_authenticated:
        # return redirect(reverse("index"))
        ...

    if request.method == "POST":
        # username = request.POST["username"]
        # email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            # return render(
            #     request, "network/register.html", {"message": "Passwords must match."}
            # )
            ...
        # Attempt to create new user
        try:
            ...
            # user = User.objects.create_user(username, email, password)
            # user.save()
        except IntegrityError:
            # return render(
            #     request, "network/register.html", {"message": "Username already taken."}
            # )
            ...
        # login(request, user)
        return HttpResponse("index")
    else:
        # return render(request, "network/register.html")
        ...
