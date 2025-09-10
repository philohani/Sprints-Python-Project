#importing Tkinter Library for GUI
import tkinter as tk
from tkinter import ttk, messagebox

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Configure grid weights for centering
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        # Title
        icon=tk.PhotoImage(file="plane.png")
        icon=icon.subsample(20,20)
        title_label = tk.Label(self, text=" Happy Wings For Flight Reservations", fg="#0E12F1", image=icon, compound="left", font=("Arial", 24, "bold"))
        title_label.grid(row=1, column=1, pady=20)
        title_label.image = icon
        title_label.grid(row=1, column=1, pady=20)
        # Book Flight Button
        book_btn = tk.Button(self, bg="#0E12F1", fg="white", text="Book a Flight", command=lambda: controller.show_frame("BookingPage"),width=20)
        book_btn.grid(row=2, column=1, pady=10)
        # View Reservations Button
        view_btn = tk.Button(self, bg="#00F2FF", fg="black", text="View my Reservations", command=lambda: controller.show_frame("ReservationsPage"),width=20)
        view_btn.grid(row=3, column=1, pady=10)