from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from dotenv import load_dotenv
from rest_framework.decorators import api_view

from .models import Note, Tag, User

load_dotenv()


# Create your views here.
@api_view(["GET"])
def index(request):
    all_notes = []

    if request.user.is_authenticated:
        # Get user's notes
        notes = Note.objects.filter(
            author=request.user, is_archived=False, is_deleted=False
        ).all()

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
        return render(request, "final_project/index.html", {"notes": all_notes})
    else:
        return redirect(reverse("login"))


@api_view(["GET"])
def archives(request):
    all_notes = []

    if request.user.is_authenticated:
        # Get user's notes
        notes = Note.objects.filter(author=request.user, is_archived=True).all()

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
        return render(request, "final_project/archives.html", {"notes": all_notes})
    else:
        return redirect(reverse("login"))


@api_view(["GET"])
def deleted(request):
    all_notes = []

    if request.user.is_authenticated:
        # Get user's notes
        notes = Note.objects.filter(author=request.user, is_deleted=True).all()

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
        return render(request, "final_project/deleted.html", {"notes": all_notes})
    else:
        return redirect(reverse("login"))


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


@api_view(["POST"])
def save_note(request, note_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.data.get("title")
            tag_input = request.data.get("tags")
            content = request.data.get("content")

            print(title)

            tags = []

            for word in tag_input.split(","):
                tags.append(word.strip())

            print(tags)
            # Delete tags asscociated with that note
            Tag.objects.filter(note_id=note_id).all().delete()
            n = Note.objects.filter(id=note_id)

            for tag in tags:
                t = Tag(note_id=n.last(), tag_name=tag)
                t.save()

            n.update(content=content, title=title)
            return redirect(reverse("index"))
        else:
            return redirect(reverse("login"))
    else:
        return redirect(reverse("login"))


@api_view(["POST", "GET"])
def forgot_password_view(request):
    if request.method == "POST":
        ...
    else:
        return render(request, "final_project/forgot_password.html")


def forgot_password_page(request):
    return render(request, "forgot_password.html")


@api_view(["POST", "GET"])
def login_view(request):
    if request.method == "POST":
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


@api_view(["GET"])
def archive_note(_, note_id):
    if note_id:
        Note.objects.filter(id=note_id).update(is_archived=True)

    return JsonResponse({"ok": True})


@api_view(["GET"])
def unarchive_note(_, note_id):
    if note_id:
        Note.objects.filter(id=note_id).update(is_archived=False)

    return JsonResponse({"ok": True})


@api_view(["GET"])
def delete_note(_, note_id):
    if note_id:
        Note.objects.filter(id=note_id).update(is_deleted=True)

    return JsonResponse({"ok": True})


@api_view(["GET"])
def restore_note(_, note_id):
    if note_id:
        Note.objects.filter(id=note_id).update(is_deleted=False)

    return JsonResponse({"ok": True})


@api_view(["GET"])
def select_note(_, note_id):
    note = Note.objects.get(id=note_id)
    note_tags = Tag.objects.filter(note_id__id=note_id)

    tags = set()
    for tag in note_tags:
        tags.add(tag.tag_name)

    tags = list(tags)
    note_details = {
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at,
        "updated_at": note.updated_at,
        "tags": tags,
    }

    return JsonResponse({"note_details": note_details})


@api_view(["POST", "GET"])
def register(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            username = request.POST["username"]
            email = request.POST["email"]

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirm_password"]
            if password != confirmation:
                return render(
                    request,
                    "final_project/register.html",
                    {"message": "Passwords does not match."},
                )
            else:
                try:
                    user = User.objects.create_user(username, email, password)
                    user.save()
                except IntegrityError as e:
                    print(e)
                    return render(
                        request,
                        "final_project/register.html",
                        {"message": "Username/email already taken."},
                    )
                else:
                    login(
                        request,
                        user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )
                return redirect(reverse("index"))
        else:
            print("Hssol")
            return redirect(reverse("index"))
    else:
        return render(request, "final_project/register.html")
