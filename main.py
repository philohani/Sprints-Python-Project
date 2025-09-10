#Importing GUI Libraries, Database Libraries, Pages files
import tkinter as tk
from tkinter import ttk
from database import setup_database
from home import HomePage
from booking import BookingPage
from reservation import ReservationsPage
from edit_reservation import EditReservationPage

class FlightReservationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set up the database
        setup_database()
        # Configure the main window
        self.title("Happy Wing For Flight Reservation")
        self.geometry("800x600")
        self.resizable(True, True)
        # Create a container frame to hold all pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # Dictionary to hold all frames
        self.frames = {}
        # Create and add all frames to the container
        for F in (HomePage, BookingPage, ReservationsPage, EditReservationPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        # Show the home page initially
        self.show_frame("HomePage")
    #Showing of the frame of the meant page
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
if __name__ == "__main__":
    app = FlightReservationApp()
    app.mainloop()