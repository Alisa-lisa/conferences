# TODO: make prelearned models for 1k, 5k, 10k, 25k, 50k items for 2,3,5 labels for NB, RandomForest, SVM with nltk
# TODO: validation
# TODO: logging
# TODO: deploy with uWSGI


from flask import Flask, request, jsonify, render_template, session
import json
import ast
app = Flask(__name__)
app.secret_key = "p3we3a"

short_description = {}
models = []

@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route("/collect-text", methods=['POST', 'GET'])
def collect_files():
    if request.method == 'POST':
        with open('tmp/tmp_storage.txt', 'a') as storage:
            req = request.get_json()
            text = req['text']
            label = req['label']
            storage.write(json.dumps({label:text}))
            storage.write('\n')
            return jsonify({"INFO":"Storing files"})
    elif request.method == 'GET':
        counter = 0
        labels = []
        try:
            with open('tmp/tmp_storage.txt', 'r') as stored:
                for line in stored:
                    if '\n' == line[-1]:
                        counter +=1
                        label = list(ast.literal_eval(line).keys())[0]
                        if label not in labels:
                            labels.append(label)
                return jsonify({"Number texts stored":counter, "Labels stored":labels})
        except Exception as ex:
            return jsonify({"ERROR":"couldn't read file due to {}".format(ex)})
    else:
        return jsonify({"Method error":"Attempt to use not allowed method"})


@app.route("/set", methods=['POST', 'GET'])
def set_model():
    if request.method == 'GET':
        try:
            return jsonify("Chosen model for the session is {}".format(session['model']))
        except Exception as ex:
            return jsonify("No model was set yet")
    elif request.method == 'POST':
        req = request.get_json()
        model = req['model']
        session['model'] = model
        app.logger.info(session)
        return jsonify({"INFO":"you have chosen {} for this learning session".format(model)})


# TODO: create learning and validation sets from populated file for special labels, train the model and pickle it
# expects split size, labels
@app.route("/learn", methods=['POST', 'GET'])
def learn_model():
    model = session.get('model')
    app.logger.info(model)
    if request.method == 'POST':
        req = request.get_json()
        split = req['split']
        labels = request['labels']
        if model == "NB":
            return jsonify("starting training")
    elif request.method == 'GET':
        app.logger.info(model)
        return jsonify("Chosen model is {}. Set, split and labels for the trainig".format(model))


# shows short description for a model
@app.route("/choose-model", methods=['GET', 'POST'])
def get_models_details():
    if request.method == 'POST':
        chosen_model = request.get_json()['model']
        return jsonify({"Short description for {}".format(chosen_model):short_description[chosen_model]})
    # TODO: make visual representation pretty
    elif request.method == 'GET':
        return render_template('models.html')


if __name__ == "__main__":
    app.run(debug=True, port=30100)
