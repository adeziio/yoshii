from flask import Flask
import yoshii
app = Flask(__name__)


@app.route('/')
def default():
    yoshii.run()
    return ""


# Main
if __name__ == '__main__':
    app.run()
