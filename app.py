from flask import Flask, render_template, request, redirect, url_for
from crew import SceneCrew
from stable_connector import txt2image_request

app = Flask(__name__)

sceneCrew = SceneCrew()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    scene = request.form['scene']
    result = sceneCrew.generateScene(scene)

    print(result)

    sceneCrew.saveResult(scene, result)

    res = txt2image_request(result)

    print(res)

    temp = render_template('response_template.html', content=result)

    return temp


if __name__ == "__main__":
    app.run(debug=True)
