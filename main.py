from fastapi import FastAPI
import json
import os
from pydantic import BaseModel


class Note(BaseModel):
    title: str
    content: str


app = FastAPI()

DATA_FILE = "notes.json"

def load_notes():
    if not os.path.exists(DATA_FILE):
        return []
    with open (DATA_FILE, 'r') as f:
        return json.load(f)
    

def save_notes(notes):
    with open(DATA_FILE, 'w') as f:
        json.dump(notes, f, indent=4)

@app.get("/")
def home():
    return {"message": "Welcome to the Notes API"}

@app.get("/notes")
def get_notes():
    notes = load_notes()
    return notes


@app.post("/notes", summary="Create a new note")
def create_note(note: Note):
    notes = load_notes()

    new_note = {
        "id": len(notes) + 1,
        "title": note.title,
        "content": note.content
    }

    notes.append(new_note)
    save_notes(notes)
    return new_note

@app.put("/notes/{note_id}", summary="Update an existing note")
def update_note(note_id: int, updated_note: Note):
    notes = load_notes()

    for note in notes:
        if note["id"] == note_id:
            note["title"] = updated_note.title
            note["content"] = updated_note.content
            save_notes(notes)
            return note
    return {"Error": "Note not found"}



@app.delete("/notes/{note_id}", summary="Delete a note by ID")
def delete_note(note_id: int):
    notes = load_notes()
    updated_notes = [note for note in notes if note["id"] != note_id]

    if len(updated_notes) == len(notes):
        return {"error":"Note not found"}
    
    save_notes(updated_notes)
    return {"message": f"Note {note_id} deleted."}
