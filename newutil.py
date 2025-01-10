import os
import pickle

import tkinter as tk
from tkinter import messagebox
import face_recognition


def get_button(parent, text, bg_color, command, **kwargs):
    button = tk.Button(parent, text=text, command=command, bg=bg_color, **kwargs)
    return button


def get_img_label(parent, **kwargs):
    label = tk.Label(parent, **kwargs)
    label.imgtk = None
    return label


def get_text_label(parent, text, **kwargs):
    label = tk.Label(parent, text=text, **kwargs)
    return label

def get_entry_text(parent, **kwargs):
    entry = tk.Text(parent, **kwargs)
    return entry


def msg_box(title, description):
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'