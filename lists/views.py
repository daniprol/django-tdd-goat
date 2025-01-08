from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_page(request: HttpRequest):
    context = {}
    # if request.method == "POST":
    #     context["new_item_text"] = request.POST["item_text"]
    # NOTE: request.POST is a dictionary??
    # return HttpResponse("You submitted: " + request.POST["item_text"])
    return render(request, "home.html", context={"new_item_text": request.POST.get("item_text", "")})
