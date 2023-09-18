from flask import Flask, request
from resourses import EntryManager, Entry

FOLDER = r'C:\Users\Aleksandr\PycharmProjects\todo-list-backend'

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/entries/')
def get_entries():
    start = EntryManager(FOLDER)
    start.load()
    return [entry.to_dict_for_json() for entry in start.entries]

@app.route('/api/save_entries/', methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    for entry in request.get_json():
        entry = Entry.from_json(entry)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {'status': 'success'}

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)