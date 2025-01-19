from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import Item, List


def home_page(request: HttpRequest):
    # context = {}
    # if request.method == "POST":
    #     context["new_item_text"] = request.POST["item_text"]
    # NOTE: request.POST is a dictionary??
    # return HttpResponse("You submitted: " + request.POST["item_text"])
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: int):
    our_list = List.objects.get(id=list_id)
    # items = Item.objects.filter(list=our_list)
    # return render(request, "list.html", {"items": items})
    return render(request, "list.html", {"list": our_list})


def new_list(request: HttpRequest):
    # FIXME: only POST requests are supported for now
    nulist = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=nulist)
    return redirect(f"/lists/{nulist.id}/")


def add_item(request: HttpRequest, list_id: int):
    our_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=our_list)
    return redirect(f"/lists/{our_list.id}/")
