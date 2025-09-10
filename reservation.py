#Importing GUI and Database Libraries
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import create_connection
# Creating Reservation Display Page
class ReservationsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Title
        title_label = tk.Label(self, text="Your Reservations", fg="#0E12F1", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=10)
        # Treeview for displaying reservations
        columns = ("name", "flight_number", "departure", "destination", "date", "seat_number")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        # Define headings
        self.tree.heading("name", text="Name")
        self.tree.heading("flight_number", text="Flight Number")
        self.tree.heading("departure", text="Departure")
        self.tree.heading("destination", text="Destination")
        self.tree.heading("date", text="Date")
        self.tree.heading("seat_number", text="Seat Number")
        # Set column widths
        self.tree.column("name", width=120)
        self.tree.column("flight_number", width=100)
        self.tree.column("departure", width=100)
        self.tree.column("destination", width=100)
        self.tree.column("date", width=100)
        self.tree.column("seat_number", width=80)
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        scrollbar.grid(row=1, column=1, sticky="ns", pady=10)
        # Buttons frame
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        edit_btn = tk.Button(button_frame, bg="#0E12F1", fg="white", text="Edit Selected Reservation", command=self.edit_reservation)
        edit_btn.pack(side=tk.LEFT, padx=10)
        cancel_btn = tk.Button(button_frame, bg="#F93333", fg="white", text="Cancel Selected Reservation", command=self.delete_reservation)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        refresh_btn = tk.Button(button_frame, bg="#65DC29", fg="black", text="Refresh", command=self.load_reservations)
        refresh_btn.pack(side=tk.LEFT, padx=10)
        back_btn = tk.Button(button_frame, text="Back to Home", command=lambda: controller.show_frame("HomePage"))
        back_btn.pack(side=tk.LEFT, padx=10)
        # Bind the show event to automatically load reservations
        self.bind("<<ShowFrame>>", lambda e: self.load_reservations())
    #Loading Reservation
    def load_reservations(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Get data from database
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM reservations")
            rows = c.fetchall()
            conn.close()
            # Insert data into the Table
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
    #Edit Reservation Navigation Button
    def edit_reservation(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reservation to edit.")
            return
        item = self.tree.item(selected[0])
        reservation_id = item['values'][0]
        # Switch to edit page with the reservation ID
        self.controller.frames["EditReservationPage"].load_reservation(reservation_id)
        self.controller.show_frame("EditReservationPage")
    #Delete Reservation Button
    def delete_reservation(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reservation to delete.")
            return
        item = self.tree.item(selected[0])
        reservation_id = item['values'][0]
        name = item['values'][1]
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete reservation for {name}?"):
            try:
                conn = create_connection()
                c = conn.cursor()
                c.execute("DELETE FROM reservations WHERE id=?", (reservation_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Reservation deleted successfully!")
                self.load_reservations()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))