from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django import forms
from random import randint
from markdown2 import Markdown

from . import util

class EntryForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Title", "class": "mb-4"}
        ),
    )
    content = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-4",
                "placeholder": "Content (markdown)",
                "id": "new_content",
            }
        ),
    )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": Markdown().convert(util.get_entry(title))
    })

def search(request):
    q = request.GET.get("q", "")
    result = util.get_entry(q)
    if result:
        return HttpResponseRedirect("/wiki/{}".format(q))
    else:
        results = []
        entries = util.list_entries()
        for entry in entries:
            if entry.find(q) == True:
                results.append(entry)
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "query": q
        })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html",{
            "form": EntryForm
        })
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                messages.add_message(
                    request,
                    messages.WARNING,
                    message = 'Entry already exists',
                )
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect("/wiki/{}".format(title))
        else:
            messages.add_message(
                request, messages.WARNING, message="Invalid request form"
            )
            return render(
                request,
                "encyclopedia/create.html",
                {"form": form},
            )

def edit(request, entry):
    if request.method == "GET":
        title = entry
        content = util.get_entry(title)
        form = EntryForm({"title": title, "content": content})
        return render(
            request,
            "encyclopedia/edit.html",
            {"form": form, "title": title},
        )

    form = EntryForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        content = form.cleaned_data.get("content")

        util.save_entry(title=title, content=content)
        return HttpResponseRedirect("/wiki/{}".format(title))

def random(request):
    entries = util.list_entries()
    entry = entries[randint(0, len(entries) - 1)]
    return HttpResponseRedirect("/wiki/{}".format(entry))