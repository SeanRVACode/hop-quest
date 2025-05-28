from flask import Blueprint, render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
from icecream import ic
from app.services import Brew_Service, Data_Cleaner

# Can also pull in logic from a service layer
# ex from app.services.greet_service import get_greeting

main_bp = Blueprint("main", __name__)

bs = Brew_Service()
dc = Data_Cleaner()


@main_bp.route("/", methods=["GET", "POST"])
def home():
    ic("On Home page")
    if request.method == "POST":
        data = bs.search_by_params(request=request)
        if data:
            headers_list = dc.proper_names(data)
            try:
                return render_template("main/results.html", data=data, headers=headers_list)
            except TemplateNotFound:
                return render_template("404.html")
    try:
        return render_template("main/hop-quest-home.html")
    except TemplateNotFound:
        return render_template("404.html")


@main_bp.route("/random")
def random_breweries():
    data = bs.random_breweries()
    headers_list = dc.proper_names(data)
    ic(headers_list)
    try:
        return render_template("main/results.html", data=data, headers=headers_list)
    except TemplateNotFound:
        return render_template("404.html")
