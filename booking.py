#Importing GUI library, Database library
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
from database import create_connection
#Creating a class for Booking page
class BookingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Configure grid
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)
        # Title
        title_label = tk.Label(self, text="Book a Flight", fg="#0E12F1",font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        # Input fields with consistent key names
        fields = [("Name:", "name"),("Flight Number:", "flight_number"),("Departure:", "departure"),("Destination:", "destination"),("Date (YYYY-MM-DD):", "date"),("Seat Number:", "seat_number")]
        self.entries = {}
        #Creating data fields for the form
        for i, (label_text, field_name) in enumerate(fields, 1):
            lbl = tk.Label(self, text=label_text, anchor="e")
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(self, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries[field_name] = entry
        # Creating Submit, Cancel and Return Buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        submit_btn = tk.Button(button_frame, text="Submit", bg="#0E12F1", fg="white", command=self.submit_booking)
        submit_btn.pack(side=tk.LEFT, padx=10)
        back_btn = tk.Button(button_frame, text="Return to Homepage", command=lambda: controller.show_frame("HomePage"))
        back_btn.pack(side=tk.LEFT, padx=10)
        cancel_btn = tk.Button(button_frame, text="Cancel", bg="#F93333", fg="white", command=self.clear_form)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    # Checking for the entered Date Format function
    def validate_date(self, date_string):
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    #Submitting the Booking Data to Database
    def submit_booking(self):
        # Get data from entries
        data = {}
        for key, entry in self.entries.items():
            data[key] = entry.get().strip()
            if not data[key]:
                messagebox.showerror("Error", f"Please fill in the {key.replace('_', ' ')} field.")
                return
        # Validate date format
        if not self.validate_date(data['date']):
            messagebox.showerror("Error", "Please enter date in YYYY-MM-DD format (e.g., 2023-12-25).")
            return
        # Save to database
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute('''INSERT INTO reservations 
                        (name, flight_number, departure, destination, date, seat_number) 
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (data['name'], data['flight_number'], data['departure'], 
                      data['destination'], data['date'], data['seat_number']))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Flight booked successfully!")
            self.clear_form()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
    #Clearing form after submittial to allow another entry
    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)