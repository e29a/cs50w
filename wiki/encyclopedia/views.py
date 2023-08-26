from django.shortcuts import render, redirect
from markdown2 import Markdown
from django.http import Http404
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    if title not in util.list_entries():
        raise Http404
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "content": Markdown().convert(content)
        })

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    results = [
        i
        for i in entries
        if query.lower() in i.lower()
    ]

    if query is None or query == "":
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": results
        })
    elif len(results) > 1:
        return render(request, "encyclopedia/search.html", {
            "results": results, 
            "query": query
            })
    else:
        return redirect("wiki", results[0])

