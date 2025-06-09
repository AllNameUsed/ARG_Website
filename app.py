from flask import Flask, request, redirect, render_template, make_response

app = Flask(__name__)

@app.before_request
def muggle_firewall():
    path = request.path
    muggle_status = request.cookies.get("muggle")

    # Avoid interference with core pages
    if path.startswith(("/static", "/reset", "/favicon.ico")):
        return

    # Banned muggles: trap them
    if muggle_status == "banned" and path != "/lol" and path != "/reset":
        return redirect("/lol")

    # First-time muggles: only allow homepage and muggle view
    if muggle_status == "true":
        if path not in ["/", "/muggle"]:
            return redirect("/muggle")
    

    # Authenticated users go straight to /authenticated when hitting "/"
    if muggle_status == "authenticated" and path not in ["/reset", "/authenticated"] :
        return redirect("/authenticated")

    

@app.route("/", methods=["GET", "POST"])
def home():
    muggle_status = request.cookies.get("muggle")

    if request.method == "POST":
        choice = request.form.get("choice")

        if choice == "yes":
            resp = make_response(redirect("/muggle"))
            resp.set_cookie("muggle", "true", max_age=60*60*24*365)
            return resp

        elif choice == "no":
            if muggle_status == "true":
                # Muggle tries to lie — ban them
                resp = make_response(redirect("/lol"))
                resp.set_cookie("muggle", "banned", max_age=60*60*24*365)
                return resp
            else:
                # First-time honest user — label as auth
                resp = make_response(render_template("authenticate.html"))
                resp.set_cookie("muggle", "auth", max_age=60*60*24*365)
                return resp
            
    elif request.method == "GET":
        if muggle_status == "auth":
            return render_template("authenticate.html")


    # GET request just shows the question page
    return render_template("index.html")

@app.route("/muggle")
def muggle():
    return render_template("muggle.html")

@app.route("/lol")
def troll():
    return render_template("troll.html")

@app.route("/reset")
def reset_cookie():
    resp = make_response(redirect("/"))
    resp.set_cookie("muggle", "", expires=0)
    return resp

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/cases")
def investigations():
    return render_template("cases.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/PSA")
def lost_found():
    return render_template("psa.html")

@app.route("/scamwatch")
def scamwatch():
    return render_template("scamwatch.html")

@app.route("/authenticated")
def endgame():
    return render_template("authenticated.html")

@app.route("/appeal")
def appeal():
    return render_template("appeal.html")

if __name__ == "__main__":
    app.run(debug=True)
