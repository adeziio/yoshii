from flask import Flask
import yoshii


app = Flask(__name__)

yoshii.run()


@app.route('/')
def home():
    return "Server is Online..."


# Main
if __name__ == '__main__':
    app.run()
