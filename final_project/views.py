import random
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from dotenv import load_dotenv
from rest_framework.decorators import api_view

from mail.models import Email

from .models import Code, Note, Tag, User

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

            n.update(content=content, title=title, updated_at=timezone.now())
            return redirect(reverse("index"))
        else:
            return redirect(reverse("login"))
    else:
        return redirect(reverse("login"))


def generate_code(user):
    num = list("1234567890")

    code = ""
    for _ in range(0, 6):
        code += random.choice(num)

    if code:
        # Check if user has already requested a code
        generated_code = Code.objects.filter(user=user)

        if len(generated_code) > 0:
            generated_code.update(code=code, updated_at=timezone.now())
        else:
            c = Code(user=user, code=code)
            c.save()

        email = Email(
            user=user,
            subject="Your Recovery Code",
            body=code,
            sender=User.objects.get(email="notebook@gmail.com"),
        )
        email.save()
        email.recipients.add(user)

        return code
    else:
        return None


@api_view(["POST"])
def request_code(request):
    email = request.data.get("email")
    user = User.objects.get(email=email)

    if generate_code(user):
        return JsonResponse({"message": "Code successfully sent. Check you mailbox"})
    else:
        return JsonResponse({"message": "Could not generate code"})


@api_view(["POST", "GET"])
def forgot_password_view(request):
    if request.method == "POST":
        email = request.data.get("email")
        verification_code = request.data.get("code")

        if verification_code:
            stored_verification_code = Code.objects.get(user=request.user)
            verification_code = int(verification_code.strip())

            # Check if code is past 15 mins
            is_expired = (
                timezone.now() - stored_verification_code.updated_at
                > timedelta(minutes=15)
            )
            if is_expired:
                return render(
                    request,
                    "final_project/forgot_password.html",
                    {
                        "message": "Code expired",
                        "email": email,
                        "code_sent": True,
                        "expired": True,
                    },
                )

            if stored_verification_code.code == verification_code:
                return redirect(reverse("set_new_password"))
            else:
                return render(
                    request,
                    "final_project/forgot_password.html",
                    {
                        "message": "Invalid code. Please try again",
                        "code": verification_code,
                        "code_sent": True,
                        "invalid": True,
                    },
                )
        else:
            try:
                user_found = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(
                    request,
                    "final_project/forgot_password.html",
                    {"message": "Email not found", "email": email},
                )
            else:
                if user_found:
                    if generate_code(user_found):
                        return render(
                            request,
                            "final_project/forgot_password.html",
                            {"message": "Check your mail for code", "code_sent": True},
                        )
                    else:
                        return render(
                            request,
                            "final_project/forgot_password.html",
                            {"message": "Could not generate code", "email": email},
                        )
    else:
        return render(request, "final_project/forgot_password.html")


@api_view(["POST", "GET"])
def set_new_password(request):
    if request.method == "GET":
        return render(request, "final_project/set_new_password.html")
    else:
        password = request.data.get("password")
        confirmation = request.data.get("confirmation")

        if password != confirmation:
            return render(
                request,
                "final_project/set_new_password.html",
                {"error": "Password does not match"},
            )
        else:
            try:
                user = User.objects.get(username=request.user.username)
            except User.DoesNotExist:
                return render(
                    request,
                    "final_project/set_new_password.html",
                    {"error": "Invalid user"},
                )
            else:
                user.password = password

                return redirect(reverse("index"))


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
        Note.objects.filter(id=note_id).update(
            is_archived=True, updated_at=timezone.now()
        )

    return JsonResponse({"ok": True})


@api_view(["GET"])
def unarchive_note(_, note_id):
    if note_id:
        Note.objects.filter(id=note_id).update(
            is_archived=False, updated_at=timezone.now()
        )

    return JsonResponse({"ok": True})


@api_view(["GET"])
def delete_note(_, note_id):
    if note_id:
        Note.objects.filter(id=note_id).update(
            is_deleted=True, updated_at=timezone.now()
        )

    return JsonResponse({"ok": True})


@api_view(["GET"])
def restore_note(_, note_id):
    if note_id:
        Note.objects.filter(id=note_id).update(
            is_deleted=False, updated_at=timezone.now()
        )

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
