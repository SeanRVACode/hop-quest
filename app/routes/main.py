from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
from icecream import ic

# Can also pull in logic from a service layer
# ex from app.services.greet_service import get_greeting

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    ic("On Home page")
    try:
        return render_template("main/hop-quest-home.html")
    except TemplateNotFound:
        return render_template("404.html")


@main_bp.route("/search", methods=["GET", "POST"])
def search():
    return render_template("main/results.html")
