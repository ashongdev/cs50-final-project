from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from dotenv import load_dotenv
from rest_framework.decorators import api_view

from .models import Note, Tag

load_dotenv()


# Create your views here.
def index(request):
    # notes = [
    #     {
    #         "id": 4,
    #         "title": "Weekly Workout Plan",
    #         "tags": ["Dev", "React"],
    #         "updated_at": date.today(),
    #         "isActive": False,
    #         "content": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Cum rem, libero quia omnis perferendis minus, voluptas mollitia laudantium nemo odio aliquam veritatis illum fugiat magnam delectus dolorem iusto corporis deleniti.",
    #     },
    # ]

    all_notes = []

    if request.user.is_authenticated:
        # Get user's notes
        notes = Note.objects.filter(author=request.user).all()

        # Get user's tags
        tags = []
        note_tags = Tag.objects.filter(note_id__author=request.user)

        for tag in note_tags:
            tags.append(
                {"tag_id": tag.pk, "note_id": tag.note_id.pk, "tag_name": tag.tag_name}
            )

        for note in notes:
            each_notes_tag = set()
            for tag in note_tags:
                if note.pk == tag.note_id.pk:
                    each_notes_tag.add(tag.tag_name)
            each_notes_tag = list(each_notes_tag)
            print(each_notes_tag)

            all_notes.append(
                {
                    "id": note.pk,
                    "title": note.title,
                    "content": note.content,
                    "is_deleted": note.is_deleted,
                    "is_archived": note.is_archived,
                    "created_at": note.created_at,
                    "updated_at": note.updated_at,
                    "tags": each_notes_tag,
                }
            )
    else:
        return redirect(reverse("login"))

    return render(request, "final_project/index.html", {"notes": all_notes})


@api_view(["POST", "GET"])
def create_new_note(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            content = request.data.get("content")
            title = request.data.get("title")
            tag_input = request.data.get("tags")

            tags = []

            for word in tag_input.split(","):
                tags.append(word.strip())

            n = Note(title=title, content=content, author=request.user)
            n.save()

            for tag in tags:
                t = Tag(note_id_id=n.pk, tag_name=tag)
                t.save()

            return redirect(reverse("index"))
        else:
            return render(request, "final_project/create.html")
    else:
        return redirect(reverse("login"))


@api_view(["POST", "GET"])
def forgot_password_view(request):
    if request.method == "POST":
        ...
    else:
        return render(request, "final_project/forgot_password.html")
    ...


def forgot_password_page(request):
    return render(request, "forgot_password.html")


@api_view(["POST", "GET"])
def login_view(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            # Attempt to sign user in
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return redirect(reverse("index"))
            else:
                return render(
                    request,
                    "final_project/login.html",
                    {"message": "Invalid username and/or password."},
                )
    else:
        return render(request, "final_project/login.html")


def logout_view(request):
    logout(request)
    return redirect(reverse("login"))


@api_view(["POST", "GET"])
def register(request):
    if request.method == "POST":
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

    else:
        return render(request, "final_project/register.html")
