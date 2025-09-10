#Importing GUI and database libraries
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
from database import create_connection
#Creating class for editing reservation
class EditReservationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.current_id = None
        # Configure grid
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)
        # Title
        title_label = tk.Label(self, text="Edit Reservation", fg="#0E12F1", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=10)
        # Input fields with consistent key names
        fields = [("Name:", "name"),("Flight Number:", "flight_number"),("Departure:", "departure"),("Destination:", "destination"),("Date (YYYY-MM-DD):", "date"),("Seat Number:", "seat_number")]
        self.entries = {}
        #Creating Label and Entries for the form
        for i, (label_text, field_name) in enumerate(fields, 1):
            lbl = tk.Label(self, text=label_text, anchor="e")
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(self, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries[field_name] = entry
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=7, column=0, pady=20)
        update_btn = tk.Button(button_frame, text="Update", bg="#0E12F1", fg="white", command=self.update_reservation)
        update_btn.pack(side=tk.LEFT, padx=10)
        back_btn = ttk.Button(button_frame, text="Back to Reservations", command=lambda: controller.show_frame("ReservationsPage"))
        back_btn.pack(side=tk.LEFT, padx=10)
    #Checking for the Entered Date Format (YYYY-MM-DD)
    def validate_date(self, date_string):
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    #Loading the available Reservation
    def load_reservation(self, reservation_id):
        self.current_id = reservation_id
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM reservations WHERE id=?", (reservation_id,))
            row = c.fetchone()
            conn.close()
            if row:
                # Fill the form with existing data
                fields = ["name", "flight_number", "departure", "destination", "date", "seat_number"]
                for i, field in enumerate(fields, 1):
                    self.entries[field].delete(0, tk.END)
                    self.entries[field].insert(0, str(row[i]))
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
    #Updating Reservations
    def update_reservation(self):
        if not self.current_id:
            messagebox.showerror("Error", "No reservation loaded.")
            return
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
        # Update database
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute('''UPDATE reservations 
                        SET name=?, flight_number=?, departure=?, destination=?, date=?, seat_number=?
                        ''',
                     (data['name'], data['flight_number'], data['departure'], 
                      data['destination'], data['date'], data['seat_number']))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Reservation updated successfully!")
            self.controller.show_frame("ReservationsPage")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))