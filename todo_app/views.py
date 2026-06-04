import os
import json
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

file_path = os.path.join(settings.BASE_DIR, "notes.json")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/notes/")
        else:
            return render(request, "auth/login.html", {"error": "Invalid credentials"})

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")


@login_required
def notes_view(request):
    if os.path.exists(file_path):
        with open(file_path, "r") as jsonfile:
            all_notes = json.load(jsonfile)
        notes = [n for n in all_notes if n.get("user_id") == request.user.id]
    else:
        notes = []
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_id = max([n["id"] for n in all_notes], default=0) + 1
        note = {
            "id": new_id,
            "user_id": request.user.id,   # 🔥 ADD THIS
            "title": title,
            "content": content,
            "timestamp": timestamp
        }
        notes.append(note)
        with open(file_path, "w") as notefile:
            json.dump(notes, notefile)
    return render(request, "note/notes.html", {'notes': notes})


@login_required
def delete_note(request, id):
    with open(file_path, "r") as f:
        notes = json.load(f)
    good_note = [
        note for note in notes
        if not (note["id"] == id and note.get("user_id") == request.user.id)
    ]
    with open(file_path, "w") as noteFile:
        json.dump(good_note, noteFile)
    return redirect("/notes/")


@login_required
def edit_note(request, id):
    with open(file_path, "r") as f:
        notes = json.load(f)
    note_to_edit = None
    for note in notes:
        if note["id"] == id and note.get("user_id") == request.user.id:
            note_to_edit = note
    if request.method == "GET":
        return render(request, "note/edit_note.html", {'note': note_to_edit})
    elif request.method == "POST":
        new_title = request.POST.get("title").strip()
        new_content = request.POST.get("content").strip()
        for note in notes:
            if note["id"] == id and note.get("user_id") == request.user.id:
                note["title"] = new_title
                note["content"] = new_content
        with open(file_path, "w") as noteFile:
            json.dump(notes, noteFile)
        return redirect("/notes/")

