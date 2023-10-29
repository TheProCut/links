import os
import requests
from flask import Flask, redirect, request, session, render_template_string

print("ZER, READ THE 'READ ME' FILE!")

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = "https://links.theprocut.co.uk/callback"
DISCORD_API_URL = "https://discord.com/api"

user_ranks = {
    "theprocut": "Support Team +",
    "zertybee": "Junior Support",
    "superevilluke": "Support Team +",
    "omminerofficial": "Support Team +",
    "jqmeswxnder": "Support Team +",
    "pilot_773": "Junior Support",
    "crocscore": "Junior Support",
    "zaac0808": "Support Team +",
}

links = {
    "Support Team +": [
        {
            "label": "Support Warning Database",
            "url": os.environ['SupportWarningSystem'],
            "image_url": "https://as2.ftcdn.net/v2/jpg/03/84/49/65/1000_F_384496509_MvBSkODOe3h4XOKYndJ0A3Ph68wsGS6T.jpg"
        },
        {
            "label": "Free Products PDF",
            "url": "https://drive.google.com/file/d/1161vL5LOHYnwLfluWcaw7B7m-EIAasUm/view?usp=sharing",
            "image_url": "https://lh3.googleusercontent.com/u/1/drive-viewer/AK7aPaC4SCPF3HjQSbmsrMtEA8PFWL9bSX4xvISrGlxO8vrLBNNhlXnIACKTVF5d5S9mrzlIgjWjWqpoOaGTdU-LjV6j2LaY=w1920-h911"
        },
        {
            "label": "Tickets bot",
            "url": "https://dashboard.ticketsbot.net/manage/856122881086849049/transcripts",
            "image_url": "https://ticketsbot.net/assets/img/logo-trans.webp"
        },
        {
            "label": "Link 4",
            "url": "/supportteam/link4",
            "image_url": "https://example.com/image4.png"
        },
        {
            "label": "Link 5",
            "url": "/supportteam/link5",
            "image_url": "https://example.com/image5.png"
        },
    ],
    "Junior Support": [
        {
            "label": "Log a warning",
            "url": os.environ['warninglog'],
            "image_url": "https://as2.ftcdn.net/v2/jpg/03/84/49/65/1000_F_384496509_MvBSkODOe3h4XOKYndJ0A3Ph68wsGS6T.jpg"
        },
        {
            "label": "Free Products PDF",
            "url": "https://drive.google.com/file/d/1161vL5LOHYnwLfluWcaw7B7m-EIAasUm/view?usp=sharing",
            "image_url": "https://lh3.googleusercontent.com/u/1/drive-viewer/AK7aPaC4SCPF3HjQSbmsrMtEA8PFWL9bSX4xvISrGlxO8vrLBNNhlXnIACKTVF5d5S9mrzlIgjWjWqpoOaGTdU-LjV6j2LaY=w1920-h911"
        },
        {
            "label": "Tickets bot",
            "url": "https://dashboard.ticketsbot.net/",
            "image_url": "https://ticketsbot.net/assets/img/logo-trans.webp"
        },
        {
            "label": "Link 4",
            "url": "/juniorsupport/link4",
            "image_url": "https://example.com/image9.png"
        },
        {
            "label": "Link 5",
            "url": "/juniorsupport/link5",
            "image_url": "https://example.com/image10.png"
        },
    ],
}

@app.route("/")
def home():
    if "discord_token" in session:
        discord_user = get_discord_user()
        username = discord_user["username"]
        rank = user_ranks.get(username, None)

        if rank:
            user_links = links.get(rank, [])

            links_html = "".join([
                f'''
                <div class="link">
                    <img src="{link["image_url"]}" alt="{link["label"]}">
                    <a href="{link["url"]}">{link["label"]}</a>
                </div>
                '''
                for link in user_links
            ])

            return render_template_string("""
            <html>
            <head>
                <title>Links Page</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    h1 {
                        text-align: center;
                    }
                    .link {
                        display: flex;
                        align-items: center;
                        margin: 10px 0;
                        padding: 10px;
                        background-color: #fff;
                        border-radius: 5px;
                        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
                    }
                    .link img {
                        width: 50px;
                        height: 50px;
                        margin-right: 10px;
                    }
                    .link a {
                        text-decoration: none;
                        color: #007BFF;
                    }
                    .link:hover {
                        background-color: #f0f0f0;
                    }
                    .logout {
                        text-align: center;
                        margin-top: 20px;
                    }
                    .logout a {
                        text-decoration: none;
                        padding: 10px 20px;
                        background-color: #dc3545;
                        color: #fff;
                        border-radius: 5px;
                    }
                    .signin-button {
                        display: block;
                        width: 200px;
                        margin: 0 auto;
                        padding: 10px;
                        background-color: #7289DA;
                        color: #fff;
                        text-align: center;
                        border-radius: 5px;
                        text-decoration: none;
                    }
                    .signin-button:hover {
                        background-color: #5465A7;
                    }
                    .help-button {
                        display: block;
                        width: 200px;
                        margin: 0 auto;
                        padding: 10px;
                        background-color: #28a745;
                        color: #fff;
                        text-align: center;
                        border-radius: 5px;
                        text-decoration: none;
                    }
                    .help-button:hover {
                        background-color: #1e7e34;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Welcome, {{ username }} ({{ rank }})!</h1>
                    <div class="links">
                        {{ links_html | safe }}
                    </div>
                    <div class="logout">
                        <a href='/logout'>Logout</a>
                    </div>
                    <div class="help-button">
                        <a href="/help">Help/Report Bug</a>
                    </div>
                </div>
            </body>
            </html>
            """, username=username, rank=rank, links_html=links_html)
        else:
            return "Sorry, you don't have access to any links."
    else:
        return '<a class="signin-button" href="/login">Sign in with Discord</a>'

@app.route("/login")
def login():
    return redirect(f"{DISCORD_API_URL}/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify")

@app.route("/logout")
def logout():
    session.pop("discord_token", None)
    return redirect("/")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(f"{DISCORD_API_URL}/oauth2/token", data=data, headers=headers)
    token_data = response.json()
    session["discord_token"] = token_data["access_token"]
    return redirect("/")

@app.route("/help", methods=["GET", "POST"])
def help():
    if request.method == "POST":
        user_input = request.form["user_input"]
        send_discord_webhook(user_input)
    return render_help_form()

def render_help_form():
    return render_template_string("""
    <html>
    <head>
        <title>Help/Report Bug</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                text-align: center;
            }
            .form-container {
                background-color: #fff;
                border-radius: 5px;
                padding: 20px;
                box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
            }
            .form-label {
                display: block;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .form-input {
                width: 100%;
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            .form-button {
                display: block;
                width: 100%;
                padding: 10px;
                background-color: #007BFF;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .form-button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Help/Report Bug</h1>
            <div class="form-container">
                <form method="post">
                    <label class="form-label" for="user_input">Please enter your message:</label>
                    <textarea class="form-input" id="user_input" name="user_input" rows="6" required></textarea>
                    <button class="form-button" type="submit">Submit</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """)

def send_discord_webhook(message):
    webhook_url = os.environ['webhook']

    data = {
        "content": message
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, json=data, headers=headers)

    if response.status_code == 204:
        print("Message sent to Discord successfully")
    else:
        print(f"Failed to send message to Discord, status code: {response.status_code}")

def get_discord_user():
    headers = {
        "Authorization": f"Bearer {session['discord_token']}"
    }

    response = requests.get(f"{DISCORD_API_URL}/users/@me", headers=headers)
    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
