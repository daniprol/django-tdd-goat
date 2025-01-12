from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import Item


def home_page(request: HttpRequest):
    if request.method == "POST":
        # This needs an explicit save!
        # item = Item(text=request.POST.get("item_text", ""))

        # item.text = request.POST.get("item_text", "")
        # item.save()
        Item.objects.create(text=request.POST.get("item_text", ""))
        return redirect("/lists/the-only-list-in-the-world/")

    # context = {}
    # if request.method == "POST":
    #     context["new_item_text"] = request.POST["item_text"]
    # NOTE: request.POST is a dictionary??
    # return HttpResponse("You submitted: " + request.POST["item_text"])
    return render(request, "home.html")


def view_list(request: HttpRequest):
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})
