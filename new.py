import os.path
import datetime
import pickle

import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import face_recognition

import newutil


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1000x600+300+100")
        self.main_window.title("Facial Recognition Attendance System")

        self.control_frame = tk.Frame(self.main_window, bg="#f0f0f0")
        self.control_frame.place(x=700, y=0, width=300, height=600)

        self.camera_frame = tk.Frame(self.main_window, bg="#f0f0f0")
        self.camera_frame.place(x=0, y=0, width=700, height=600)

        self.webcam_label = newutil.get_img_label(self.camera_frame, bg="#f0f0f0")
        self.webcam_label.place(x=20, y=20, width=660, height=480)

        self.login_button = newutil.get_button(self.control_frame, 'Login', '#4CAF50', self.login, fg="white", font=('Arial', 12))
        self.login_button.place(x=20, y=150, width=250, height=60)

        self.logout_button = newutil.get_button(self.control_frame, 'Logout', '#F44336', self.logout, fg="white", font=('Arial', 12))
        self.logout_button.place(x=20, y=250, width=250, height=60)

        self.register_button = newutil.get_button(self.control_frame, 'Register New User', '#607D8B', self.register_new_user, fg='white', font=('Arial', 12))
        self.register_button.place(x=20, y=350, width=250, height=60)

        self.main_window.configure(bg="#f0f0f0")

        self.cap = None
        self.most_recent_capture_pil = None
        self.db_dir = './db'
        self.log_path = './log.txt'

        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

    def add_webcam(self, label):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        if ret:
            self.most_recent_capture_arr = frame
            img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)

            self._label.after(20, self.process_webcam)
        else:
            messagebox.showerror('Error', 'Failed to capture frame from webcam.')

    def login(self):
        name = newutil.recognize(self.most_recent_capture_arr, self.db_dir)

        if name in ['unknown_person', 'no_persons_found']:
            messagebox.showerror('Oops...', 'Unknown user. Please register new user or try again.')
        else:
            messagebox.showinfo('Welcome back!', 'Welcome, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                f.close()

    def logout(self):
        name = newutil.recognize(self.most_recent_capture_arr, self.db_dir)

        if name in ['unknown_person', 'no_persons_found']:
            messagebox.showerror('Oops...', 'Unknown user. Please register new user or try again.')
        else:
            messagebox.showinfo('Goodbye!', 'Goodbye, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{},out\n'.format(name, datetime.datetime.now()))
                f.close()

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("700x600+370+120")
        self.register_new_user_window.title("Register New User")

        self.capture_label = newutil.get_img_label(self.register_new_user_window, bg="#f0f0f0")
        self.capture_label.place(x=20, y=20, width=660, height=480)

        self.entry_register_new_user = tk.Entry(self.register_new_user_window, width=30, font=('Arial', 12))
        self.entry_register_new_user.place(x=50, y=530, width=200, height=40)

        self.text_label_register_new_user = newutil.get_text_label(self.register_new_user_window, 'Please input username:', font=('Arial', 12))
        self.text_label_register_new_user.place(x=50, y=500)

        self.accept_button_register_new_user_window = newutil.get_button(self.register_new_user_window, 'Accept', '#4CAF50', self.accept_register_new_user, fg="white", font=('Arial', 12))
        self.accept_button_register_new_user_window.place(x=450, y=530, width=100, height=40)

        self.try_again_button_register_new_user_window = newutil.get_button(self.register_new_user_window, 'Try again', '#F44336', self.try_again_register_new_user, fg="white", font=('Arial', 12))
        self.try_again_button_register_new_user_window.place(x=570, y=530, width=100, height=40)

        self.add_img_to_label(self.capture_label)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        if self.most_recent_capture_pil:
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            label.imgtk = imgtk
            label.configure(image=imgtk)

            self.register_new_user_capture = self.most_recent_capture_arr.copy()
        else:
            messagebox.showerror('Error', 'No image available to display.')

    def start(self):
        self.add_webcam(self.webcam_label)
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_register_new_user.get() 

        if self.most_recent_capture_pil:
            embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

            file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')
            pickle.dump(embeddings, file)

            messagebox.showinfo('Success!', 'User was registered successfully !')

            self.register_new_user_window.destroy()
        else:
            messagebox.showerror('Error', 'No image available for registration.')


if __name__ == "__main__":
    app = App()
    app.start()
