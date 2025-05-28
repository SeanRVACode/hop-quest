from flask import Flask, render_template, redirect, request, flash
from flask_bootstrap import Bootstrap5
import os
import re
from urllib.parse import urlencode
from werkzeug.exceptions import HTTPException
import json
import requests
import sys

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
Bootstrap5(app)

# Default URL for Openbrewerydb
DEFAULT_URL = "https://api.openbrewerydb.org/v1/breweries"


@app.route("/")
def home():
    thumb_path = ".static/assets/img/portfolio/thumbnails/"
    full_path = ".static/assets/img/portfolio/fullsize/"
    return render_template("index.html", thumb_path=thumb_path, full_path=full_path)


# Handles the redirect for thumbnail images so I don't have to type url_for a ton
@app.route("/assets/img/portfolio/thumbnails/<img>")
def thumbnails(img):
    return redirect(f"/static/assets/portfolio/thumbnails/{img}")


@app.route("/assets/img/portfolio/fullsize/<img>")
def fullsize(img):
    return redirect("/static/assets/portfolio/fullsize/img")


@app.route("/returnchecker")
def taxReturnChecker():
    return render_template("taxReturnchecker.html", status="In Progress")


@app.route("/getstatus", methods=["GET", "POST"])
def getStatus():
    # status_messages = ['Training Room Is Down. Delays expected.',
    # 'In the Dumpster on Fire','Sent to the wrong Client.',
    # 'Still waiting for you to sign that Engagement Letter.',
    # 'Lost in the Bermuda Triangle of Paperwork.',
    # "Currently on a lunch date with Murphy's law.",
    # 'Stuck in the "Quick Question" rabbit hole.']
    # if request.method == 'POST':

    #     status = random.choice(status_messages)
    #     return render_template('taxReturnchecker.html',status=status)
    return render_template("taxReturnchecker.html", status="In Progress")


@app.route("/verification", methods=["GET", "POST"])
def login():
    return render_template("verification.html")


@app.route("/logout")
def logout():
    return render_template("login.html")


@app.route("/brewery_lookup")
def lookup():
    data = get_random_breweries()
    headers_list = proper_names(data)
    return render_template("brewery_lookup.html", data=data, headers=headers_list)


@app.route("/search_brew", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        json_data = get_brewery_list(request)

        if json_data == "No Search":
            flash("Please enter at least one search criterion")
            return render_template("search.html")
        elif not json_data or len(json_data) == 0:
            flash("No breweries found matching your search criteria")
            return render_template("search.html")
        else:
            headers_list = proper_names(json_data)
            return render_template("search-a-brew.html", data=json_data, headers=headers_list)
    else:
        # Default case for GET request
        return render_template("search.html")


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # Start with the correct headers and status code from the error
    response = e.get_response()
    # Replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html")


def get_brewery_list(request=None) -> dict:
    """Query the API based on parameters provided by user and return Json data as results. Also handles creating the map URL link."""
    params = {}
    # TODO look into handling this better for no search results? Maybe having it just bring stuff up is fine?
    if request:
        # Handle form data if request is provided
        if request.method == "POST":
            # This dictionary maps the form field names (e.g., `brewName`) to the query parameter names expected by the API (e.g., `by_name`)
            form_fields = {
                "brewName": "by_name",
                "cityName": "by_city",
                "stateName": "by_state",
            }

            # Build params dictionary including only non-empty form fields
            params = {
                param_name: request.form.get(form_field)
                for form_field, param_name in form_fields.items()
                if request.form.get(form_field)
            }
            # Old way of doing search
            # b_name = request.form.get("brewName")
            # b_city = request.form.get("cityName")
            # b_state = request.form.get("stateName")
            # if b_name:
            #     params["by_name"] = b_name
            # if b_city:
            #     params["by_city"] = b_city
            # if b_state:
            #     params["by_state"] = b_state

    if params:
        # Make the API request
        query_string = urlencode(params)
        url = f"{DEFAULT_URL}?{query_string}"
        r = requests.get(url)
        json_data = r.json()
        json_data = create_map_link(json_data)
        if json_data:
            return json_data
        else:
            return None
    else:
        return "No Search"


def get_random_breweries():
    url = "https://api.openbrewerydb.org/v1/breweries/random?size=10"

    r = requests.get(url)
    # print(r.content)
    json_data = r.json()
    # Creates the map link that will be utilized in the HTML code to create a clickable google maps link for users.
    json_data = create_map_link(json_data)

    return json_data


def create_map_link(json_data):
    modified_data = json_data.copy()
    for brewery in modified_data:
        street = brewery["address_1"]
        city = brewery["city"]
        state = brewery["state"]
        postal_code = brewery["postal_code"]
        address = f"{street} {city} {state}, {postal_code}"

        brewery["address"] = address.replace(" ", "+")
    return modified_data


def proper_names(json_data):
    json_data = json_data[0]
    # Create a new dictionary with modified keys
    new_json_data = {}
    for key, value in json_data.items():
        key_new = re.sub(r"[_]+", " ", key).strip().title()
        new_json_data[key_new] = value

    return new_json_data
