import os
import random
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from vonage import Auth, Vonage
# from vonage_sms import SmsMessage
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

            tags = []

            for word in tag_input.split(","):
                tags.append(word.strip())

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


VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")


def generate_code(user, phone):
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

        # todo: Uncomment to send sms
        # client = Vonage(Auth(api_key=VONAGE_API_KEY, api_secret=VONAGE_API_SECRET))
        # message = SmsMessage(
        #     to=phone,
        #     from_="Notebook",
        #     text=f"Your verification code is {code}. It will expire in 15 minutes. Do not share this code with anyone.",
        # )  # type: ignore

        # client.sms.send(message)
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
    phone = request.data.get("phone")

    if not phone or not email:
        return Response(
            {
                "message": "Please provide both email and phone number",
                "email": email,
                "status": 400,
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {
                "message": "AN unexpected error occurred.",
                "email": email,
                "phone": phone,
                "status": 500,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    else:
        if generate_code(user, phone):
            return Response(
                {
                    "message": "Code resent. Check your mail for code",
                    "email": email,
                    "status": 200,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": "Could not generate code",
                    "email": email,
                    "status": 400,
                },
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET", "POST"])
def enter_verification_code_view(request):
    if request.method == "GET":
        return render(
            request,
            "final_project/enter-code.html",
        )
    elif request.method == "POST":
        email = request.data.get("email")
        verification_code = request.data.get("code")

        if verification_code and email:
            user = User.objects.get(email=email)

            stored_verification_code = Code.objects.get(user=user)
            verification_code = int(verification_code.strip())

            # Check if code is past 15 mins
            is_expired = (
                timezone.now() - stored_verification_code.updated_at
                > timedelta(minutes=15)
            )
            if is_expired:
                return Response(
                    {
                        "message": "Verification code expired.",
                        "email": email,
                        "status": 410,
                    },
                    status=status.HTTP_410_GONE,
                )

            if stored_verification_code.code == verification_code:
                return Response(
                    {
                        "message": "Success",
                        "email": email,
                        "status": 200,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": "Invalid verification code.",
                        "email": email,
                        "status": 400,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


@api_view(["POST", "GET"])
def phone_number_view(request):
    if request.method == "GET":
        return render(request, "final_project/phone.html")

    email = request.data.get("email")
    phone = request.data.get("phone")

    if email:
        try:
            user_found = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "Email not found", "email": email, "status": 400},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            if generate_code(user_found, phone):
                return Response(
                    {
                        "message": "Check your mail for code",
                        "email": email,
                        "phone": phone,
                        "status": 200,
                    },
                    status=status.HTTP_200_OK,
                )
    else:
        return Response(
            {
                "message": "Please provide email",
                "email": email,
                "status": 400,
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST", "GET"])
def forgot_password_view(request):
    if request.method == "POST":
        email = request.data.get("email")

        if email:
            try:
                user_found = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"message": "Email not found", "email": email, "status": 400},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                if user_found:
                    return Response(
                        {
                            "message": "Check your mail for code",
                            "email": email,
                            "status": 200,
                        },
                        status=status.HTTP_200_OK,
                    )
        else:
            return Response(
                {
                    "message": "Please provide email",
                    "email": email,
                    "status": 400,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
    else:
        return render(request, "final_project/forgot_password.html")


@api_view(["POST", "GET"])
def set_new_password(request):
    if request.method == "GET":
        return render(request, "final_project/set_new_password.html")
    else:
        email = request.data.get("email")
        password = request.data.get("password")
        confirmation = request.data.get("confirmation")

        if password != confirmation:
            return Response(
                {
                    "message": "Passwords does not match",
                    "email": email,
                    "status": 400,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {
                        "message": "User not found",
                        "email": email,
                        "status": 404,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                user.set_password(password)
                user.save()

                return Response(
                    {
                        "message": "Check your mail for code",
                        "email": email,
                        "status": 200,
                    },
                    status=status.HTTP_200_OK,
                )


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
                except IntegrityError:
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
            return redirect(reverse("index"))
    else:
        return render(request, "final_project/register.html")
