from flask import Flask

app = Flask(__name__)

@app.route("/")

def main():
    print("Hello from my_flask_app !")


if __name__ == "__main__":
    app.run(debug=True)
