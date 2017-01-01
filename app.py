from flask import Flask
import mlab
from mongoengine import *
from flask_restful import Api, Resource, reqparse
import json

mlab.connect()

class Note(Document):
    title = StringField()
    content = StringField()
    name = StringField()

#n = Note(title="A first note", content="Crazy day")
#n.save()

#for note in Note.objects:
#    print(note.to_json())

app = Flask(__name__)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, location="json")
parser.add_argument("content", type=str, location="json")
parser.add_argument("name", type=str, location="json")

@app.route('/')
def hello_world():
    return 'Hello World!'

class NoteListRes(Resource):
    def get(self): #get all notes
        return mlab.list2json(Note.objects)
    def post(self): #post new note
        args = parser.parse_args()
        title = args["title"]
        content = args["content"]
        name = args["name"]
        new_note = Note(title=title, content=content, name=name)
        new_note.save()
        return mlab.item2json(new_note)  #return {"status": "ok"}

class NoteRes(Resource):

    def get(self, note_id):
        all_notes = Note.objects
        found_note = all_notes.with_id(note_id)
        return mlab.item2json(found_note)

    def delete(self, note_id):
        all_notes = Note.objects
        found_note = all_notes.with_id(note_id)
        found_note.delete()
        return {"code": 1, "status": "OK"}, 200

    def put(self, note_id):
        args = parser.parse_args()
        title = args["title"]
        content = args["content"]
        name = args["name"]
        all_notes = Note.objects
        found_note = all_notes.with_id(note_id)
        found_note.update(set__title=title, set__content=content, set__name=name)
        return {"code": 1, "status":"OK"}, 200

api.add_resource(NoteListRes, "/api/note")
api.add_resource(NoteRes, "/api/note/<note_id>")

if __name__ == '__main__':
    app.run()
