from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from random import choice
from markdown2 import Markdown
from . import util

markdowner = Markdown()

class SearchForm(forms.Form):
    entry = forms.CharField(max_length=20, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Search entry'}))

class AddWikiForm(forms.Form):
    title = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'Title'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textArea', 'placeholder': 'Wiki entry...'}))

class EditWikiForm(forms.Form):
    title = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'readonly':'readonly'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textArea'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchForm": SearchForm()
    })


def search(request, title):
    return render(request, "encyclopedia/wiki.html", {
        "entry": markdowner.convert((util.get_entry(title))),
        "title": title
    })


def searchByIndex(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data['entry']
            isAdded = util.get_entry(entry)
            if isAdded is not None:
                return HttpResponseRedirect(reverse('search', kwargs={'title': entry}))
            else:
                entries = util.list_entries()
                entriesFound = []
                for wikiEntry in entries:
                    if entry in wikiEntry:
                        entriesFound.append(wikiEntry)
                return render(request, "encyclopedia/customsearch.html", {
                    "entries": entriesFound
                })
    return render(request, "encyclopedia/wiki.html")


def addWiki(request):
    if request.method == "POST":
        form = AddWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            isAdded = util.get_entry(title)
            if isAdded is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('search', kwargs={'title': title}))
            else:
                messages.error(request, 'Entry already exist')
        else:
            return render(request, "encyclopedia/addwiki.html", {
                "AddWikiForm": AddWikiForm(),
            })
    return render(request, "encyclopedia/addwiki.html", {
        "AddWikiForm": AddWikiForm(),
    })

def editWiki(request, title):
    entry = util.get_entry(title)
    form = EditWikiForm(initial={'title': title, 'content': entry})
    if request.method == "POST":
        newEditForm = EditWikiForm(request.POST)
        if newEditForm.is_valid():
            newContent = newEditForm.cleaned_data['content']
            util.save_entry(title, newContent)
            return HttpResponseRedirect(reverse('search', kwargs={'title': title}))
    return render(request, "encyclopedia/editwiki.html", {
        'title': title,
        "NewEditWikiForm": form,
    })

def random(self):
    entries = util.list_entries()
    randomTitle = choice(entries)
    return HttpResponseRedirect(reverse('search', kwargs={'title': randomTitle}))
