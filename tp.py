#import mysql, tkinter lib
import datetime
import os
import re
from tkinter import filedialog
from tkinter import ttk
from fpdf import FPDF
import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Notebook
from PIL import Image, ImageTk
from tkinter import Entry
from tkcalendar import DateEntry
import sv_ttk


#connect to database

cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
cursor = cnx.cursor(buffered=True)

#create a users table

cursor.execute('''CREATE TABLE IF NOT EXISTS users(user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL, 
               email VARCHAR(255) NOT NULL, 
               password VARCHAR(255) NOT NULL)''')
cnx.commit()


#destinations table

cursor.execute('''CREATE TABLE IF NOT EXISTS destinations(destinations_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
               name VARCHAR(255) NOT NULL, 
               country VARCHAR(255) NOT NULL, 
               continent VARCHAR(255) NOT NULL, 
               description VARCHAR(255) NOT NULL,
               recommended_duration VARCHAR(255) NOT NULL, 
               image_path VARCHAR(255) NOT NULL)''')
cnx.commit()


#attractions table

cursor.execute('''CREATE TABLE IF NOT EXISTS attractions(attractions_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
               destinations_id INT NOT NULL, 
               name VARCHAR(255) NOT NULL,
                country VARCHAR(255) NOT NULL, 
               continent VARCHAR(255) NOT NULL, 
               description VARCHAR(255) NOT NULL,
               recommended boolean,
               recommended_duration VARCHAR(255) NOT NULL,
               recommended_day VARCHAR(255) NOT NULL,
                image_path VARCHAR(255) NOT NULL,
                FOREIGN KEY (destinations_id) REFERENCES destinations(destinations_id))''')
cnx.commit()

#booking table

cursor.execute('''CREATE TABLE IF NOT EXISTS booking(booking_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
               user_id INT NOT NULL, 
               start_location VARCHAR(255) NOT NULL, 
               destinations_id INT NOT NULL,  
               start_date DATE NOT NULL, 
               end_date DATE NOT NULL,
               FOREIGN KEY (user_id) REFERENCES users(user_id),
               FOREIGN KEY (destinations_id) REFERENCES destinations(destinations_id)
               )''')

cnx.commit()

#booking attractions table

cursor.execute('''CREATE TABLE IF NOT EXISTS booking_attractions(booking_attractions_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
               booking_id INT NOT NULL, 
               attractions_id INT NOT NULL, 
               FOREIGN KEY (booking_id) REFERENCES booking(booking_id),
               FOREIGN KEY (attractions_id) REFERENCES attractions(attractions_id)
               )''')
cnx.close()

#create a doctors table

#

#tp class( travel planner )

class tp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Login")
        self.root.geometry("1000x700")
        
        self.get_recommended_destinations()

        #style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', font=('Helvetica', 10))
        style.map('TCombobox', background=[('selected', 'yellow')])


        #display main image
        self.mainimage = Image.open("images/main.png")
        self.mainimage = ImageTk.PhotoImage(self.mainimage)
        self.mainlabel = Label(self.root, image=self.mainimage)
        self.mainlabel.image = self.mainimage
        self.mainlabel.place(x=0, y=0, relwidth=1, relheight=1)
        #timer for 2 seconds
        self.root.after(2000, self.login_screen)
    
    #get recommended destinations
    def get_recommended_destinations(self):

        recommended_destinations = []

        #get destinations from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute('''SELECT * FROM destinations''')
        for row in cursor:
            #iterate through attractions from destinations_id and count=recommended
            count = 0
            #get attractions from attractions table with destinations_id
            cursor2 = cnx.cursor(buffered=True)
            cursor2.execute('''SELECT * FROM attractions WHERE destinations_id = %s''', (row[0],))
            for row2 in cursor2:
                if row2[7] == 1:
                    count += 1
            dt={"destination_id": row[0], 'count': count}
            recommended_destinations.append(dt)
        cursor.close()

        #sort recommended destinations by count top 5
        recommended_destinations = sorted(recommended_destinations, key=lambda x: x['count'], reverse=True)
        recommended_destinations = recommended_destinations[0:5]
        self.recommended_destinations = recommended_destinations
        
    

    def login_screen(self):
        #destory all widget
        for widget in self.root.winfo_children():
            widget.destroy()

                #display bgimage
        self.bgimage = Image.open("images/bg2.png")
        self.bgimage = ImageTk.PhotoImage(self.bgimage)
        self.bglabel = Label(self.root, image=self.bgimage)
        self.bglabel.image = self.bgimage
        self.bglabel.place(x=0, y=0, relwidth=1, relheight=1)

        #geometry
        self.root.title("Login")
        self.root.geometry("1000x700")

        #frame layout
        self.frame = Frame(self.root)
        self.frame.place(x=240, y=130, width=500, height=350)
        #bg black
        self.frame.config(bg="black")



        #travel planner title
        self.label = Label(self.frame, text="Travel Planner", font=("Arial", 30,'bold'), bg="black",fg="white")
        self.label.place(x=130, y=0)

        self.label = Label(self.frame, text="Login", font=("Arial", 30,'bold'), bg="black",fg="white")
        self.label.place(x=250, y=50)

        self.label1 = Label(self.frame, text="Email", font=("Arial", 15), bg="black",fg="white")
        self.label1.place(x=100, y=150)

        self.label2 = Label(self.frame, text="Password", font=("Arial", 15), bg="black",fg="white")
        self.label2.place(x=100, y=200)
        
        self.entry1 = Entry(self.frame, font=("Arial", 15))
        self.entry1.place(x=200, y=150)

        #eye image as button
        self.eyeimage = Image.open("images/eye.png")
        #resize image
        self.eyeimage = self.eyeimage.resize((30, 30), Image.LANCZOS)
        #convert image to photoimage
        self.eyeimage = ImageTk.PhotoImage(self.eyeimage)
        self.eyebutton = Button(self.frame, image=self.eyeimage,borderwidth=0,highlightthickness=0,command=self.show_password)
        self.eyebutton.image = self.eyeimage
        self.eyebutton.place(x=430, y=200)

        self.entry2 = Entry(self.frame, font=("Arial", 15),show="*")
        self.entry2.place(x=200, y=200)

        self.button = Button(self.frame, text="Login", font=("Arial", 15), command=self.login)
        self.button.place(x=230, y=250)

        #register
        self.button1 = Button(self.frame, text="Register", font=("Arial", 15), command=self.register)
        self.button1.place(x=350, y=250)
        

        #place ig image as button
        self.igimage = Image.open("images/ig.jpg")
        #resize image
        self.igimage = self.igimage.resize((50, 50), Image.LANCZOS)
        #convert image to photoimage
        self.igimage = ImageTk.PhotoImage(self.igimage)
        self.iglabel = Button(self.root, image=self.igimage,borderwidth=0,highlightthickness=0)
        self.iglabel.image = self.igimage
        self.iglabel.place(x=400, y=450)

        #place fb image as button
        self.fbimage = Image.open("images/fb.jpg")
        #resize image
        self.fbimage = self.fbimage.resize((100, 100), Image.LANCZOS)
        #convert image to photoimage
        self.fbimage = ImageTk.PhotoImage(self.fbimage)
        self.fblabel = Button(self.root, image=self.fbimage,borderwidth=0,highlightthickness=0)
        self.fblabel.image = self.fbimage
        self.fblabel.place(x=470, y=425)

        #place twt image as button
        self.twtimage = Image.open("images/twt.jpg")
        #resize image
        self.twtimage = self.twtimage.resize((50, 50), Image.LANCZOS)
        #convert image to photoimage
        self.twtimage = ImageTk.PhotoImage(self.twtimage)
        self.twtlabel = Button(self.root, image=self.twtimage,borderwidth=0,highlightthickness=0)
        self.twtlabel.image = self.twtimage
        self.twtlabel.place(x=570, y=450)

    #show password
    def show_password(self):
        if self.entry2.cget('show') == '*':
            self.entry2.config(show="")
        else:
            self.entry2.config(show="*")



    def login(self):
        email = self.entry1.get()
        password = self.entry2.get()
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)

        #if admin login open admin page
        if email == "admin" and password == "admin":
            self.admin_page()
            return
        

        cursor.execute("SELECT * FROM users WHERE email = '%s' AND password = '%s'" % (email, password))
        row = cursor.fetchone()

        if row is not None:
            messagebox.showinfo("Login", "Login Successfull")
            self.user_id = row[0]

            self.main_menu()
        else:
            messagebox.showerror("Login", "Login Failed")

    #admin_page
    def admin_page(self):
               #destory all widget
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Admin Menu")
        self.root.geometry("1100x800")

        #frame
        self.frame = Frame(self.root, width=1100, height=800)
        self.frame.place(x=0, y=0)

        self.bgimage = Image.open("images/bg3.png")
        self.bgimage = ImageTk.PhotoImage(self.bgimage)
        self.bglabel = Label(self.frame, image=self.bgimage)
        self.bglabel.image = self.bgimage
        self.bglabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = Label(self.frame, text="Main Menu", font=("Arial", 20),bg="black",fg="white")
        self.label.place(x=500, y=20)

        #logout button top right corner
        self.button1 = Button(self.frame, text="Logout", font=("Arial", 15), command=self.logout)
        self.button1.place(x=1000, y=20)

        #Recommendations button light green
        self.button2 = Button(self.frame, text="Recommendations", font=("Arial", 15), command=self.admin_recommendations)
        self.button2.place(x=50, y=100)

        #Explore Destinations button light green
        self.button3 = Button(self.frame, text="Explore Destinations", font=("Arial", 15), command=self.admin_explore_destinations)
        self.button3.place(x=250, y=100)

        #Explore Attractions button
        self.button4 = Button(self.frame, text="Explore Attractions", font=("Arial", 15), command=self.admin_explore_attractions)
        self.button4.place(x=450, y=100)

        #download reports
        self.button5 = Button(self.frame, text="Download Reports", font=("Arial", 15), command=self.admin_download_reports)
        self.button5.place(x=650, y=100)
        
        #contents frame
        self.frame1 = Frame(self.frame, width=1000, height=500,bg="black")
        self.frame1.place(x=50, y=150)

        self.admin_recommendations()

    #admin_download_reports
    def admin_download_reports(self):
        #clear contents frame
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #download destinations report button
        self.button1 = Button(self.frame1, text="Download Destinations Report", font=("Arial", 15), command=self.admin_download_destinations_report)
        self.button1.place(x=100, y=100)
        
        #download attractions report button
        self.button2 = Button(self.frame1, text="Download Attractions Report", font=("Arial", 15), command=self.admin_download_attractions_report)
        self.button2.place(x=100, y=150)

        #download users report button
        self.button3 = Button(self.frame1, text="Download Users Report", font=("Arial", 15), command=self.admin_download_users_report)
        self.button3.place(x=100, y=200)

        #download bookings report button
        self.button4 = Button(self.frame1, text="Download Bookings Report", font=("Arial", 15), command=self.admin_download_bookings_report)
        self.button4.place(x=100, y=250)


    #admin_download_destinations_report
    def admin_download_destinations_report(self):
        #get data from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute('''SELECT * FROM destinations''')
        rows = cursor.fetchall()

        #insert into pdf
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        #add date and time
        pdf.cell(200, 10, txt="Date: " + str(datetime.datetime.now()), ln=True)
        pdf.ln()
        #add title
        pdf.cell(200, 10, txt="Destinations Report", ln=True)
        pdf.ln()
        #add header
        pdf.cell(50, 10, txt="Destination", border=1)
        pdf.cell(50, 10, txt="Country", border=1)
        pdf.cell(50, 10, txt="Continent", border=1)
        pdf.cell(50, 10, txt="Description", border=1)
        pdf.cell(50, 10, txt="Recommended Duration", border=1)
        pdf.ln()
        #add data
        for destination in rows:
            destination_name = destination[1]
            country = destination[2]
            continent = destination[3]
            description = destination[4]
            recommended_duration = destination[5]
            pdf.cell(50, 10, txt=destination_name, border=1)
            pdf.cell(50, 10, txt=country, border=1)
            pdf.cell(50, 10, txt=continent, border=1)
            pdf.cell(50, 10, txt=description, border=1)
            pdf.cell(50, 10, txt=recommended_duration, border=1)
            pdf.ln()

        pdf.output('reports/destinations_report.pdf')
        
        #message
        messagebox.showinfo("Report", "Destinations Report Downloaded")


    #admin_download_attractions_report
    def admin_download_attractions_report(self):
        #get data from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute('''SELECT * FROM attractions''')
        rows = cursor.fetchall()
        
        #insert into pdf    pdf = FPDF()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        #add date and time
        pdf.cell(200, 10, txt="Date: " + str(datetime.datetime.now()), ln=True)
        #add title
        pdf.cell(200, 10, txt="Attractions Report", ln=True)
        pdf.ln()
        #add header
        pdf.cell(50, 10, txt="Attraction", border=1)
        pdf.cell(50, 10, txt="Country", border=1)
        pdf.cell(50, 10, txt="Continent", border=1)
        pdf.cell(50, 10, txt="Description", border=1)
        pdf.cell(50, 10, txt="Recommended Duration", border=1)
        pdf.ln()
        #add data
        for attraction in rows:
            attraction_name = attraction[2]
            country = attraction[3]
            continent = attraction[4]
            description = attraction[5]
            recommended_duration = attraction[7]
            pdf.cell(50, 10, txt=attraction_name, border=1)
            pdf.cell(50, 10, txt=country, border=1)
            pdf.cell(50, 10, txt=continent, border=1)
            pdf.cell(50, 10, txt=description, border=1)
            pdf.cell(50, 10, txt=recommended_duration, border=1)
            pdf.ln()


        pdf.output('reports/attractions_report.pdf')
        
        #message
        messagebox.showinfo("Report", "Attractions Report Downloaded")

    #admin_download_users_report
    def admin_download_users_report(self):
        #get data from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute('''SELECT * FROM users''')
        rows = cursor.fetchall()
        
        #insert into pdf    pdf = FPDF()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        #add date and time
        pdf.cell(200, 10, txt="Date: " + str(datetime.datetime.now()), ln=True)
        #add title
        pdf.cell(200, 10, txt="Users Report", ln=True)
        pdf.ln()
        #add header
        pdf.cell(50, 10, txt="Name", border=1)
        pdf.cell(50, 10, txt="Email", border=1)
        pdf.cell(50, 10, txt="Password", border=1)
        pdf.ln()
        #add data
        for user in rows:
            user_name = user[1]
            pdf.cell(50, 10, txt=user_name, border=1)
            pdf.cell(50, 10, txt=user[2], border=1)
            pdf.cell(50, 10, txt=user[3], border=1)
            pdf.ln()


        pdf.output('reports/users_report.pdf')

        #message
        messagebox.showinfo("Report", "Users Report Downloaded")

    #admin_download_bookings_report
    def admin_download_bookings_report(self):
        #get data from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute('''SELECT * FROM booking''')
        rows = cursor.fetchall()
        
        #insert into pdf    pdf = FPDF()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        #add date and time
        pdf.cell(200, 10, txt="Date: " + str(datetime.datetime.now()), ln=True)
        #add title
        pdf.cell(200, 10, txt="Bookings Report", ln=True)
        pdf.ln()
        #add header
        pdf.cell(50, 10, txt="Booking ID", border=1)
        pdf.cell(50, 10, txt="User ID", border=1)
        pdf.cell(50, 10, txt="Start Location", border=1)
        pdf.cell(50, 10, txt="Destination Id", border=1)
        pdf.cell(50, 10, txt="Start Date", border=1)    
        pdf.cell(50, 10, txt="End Date", border=1)
        pdf.ln()
        #add data
        for booking in rows:
            booking_id = booking[0]
            user_id = booking[1]
            start_location = booking[2]
            destination_id = booking[3]
            start_date = booking[4]
            end_date = booking[5]
            pdf.cell(50, 10, txt=booking_id, border=1)
            pdf.cell(50, 10, txt=user_id, border=1)
            pdf.cell(50, 10, txt=start_location, border=1)
            pdf.cell(50, 10, txt=destination_id, border=1)
            pdf.cell(50, 10, txt=start_date, border=1)
            pdf.cell(50, 10, txt=end_date, border=1)
            pdf.ln()

        pdf.output('reports/bookings_report.pdf')
        
        #message
        messagebox.showinfo("Report", "Bookings Report Downloaded")

    #admin_recommendations
    def admin_recommendations(self):
        
        #clear contents frame
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #display destinations from recommendation destinations

        #create a canvas in frame1
        self.canvas = Canvas(self.frame1, width=1000, height=400,bg="black",highlightthickness=0)
        self.canvas.place(x=0, y=0)

        #frame inside in canvas
        self.frame2 = Frame(self.canvas, width=1000, height=400,bg="black")
        self.frame2.place(x=0, y=0)

        #scrollbar
        self.scrollbar = Scrollbar(self.frame1, command=self.canvas.yview)
        self.scrollbar.place(x=1000, y=0)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.frame2, anchor="nw")
        self.frame2.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        #get data from recommended_destinations list

        current=0
        for row in self.recommended_destinations:
            destination_id = row["destination_id"]

            #get data from table
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor = cnx.cursor(buffered=True)
            cursor.execute('''SELECT * FROM destinations WHERE destinations_id = %s''', (destination_id,))
            row = cursor.fetchone()
            cursor.close()

            destination = list(row)
            destination = {
                "destination_id": destination[0],
                "destination_name": destination[1],
                "destination_image_path": destination[6]
            }

            image = Image.open(destination["destination_image_path"])
            image = image.resize((200, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = current // 6
            col = current % 6

            destination_button = Button(self.frame2, image=photo, command=lambda destination=destination: self.show_destination_details(destination))
            destination_button.image = photo
            destination_button.grid(row=row, column=col, padx=10, pady=10)
            #name
            destination_name = Label(self.frame2, text=destination["destination_name"], font=("Arial", 15),bg="black",fg="white")
            destination_name.grid(row=row+1, column=col, padx=10, pady=10)

            current += 1

    #logout





        
    #admin_explore_destinations
    def admin_explore_destinations(self):
                
        #clear contents frame
        for widget in self.frame1.winfo_children():
            widget.destroy()


        #add destination button
        self.button = Button(self.frame1, text="Add Destination", font=("Arial", 15),command=self.add_destination)
        self.button.place(x=0, y=10)


        #create a canvas in frame1
        self.canvas = Canvas(self.frame1, width=1000, height=400, bg ='black',highlightthickness=0)
        self.canvas.place(x=0, y=80)

        #frame inside in canvas
        self.frame2 = Frame(self.canvas, width=1000, height=400, bg ='black')
        self.frame2.place(x=0, y=0)

        #scrollbar
        self.scrollbar = Scrollbar(self.frame1, command=self.canvas.yview)
        self.scrollbar.place(x=1000, y=0)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.create_window((0, 0), window=self.frame2, anchor="nw")

        self.frame2.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        #get all destinations from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)

        cursor.execute("SELECT * FROM destinations")
        rows = cursor.fetchall()

        current_i = 0
        for i, destination in enumerate(rows):
            # display destination image as button
            destination = list(destination)
            destination = {
                "destination_id": destination[0],
                "destination_name": destination[1],
                "destination_image_path": destination[6]
            }
            image = Image.open(destination["destination_image_path"])
            image = image.resize((200, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            destination_button = Button(self.frame2, image=photo, command=lambda destination=destination: self.show_destination_details(destination))
            destination_button.image = photo
            destination_button.grid(row=row, column=col, padx=10, pady=10)
            destination_name = Label(self.frame2, text=destination["destination_name"], font=("Arial", 15),bg="black",fg="white")
            destination_name.grid(row=row+1, column=col, padx=10, pady=10)
            current_i = i

        cnx.close()

    #add destination
    def add_destination(self):
        #clear contents frame
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #enter destination details
        self.label = Label(self.frame1, text="Add Destination", font=("Arial", 20),bg="black",fg="white")
        self.label.place(x=400, y=10)
        
        #Name
        self.label1 = Label(self.frame1, text="Name", font=("Arial", 15),bg="black",fg="white")
        self.label1.place(x=100, y=100)
        
        self.entry1 = Entry(self.frame1, font=("Arial", 15))
        self.entry1.place(x=330, y=100)

        #Country
        self.label2 = Label(self.frame1, text="Country", font=("Arial", 15),bg="black",fg="white")
        self.label2.place(x=100, y=150)
        
        self.entry2 = Entry(self.frame1, font=("Arial", 15))
        self.entry2.place(x=330, y=150)

        #Continent
        self.label3 = Label(self.frame1, text="Continent", font=("Arial", 15),bg="black",fg="white")
        self.label3.place(x=100, y=200)

        #continent combobox
        continent=["Africa", "Asia", "Europe", "North America", "South America", "Australia"]
        self.combobox = Combobox(self.frame1, values=continent, font=("Arial", 15))
        self.combobox.place(x=330, y=200)

        #Description
        self.label4 = Label(self.frame1, text="Description", font=("Arial", 15),bg="black",fg="white")
        self.label4.place(x=100, y=250)

        self.entry4 = Entry(self.frame1, font=("Arial", 15))
        self.entry4.place(x=330, y=250)

        #Recommended Duration
        self.label5 = Label(self.frame1, text="Duration", font=("Arial", 15),bg="black",fg="white")
        self.label5.place(x=100, y=300)

        #Combobox 
        duration=["1 week", "2 weeks", "3 weeks", "1 Month", "2 Months", "3 Months"]
        self.combobox1 = Combobox(self.frame1, values=duration, font=("Arial", 15))
        self.combobox1.place(x=330, y=300)

        #Image Path
        self.label6 = Label(self.frame1, text="Image Path", font=("Arial", 15),bg="black",fg="white")
        self.label6.place(x=100, y=350)

        #Image path button
        self.button = Button(self.frame1, text="Browse", font=("Arial", 15), command=self.browse_image)
        self.button.place(x=330, y=350)

        #Add Destination Button
        self.button = Button(self.frame1, text="Add Destination", font=("Arial", 15), command=self.add_destination_db)
        self.button.place(x=200, y=400)

    #browse image
    def browse_image(self):
        image_path = filedialog.askopenfilename()
        
        #if image path is not empty
        if image_path:
            self.image_path = image_path

            #messagebox
            messagebox.showinfo("Add Destination", "Image Path Added Successfully")

        else:
            messagebox.showerror("Add Destination", "Image Path Not Added")
        
    #add destination to database
    def add_destination_db(self):
        name = self.entry1.get()
        country = self.entry2.get()
        continent = self.combobox.get()
        description = self.entry4.get()
        recommended_duration = self.combobox1.get()
        image_path = self.image_path

        #validation
        #check if all fields are filled
        if name == "" or country == "" or continent == "" or description == "" or recommended_duration == "" or image_path == "":
            messagebox.showerror("Add Destination", "All Fields Required")
        #check if image path is not empty
        elif not image_path:
            messagebox.showerror("Add Destination", "Image Path Required")
        else:
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor = cnx.cursor(buffered=True)

            cursor.execute("INSERT INTO destinations(name, country, continent, description, recommended_duration, image_path) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (name, country, continent, description, recommended_duration, image_path))
            cnx.commit()
            messagebox.showinfo("Add Destination", "Destination Added Successfully")
            self.admin_page()


    #admin_explore_attractions
    def admin_explore_attractions(self,destinations_id=None):
        #clear
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #add attraction button
        self.button = Button(self.frame1, text="Add Attraction", font=("Arial", 15), command=self.add_attraction)
        self.button.place(x=0, y=10)

        #create a canvas in frame1
        self.canvas = Canvas(self.frame1, width=1000, height=400, bg ='black',highlightthickness=0)
        self.canvas.place(x=0, y=80)

        #frame inside in canvas
        self.frame2 = Frame(self.canvas, width=1000, height=400, bg ='black')
        self.frame2.place(x=0, y=0)

        #scrollbar
        self.scrollbar = Scrollbar(self.frame1, command=self.canvas.yview)
        self.scrollbar.place(x=1000, y=0)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.frame2, anchor="nw")
        self.scrollbar.config(command=self.canvas.yview)

        self.frame2.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        rows=[]
        if destinations_id:
            #get all attractions from database
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor = cnx.cursor(buffered=True)
            cursor.execute("SELECT * FROM attractions where destinations_id = %s" , (destinations_id))
            rows = cursor.fetchall()
            cnx.close()

        #get all attractions from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT * FROM attractions ")
        rows = cursor.fetchall()
        cnx.close()

        current_i = 0
        for i, attraction in enumerate(rows):
            attraction = {
                "attraction_id": attraction[0],
                "attraction_name": attraction[2],
                "attraction_image_path": attraction[9]
            }
            image = Image.open(attraction["attraction_image_path"])
            image = image.resize((200, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            attraction_button = Button(self.frame2, image=photo, command=lambda attraction=attraction: self.show_attraction_details(attraction))
            attraction_button.image = photo
            attraction_button.grid(row=row, column=col, padx=10, pady=10)
            attraction_name = Label(self.frame2, text=attraction["attraction_name"], font=("Arial", 15),bg="black",fg="white")
            attraction_name.grid(row=row+1 ,column=col, padx=10, pady=10)
            current_i = i

        

    #show_attraction_details
    def show_attraction_details(self, attraction):
        attraction_id = attraction["attraction_id"]
        attraction_name = attraction["attraction_name"]
        attraction_image_path = attraction["attraction_image_path"]

        #clear contents frame
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #get attraction details from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT * FROM attractions WHERE attractions_id = %s" % (attraction_id))
        attraction = cursor.fetchone()
        cnx.close()
        
        print(attraction)

        #label attraction details
        self.label = Label(self.frame1, text="Attraction Details", font=("Arial", 20),bg="black",fg="white")
        self.label.place(x=400, y=10)

        #Name
        self.label1 = Label(self.frame1, text="Name", font=("Arial", 15),bg="black",fg="white")
        self.label1.place(x=100, y=100)
        
        self.entry1 = Entry(self.frame1, font=("Arial", 15))
        self.entry1.place(x=330, y=100)

        #fill in attraction details
        self.entry1.insert(0, attraction[2])

        #country
        self.label2 = Label(self.frame1, text="Country", font=("Arial", 15),bg="black",fg="white")
        self.label2.place(x=100, y=150)
        
        self.entry2 = Entry(self.frame1, font=("Arial", 15))
        self.entry2.place(x=330, y=150)

        #fill in attraction details
        self.entry2.insert(0, attraction[3])

        #continent
        self.label3 = Label(self.frame1, text="Continent", font=("Arial", 15),bg="black",fg="white")
        self.label3.place(x=100, y=200)
        
        self.entry3 = Entry(self.frame1, font=("Arial", 15))
        self.entry3.place(x=330, y=200)

        #fill in attraction details
        self.entry3.insert(0, attraction[4])

        #description
        self.label4 = Label(self.frame1, text="Description", font=("Arial", 15),bg="black",fg="white")
        self.label4.place(x=100, y=250)
        
        self.entry4 = Entry(self.frame1, font=("Arial", 15))
        self.entry4.place(x=330, y=250)

        #fill in attraction details
        self.entry4.insert(0, attraction[5])

        #recommended_duration
        self.label5 = Label(self.frame1, text="Recommended Duration", font=("Arial", 15),bg="black",fg="white")
        self.label5.place(x=100, y=300)

        self.entry5 = Entry(self.frame1, font=("Arial", 15))
        self.entry5.place(x=330, y=300)

        #fill in attraction details
        self.entry5.insert(0, attraction[7])

        #recommended_day
        self.label6 = Label(self.frame1, text="Recommended Day", font=("Arial", 15),bg="black",fg="white")
        self.label6.place(x=100, y=350)
        
        self.entry6 = Entry(self.frame1, font=("Arial", 15))
        self.entry6.place(x=330, y=350)

        #fill in attraction details
        self.entry6.insert(0, attraction[8])


        self.image_path = attraction[9]

        self.delete_attraction_id = attraction_id

        #display image
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(self.image)
        self.image_label = Label(self.frame1, image=photo)
        self.image_label.image = photo
        self.image_label.place(x=700, y=100)

        #update button
        self.update_button = Button(self.frame1, text="Update", font=("Arial", 15), command=lambda attraction=attraction: self.update_attraction(attraction))
        self.update_button.place(x=400, y=400)

        #delete button
        self.delete_button = Button(self.frame1, text="Delete", font=("Arial", 15), command=lambda attraction=attraction: self.delete_attraction(attraction))
        self.delete_button.place(x=500, y=400)

        #back button
        self.back_button = Button(self.frame1, text="Back", font=("Arial", 15), command=lambda attraction=attraction: self.admin_page())
        self.back_button.place(x=600, y=400)

    #update_attraction
    def update_attraction(self, attraction):
        #get data
        attraction_name = self.entry1.get()
        attraction_country = self.entry2.get()
        attraction_continent = self.entry3.get()
        attraction_description = self.entry4.get()
        attraction_recommended_duration = self.entry5.get()
        attraction_recommended_day = self.entry6.get()

        #check if data is empty
        if attraction_name == "" or attraction_country == "" or attraction_continent == "" or attraction_description == "" or attraction_recommended_duration == "" or attraction_recommended_day == "":
            messagebox.showerror("Error", "Please fill in all fields")
        else:
            #update attraction in database
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor = cnx.cursor(buffered=True)
            cursor.execute("UPDATE attractions SET name = %s, country = %s, continent = %s, description = %s, recommended_duration = %s, recommended_day = %s WHERE attractions_id = %s" , (attraction_name, attraction_country, attraction_continent, attraction_description, attraction_recommended_duration, attraction_recommended_day, self.delete_attraction_id))
            cnx.commit()

            messagebox.showinfo("Success", "Attraction updated successfully")
            self.admin_page()
        
                                                                                                                                                                                                                                                            

    #delete_attraction
    def delete_attraction(self, attraction):
        try:
            #get id from attraction
            attraction_id = self.delete_attraction_id
            #delete attraction from database
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor = cnx.cursor(buffered=True)
            cursor.execute("DELETE FROM attractions WHERE attractions_id = %s" % (attraction_id))
            cnx.commit()
            messagebox.showinfo("Success", "Attraction deleted successfully")
            self.admin_page()
        except:
            #we cannot delete as ticket is booked with this attraction
            messagebox.showerror("Error", "You cannot delete this attraction as it is booked by tickets")









    #show destination details
    def show_destination_details(self, destination):

        destination_id = destination["destination_id"]

        #get destination details from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT * FROM destinations WHERE destinations_id = %s" % (destination_id))
        destination = cursor.fetchone()
        cnx.close()



        #clear contents frame
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #label destination details
        self.label = Label(self.frame1, text="Destination Details", font=("Arial", 20),bg="black",fg="white")
        self.label.place(x=400, y=10)

        #Name
        self.label1 = Label(self.frame1, text="Name", font=("Arial", 15),bg="black",fg="white")
        self.label1.place(x=100, y=100)
        
        self.entry1 = Entry(self.frame1, font=("Arial", 15),width=22)
        self.entry1.place(x=320, y=100)

        #fill in destination details
        self.entry1.insert(0, destination[1])

        #country
        self.label2 = Label(self.frame1, text="Country", font=("Arial", 15),bg="black",fg="white")
        self.label2.place(x=100, y=150)
        
        self.entry2 = Entry(self.frame1, font=("Arial", 15), width=22)
        self.entry2.place(x=320, y=150)

        #fill in destination details
        self.entry2.insert(0, destination[2])

        #continent
        self.label3 = Label(self.frame1, text="Continent", font=("Arial", 15),bg="black",fg="white")
        self.label3.place(x=100, y=200)

        continents = ["Asia", "Europe", "North America", "South America", "Australia", "Africa","Antarctica"]

        self.combobox = Combobox(self.frame1, values=continents, font=("Arial", 15))
        self.combobox.place(x=320, y=200)

        #fill in destination details
        self.combobox.set(destination[3])

        #description
        self.label4 = Label(self.frame1, text="Description", font=("Arial", 15),bg="black",fg="white")
        self.label4.place(x=100, y=250)

        self.entry4 = Entry(self.frame1, font=("Arial", 15),width=22)
        self.entry4.place(x=320, y=250)

        #fill in destination details
        self.entry4.insert(0, destination[4])

        #recommended duration
        self.label5 = Label(self.frame1, text="Recommended Duration", font=("Arial", 15),bg="black",fg="white")
        self.label5.place(x=100, y=300)

        duration=["1 Day","1 week", "2 weeks", "3 weeks", "1 Month", "2 Months", "3 Months"]
        self.combobox1 = Combobox(self.frame1, values=duration, font=("Arial", 15))
        self.combobox1.place(x=320, y=300)
        
        #fill in destination details
        self.combobox1.set(destination[5])

        #update button
        self.button = Button(self.frame1, text="Update", font=("Arial", 15), command=self.update_destination)
        self.button.place(x=100, y=350)

        self.image_path=destination[6]

        #display image 
        image = Image.open(destination[6])
        image = image.resize((200, 250), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        attraction_button = Button(self.frame1, image=photo)
        attraction_button.image = photo
        attraction_button.place(x=700, y=100)

        self.delete_destination_id=destination_id

        #delete button
        self.button1 = Button(self.frame1, text="Delete", font=("Arial", 15), command=self.delete_destination)
        self.button1.place(x=200, y=350)

        #back button
        self.button2 = Button(self.frame1, text="Back", font=("Arial", 15), command=self.admin_page)
        self.button2.place(x=330, y=350)

        #go into attraction details
        self.button3 = Button(self.frame1, text="Attractions", font=("Arial", 15), command=lambda destination=destination: self.admin_explore_attractions(destination[0]))
        self.button3.place(x=400, y=350)



    #update_destination
    def update_destination(self):
        #get entries
        name = self.entry1.get()
        country = self.entry2.get()
        continent = self.combobox.get()
        description = self.entry4.get()
        recommended_duration = self.combobox1.get()
        image_path = self.image_path

        #check if data is available
        if name == "":
            messagebox.showerror("Error", "Name is required")
        elif country == "":
            messagebox.showerror("Error", "Country is required")
        elif continent == "":
            messagebox.showerror("Error", "Continent is required")
        elif description == "":
            messagebox.showerror("Error", "Description is required")
        elif recommended_duration == "":
            messagebox.showerror("Error", "Recommended Duration is required")
        elif image_path == "":
            messagebox.showerror("Error", "Image is required")
        else:
            print(name, country, continent, description, recommended_duration, image_path)            
            #update destination_id
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor = cnx.cursor()
            cursor.execute("UPDATE destinations SET name = %s, country = %s, continent = %s, description = %s, recommended_duration = %s, image_path = %s WHERE destinations_id = %s" , (name, country, continent, description, recommended_duration, image_path, self.delete_destination_id))
            cnx.commit()
            cnx.close()

            #message
            messagebox.showinfo("Success", "Destination updated successfully")
            self.admin_page()        


    #delete_destination
    def delete_destination(self):

        #delete destination_id
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("DELETE FROM destinations WHERE destinations_id = %s" % (self.delete_destination_id))
        cnx.commit()
        cnx.close()

        #message
        messagebox.showinfo("Success", "Destination deleted successfully")
        self.admin_page()









    #add attraction
    def add_attraction(self):
        #clear contents frame
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #enter attraction details
        self.label = Label(self.frame1, text="Add Attraction", font=("Arial", 20),bg="black",fg="white")
        self.label.place(x=400, y=10)
        
        #Name
        self.label1 = Label(self.frame1, text="Name", font=("Arial", 15),bg="black",fg="white")
        self.label1.place(x=100, y=100)
        
        self.entry1 = Entry(self.frame1, font=("Arial", 15))
        self.entry1.place(x=330, y=100)

        #Country

        #get countries from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT DISTINCT name FROM destinations")
        countries = cursor.fetchall()
        countries = [country[0] for country in countries]
        countries.insert(0, "Select Country")

        self.label2 = Label(self.frame1, text="Country", font=("Arial", 15),bg="black",fg="white")
        self.label2.place(x=100, y=150)
        
        self.combobox1 = Combobox(self.frame1, values=countries, font=("Arial", 15))
        self.combobox1.place(x=330, y=150)

        #select event for country
        self.combobox1.bind("<<ComboboxSelected>>", self.select_country)

        #get desintation name from country selected


        #destination name
        self.label3 = Label(self.frame1, text="Destination", font=("Arial", 15),bg="black",fg="white")
        self.label3.place(x=100, y=200)
        
        self.comboboxD = Combobox(self.frame1, values=[" Select Country"], font=("Arial", 15))
        self.comboboxD.place(x=330, y=200)


        #Continent
        self.label3 = Label(self.frame1, text="Continent", font=("Arial", 15),bg="black",fg="white")
        self.label3.place(x=100, y=250)

        #continent combobox
        continent=["Africa", "Asia", "Europe", "North America", "South America", "Australia"]
        self.combobox2 = Combobox(self.frame1, values=continent, font=("Arial", 15))
        self.combobox2.place(x=330, y=250)

        #Description
        self.label4 = Label(self.frame1, text="Description", font=("Arial", 15),bg="black",fg="white")
        self.label4.place(x=100, y=300)

        self.entry4 = Entry(self.frame1, font=("Arial", 15))
        self.entry4.place(x=330, y=300)

        #Recommended Duration
        self.label5 = Label(self.frame1, text="Duration", font=("Arial", 15),bg="black",fg="white")
        self.label5.place(x=100, y=350)

        #Combobox 
        duration=["1 Day","1 week", "2 weeks", "3 weeks", "1 Month", "2 Months", "3 Months"]
        self.combobox3 = Combobox(self.frame1, values=duration, font=("Arial", 15))
        self.combobox3.place(x=330, y=350)

        #Recommended Day
        self.label6 = Label(self.frame1, text="Day",font=("Arial", 15),bg="black",fg="white")
        self.label6.place(x=100, y=400)

        #Combobox
        day=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.combobox4 = Combobox(self.frame1, values=day, font=("Arial", 15))
        self.combobox4.place(x=330, y=400)

        #checkbutton for recommended
        self.label7 = Label(self.frame1, text="Recommended", font=("Arial", 15),bg="black",fg="white")
        self.label7.place(x=600, y=250)
        self.checkbutton_var = IntVar()
        self.checkbutton = Checkbutton(self.frame1, font=("Arial", 15))
        self.checkbutton.place(x=750, y=250)
        self.checkbutton.config(variable=self.checkbutton_var)

        #Image
        self.label8 = Label(self.frame1, text="Image", font=("Arial", 15),bg="black",fg="white")
        self.label8.place(x=100, y=450)    

        #browse button
        self.button = Button(self.frame1, text="Browse", font=("Arial", 15), command=self.browse_image)
        self.button.place(x=330, y=450)

        #submit button
        self.button1 = Button(self.frame1, text="Submit", font=("Arial", 15), command=self.add_attraction_to_database)
        self.button1.place(x=400, y=500)

        #back
        self.button2 = Button(self.frame1, text="Back", font=("Arial", 15), command=self.admin_page)
        self.button2.place(x=500, y=500)

    #select country
    def select_country(self, event):
        country = self.combobox1.get()
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)

        #get destination_id from database
        cursor.execute("SELECT name  FROM destinations WHERE country = '%s'" % country)
        destination_id = cursor.fetchall()
        destination_id = [destination_id[0] for destination_id in destination_id]
        destination_id.insert(0, "Select Destination")
        self.comboboxD.config(values=destination_id)


    #add attraction to database
    def add_attraction_to_database(self):
        attraction_name = self.entry1.get()
        attraction_country = self.combobox1.get()
        attraction_continent = self.combobox2.get()
        attraction_description = self.entry4.get()
        attraction_duration = self.combobox3.get()
        attraction_day = self.combobox4.get()
        attraction_image_path = self.image_path
        destination_name = self.comboboxD.get()
        var=self.checkbutton_var.get()


        #validation
        if attraction_name == "" or attraction_country == "" or attraction_continent == "" or attraction_description == "" or attraction_duration == "" or attraction_day == ""or attraction_image_path == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor = cnx.cursor(buffered=True)

            #get destination_id from database
            cursor.execute("SELECT destinations_id FROM destinations WHERE name = '%s'" % destination_name)
            destination_id = cursor.fetchone()
            destination_id = destination_id[0]
            destination_id = int(destination_id)

                        #add attraction to database
            cursor.execute("INSERT INTO attractions (name, country, continent, description, recommended_duration, recommended_day, image_path, destinations_id, recommended) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (attraction_name, attraction_country, attraction_continent, attraction_description, attraction_duration, attraction_day, attraction_image_path, destination_id, var))
            cnx.commit()
            messagebox.showinfo("Success", "Attraction added successfully")
            self.admin_page()
            cnx.close()
      










    def register(self):
        #destory all widget
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Register")
        self.root.geometry("1000x700")

                #display bgimage
        self.bgimage = Image.open("images/bg2.png")
        self.bgimage = ImageTk.PhotoImage(self.bgimage)
        self.bglabel = Label(self.root, image=self.bgimage)
        self.bglabel.image = self.bgimage
        self.bglabel.place(x=0, y=0, relwidth=1, relheight=1)


        self.frame = Frame(self.root, bg="black")
        self.frame.place(x=400, y=0)

        self.label = Label(self.frame, text="Register", font=("Arial", 30,'bold'),bg="black",fg="white")
        self.label.pack(pady=10)

        self.label1 = Label(self.frame, text="Email", font=("Arial", 15),bg="black",fg="white")
        self.label1.pack(pady=10)

        #entry
        self.entry1 = Entry(self.frame, font=("Arial", 15))
        self.entry1.pack(pady=10)

        #name
        self.label2 = Label(self.frame, text="Name", font=("Arial", 15),bg="black",fg="white")
        self.label2.pack(pady=10)

        self.entry2 = Entry(self.frame, font=("Arial", 15))
        self.entry2.pack(pady=10)

        #password
        self.label3 = Label(self.frame, text="Password", font=("Arial", 15),bg="black",fg="white")
        self.label3.pack(pady=10)

        self.entry3 = Entry(self.frame, font=("Arial", 15),show="*")
        self.entry3.pack(pady=10)

        #confirm password
        self.label4 = Label(self.frame, text="Confirm Password", font=("Arial", 15),bg="black",fg="white")
        self.label4.pack(pady=10)

        self.entry4 = Entry(self.frame, font=("Arial", 15))
        self.entry4.pack(pady=10)

        self.button = Button(self.frame, text="Register", font=("Arial", 15), command=self.registersccount)
        self.button.pack(pady=10)

        #login user
        self.button1 = Button(self.frame, text="Login", font=("Arial", 15), command=self.login_screen)
        self.button1.pack(pady=10)


    def registersccount(self):
        email = self.entry1.get()
        password = self.entry3.get()
        name = self.entry2.get()

        #validation
        if password!= self.entry4.get():
            messagebox.showerror("Register", "Passwords do not match")
        elif len(password) < 8:
            messagebox.showerror("Register", "Password must be at least 8 characters long")
        elif len(name) < 5:
            messagebox.showerror("Register", "Name must be at least 5 characters long")
        #password validation
        elif not re.match(r'^[a-zA-Z0-9]+$', name):
            messagebox.showerror("Register", "Name can only contain letters and numbers")
        #email validation
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            messagebox.showerror("Register", "Invalid Email")
        #password validation atleast 1 uppercase, 1 lowercase, 1 number, 1 special character
        elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            messagebox.showerror("Register", "Password must contain at least 1 uppercase, 1 lowercase, 1 number, 1 special character")
        else:
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor = cnx.cursor(buffered=True)

            cursor.execute("SELECT * FROM users WHERE email = '%s'" % (email))
            row = cursor.fetchone()

            if row is not None:
                messagebox.showerror("Register", "Email Already Registered")
            else:
                cursor.execute("INSERT INTO users(name, email, password) VALUES('%s', '%s', '%s')" % (name, email, password))
                cnx.commit()
                messagebox.showinfo("Register", "Register Successfull")
                #back to login page
                self.login_screen()

    def logout(self):
        self.login_screen()
        #back to login pag

    #main menu
    def main_menu(self):
        #destory all widget
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Main Menu")
        self.root.geometry("1100x800")



        #frame
        self.frame = Frame(self.root, width=1100, height=800,bg="black")
        self.frame.place(x=0, y=0,)

                #display bg2 
        self.bgimage = Image.open("images/bg3.png")
        self.bgimage = ImageTk.PhotoImage(self.bgimage)
        self.bglabel = Label(self.frame, image=self.bgimage)
        self.bglabel.image = self.bgimage
        self.bglabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = Label(self.frame, text="Main Menu", font=("Arial", 20),bg="black",fg="white")
        self.label.place(x=500, y=20)

        #logout button top right corner
        self.button1 = Button(self.frame, text="Logout", font=("Arial", 15), command=self.logout)
        self.button1.place(x=1000, y=20)

        #book Travel button
        self.button2 = Button(self.frame, text="Book Travel", font=("Arial", 15), command=self.book_travel)
        self.button2.place(x=50, y=150)


        #Recommendations button light green
        self.button2 = Button(self.frame, text="Recommendations", font=("Arial", 15), command=self.recommendations)
        self.button2.place(x=50, y=100)

        #Explore Destinations button light green
        self.button3 = Button(self.frame, text="Explore Destinations", font=("Arial", 15), command=self.explore_destinations)
        self.button3.place(x=250, y=100)

        #Explore Attractions button
        self.button4 = Button(self.frame, text="Explore Attractions", font=("Arial", 15), command=self.explore_attractions)
        self.button4.place(x=450, y=100)


        #my bookings
        self.button4 = Button(self.frame, text="My Bookings", font=("Arial", 15), command=self.my_bookings)
        self.button4.place(x=650, y=100)

        #contents frame
        self.frame1 = Frame(self.frame, width=1000, height=500,bg="black")
        self.frame1.place(x=50, y=200)

        #open default recommended destinations
        self.recommendations()

    #book_travel
    def book_travel(self):

        self.selected_attractions = []
        
        #frame inside frame
        self.frame2 = Frame(self.frame1, width=1000, height=400, bg ='black')
        self.frame2.place(x=0, y=0)

        #Choose Start Date
        self.label1 = Label(self.frame2, text="Choose Start Date", font=("Arial", 15),bg="black",fg="white")
        self.label1.place(x=50, y=20)

        self.entry1 = DateEntry(self.frame2, font=("Arial", 15))
        self.entry1.place(x=60, y=60)

        #Choose End Date
        self.label2 = Label(self.frame2, text="Choose End Date", font=("Arial", 15),bg="black",fg="white")
        self.label2.place(x=350, y=20)

        self.entry2 = DateEntry(self.frame2, font=("Arial", 15))
        self.entry2.place(x=360, y=60)

        #on left select start Location
        self.label3 = Label(self.frame2, text="Choose Start Location", font=("Arial", 15),bg="black",fg="white")
        self.label3.place(x=700, y=20)

        #locations list
        locations=["India", "USA", "China", "Japan", "Germany", "France", "Italy", "Australia", "Brazil", "Canada", "Mexico", "South Africa", "Egypt", "Russia", "Spain", "United Kingdom", "Thailand", "Turkey", "Greece", "Netherlands", "Switzerland", "Sweden", "Norway", "Denmark", "Finland", "Belgium", "Austria", "Portugal", "Czech Republic", "Ireland", "Poland", "Romania", "Hungary", "Ukraine", "Slovakia", "Croatia", "Bulgaria", "Slovenia", "Lithuania", "Latvia", "Estonia", "Serbia", "Bosnia and Herzegovina", "Montenegro", "Albania", "Macedonia", "Kosovo", "Belarus", "Moldova", "Luxembourg", "Cyprus", "Malta", "Iceland", "Andorra", "Monaco", "Liechtenstein", "San Marino", "Vatican City"]
        self.combobox2 = Combobox(self.frame2, values=locations, font=("Arial", 15))
        self.combobox2.place(x=700, y=60)

        #choose destinations
        self.label3 = Label(self.frame2, text="Choose Destinations", font=("Arial", 15),bg="black",fg="white")
        self.label3.place(x=50, y=100)

        #get all destinations from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT * FROM destinations")
        rows = cursor.fetchall()
        destinations=[]
        for i, row in enumerate(rows):
            destinations.append(row[1])
        self.combobox1 = Combobox(self.frame2, values=destinations, font=("Arial", 15))
        self.combobox1.place(x=60, y=140)
        self.combobox1.bind("<<ComboboxSelected>>", self.book_destinations_id)

        #choose attractions
        self.label4 = Label(self.frame2, text="Choose Attractions", font=("Arial", 15),bg="black",fg="white")
        self.label4.place(x=60, y=200)

        #combobox
        self.combobox3 = Combobox(self.frame2, font=("Arial", 15))
        self.combobox3.place(x=60, y=240)
        self.combobox3.bind("<<ComboboxSelected>>", self.attractions_added)

        #book travel button
        self.button1 = Button(self.frame2, text="Book Travel", font=("Arial", 15), command=self.book_travel_function)
        self.button1.place(x=60, y=330)

        #treeview on left to show added attractions
        self.tree = ttk.Treeview(self.frame2, columns=("Attractions"), show="headings")
        self.tree.heading("Attractions", text="Attractions")
        self.tree.place(x=450, y=130)

    #book_travel_function
    def book_travel_function(self):

        #get data
        start_date = self.entry1.get_date()
        end_date = self.entry2.get_date()
        destinations = self.combobox1.get()
        start_location = self.combobox2.get()

        #frame inside frame1
        self.frame3 = Frame(self.frame1, width=1000, height=500, bg ='black')
        self.frame3.place(x=0, y=0)

        #confirm booking page
        self.label1 = Label(self.frame3, text="Confirm Booking", font=("Arial", 15),bg="black",fg="white")
        self.label1.place(x=50, y=20)

        #Start date Label
        self.label2 = Label(self.frame3, text="Start Date", font=("Arial", 15),bg="black",fg="white")
        self.label2.place(x=50, y=100)

        #start date Label fill with data
        self.label3 = Label(self.frame3, text=start_date, font=("Arial", 15),bg="black",fg="white")
        self.label3.place(x=150, y=100)

        #End date Label
        self.label4 = Label(self.frame3, text="End Date", font=("Arial", 15),bg="black",fg="white")
        self.label4.place(x=350, y=100)

        #end date Label fill with data
        self.label5 = Label(self.frame3, text=end_date, font=("Arial", 15),bg="black",fg="white")
        self.label5.place(x=450, y=100)

        # From + start location +to + destination
        self.label6 = Label(self.frame3, text=" From "+start_location + " to " + destinations, font=("Arial", 15),bg="black",fg="white")
        self.label6.place(x=200, y=150)

        # My Airlines + Round Trip + Price 
        self.label7 = Label(self.frame3, text=" My Airlines Provide Round Trip airlines Service", font=("Arial", 15),bg="black",fg="white")
        self.label7.place(x=100, y=200)

        #count days between start and end date
        days=(end_date-start_date).days

        #total + days + nights + price
        self.label8 = Label(self.frame3, text="Total "+" "+str(days)+" Nights "+" Accomdations at My Motels", font=("Arial", 15),bg="black",fg="white")
        self.label8.place(x=50, y=250)

        #Tourist Guide Include with My Cabs Service
        self.label9 = Label(self.frame3, text="Tourist Guide Include with My Cabs Service", font=("Arial", 15),bg="black",fg="white")
        self.label9.place(x=50, y=300)

        #total 
        self.label10 = Label(self.frame3, text="Total: $10,000 to 34,0000", font=("Arial", 15),bg="black",fg="white")
        self.label10.place(x=50, y=350)

        #Confirm Booking Button
        self.button1 = Button(self.frame3, text="Confirm Booking", font=("Arial", 15), command=self.confirm_booking)
        self.button1.place(x=400, y=400)


    #confirm_booking function
    def confirm_booking(self):
        #get details
        start_date = self.entry1.get_date()
        end_date = self.entry2.get_date()
        start_location = self.combobox2.get()
        destinations = self.combobox1.get()
        self.destinations_id = self.combobox1.get()
        self.selected_attractions = self.selected_attractions

        #validate
        if start_date > end_date:
            messagebox.showerror("Error", "Start Date must be before End Date")
            return
        if start_date == end_date:
            messagebox.showerror("Error", "Start Date and End Date must be different")
            return
        if start_location == destinations:
            messagebox.showerror("Error", "Start Location and Destination must be different")
            return
        if self.selected_attractions == []:
            messagebox.showerror("Error", "Select atleast one attraction")
            return
        if self.destinations_id == 0:
            messagebox.showerror("Error", "Select atleast one destination")
            return
        
        print(self.destinations_id)
        
        #get destination id
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT destinations_id FROM destinations WHERE name = %s", (self.destinations_id,))
        row = cursor.fetchone()
        self.destinations_id = row[0]
        
        #confirm booking
        cursor = cnx.cursor(buffered=True)
        cursor.execute("INSERT INTO booking (user_id,start_date, end_date, start_location, destinations_id) VALUES (%s,%s, %s, %s, %s)", (self.user_id,start_date, end_date, start_location, self.destinations_id))
        cnx.commit()

        #get recent added bookings_id
        cursor.execute("SELECT booking_id FROM booking ORDER BY booking_id DESC LIMIT 1")
        row = cursor.fetchone()
        self.bookings_id = row[0]

        #booked attractions
        for attraction in self.selected_attractions:
            #get attraction id
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor = cnx.cursor(buffered=True)
            cursor.execute("SELECT attractions_id FROM attractions WHERE name = %s", (attraction,))
            row = cursor.fetchone()
            attraction_id = row[0]
            cursor.execute("INSERT INTO booking_attractions (booking_id, attractions_id) VALUES (%s, %s)", (self.bookings_id, attraction_id))
            cnx.commit()

        #messagebox
        messagebox.showinfo("Confirmation", "Booking Confirmed")

        #write to pdf
        pdf=FPDF()
        #writting booking details into pdf 
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(190, 10, 'Booking Details', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(190, 10, 'Booking ID: '+str(self.bookings_id), 0, 1, 'C')
        pdf.cell(190, 10, 'Start Date: '+str(start_date), 0, 1, 'C')
        pdf.cell(190, 10, 'End Date: '+str(end_date), 0, 1, 'C')
        pdf.cell(190, 10, 'Start Location: '+str(start_location), 0, 1, 'C')
        pdf.cell(190, 10, 'Destination: '+str(destinations), 0, 1, 'C')
        #" My Airlines Provide Round Trip airlines Service"
        pdf.cell(190, 10, 'My Airlines Provide Round Trip airlines Service', 0, 1, 'C')
        pdf.cell(190, 10, 'Trip Type : Round Trip', 0, 1, 'C')
        pdf.cell(190, 10, 'Your stay will be organized at My Motels', 0, 1, 'C')
        pdf.cell(190, 10, 'Tourist Guide Included with My Cabs Service', 0, 1, 'C')
        pdf.cell(190, 10, 'Total: $10,000 to 34,0000', 0, 1, 'C')

        #booking confirmed 
        pdf.cell(190, 10, 'Booking Confirmed', 0, 1, 'C')

        #save and open the pdf
        pdf.output(str(self.bookings_id)+'ticket.pdf')
        os.startfile(str(self.bookings_id)+'ticket.pdf')

        #self.my_bookings
        self.my_bookings()

        

    #attractions_added
    def attractions_added(self, event):
        attraction_name = self.combobox3.get()

        #if already added
        if attraction_name in self.selected_attractions:
            messagebox.showinfo("Attractions", "Attractions Already Added")
            return
    
        self.selected_attractions.append(attraction_name)
        
        #fill the treeview from list
        self.tree = ttk.Treeview(self.frame2, columns=("Attractions"), show="headings")
        self.tree.heading("Attractions", text="Attractions")
        self.tree.place(x=450, y=130)
        for i, attraction in enumerate(self.selected_attractions):
            self.tree.insert("", "end", text=attraction, values=(attraction))
        
        #to center
        self.tree.place(x=450, y=130)

        #messagebox
        messagebox.showinfo("Attractions", "Attractions Added")



        
    #book_destinations_id function
    def book_destinations_id(self, event):
        self.destinations_id = self.combobox1.get()

        #get destination id
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT destinations_id FROM destinations WHERE name = '%s'" % (self.destinations_id))
        row = cursor.fetchone()
        self.destinations_id = row[0]


        #get list of attractions from database from destinations_id
        cursor.execute("SELECT * FROM attractions WHERE destinations_id = %s" % (int(self.destinations_id)))
        rows = cursor.fetchall()
        attractions=[]
        for i, row in enumerate(rows):
            attractions.append(row[2])
        self.combobox3.configure(values=attractions)




    


    #explore attractions function similar to explore destinations
    def explore_attractions(self,destinations_id=None):

        #create a canvas in frame1
        self.canvas = Canvas(self.frame1, width=1000, height=400, bg ='black',highlightthickness=0)
        self.canvas.place(x=0, y=0)

        #frame inside in canvas
        self.frame2 = Frame(self.canvas, width=1000, height=400, bg ='black')
        self.frame2.place(x=0, y=0)

        #scrollbar
        self.scrollbar = Scrollbar(self.frame1, command=self.canvas.yview)
        self.scrollbar.place(x=1000, y=0)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.create_window((0, 0), window=self.frame2, anchor="nw")

        self.frame2.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        #get all attractions from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)

        if destinations_id is not None:
            cursor.execute("SELECT * FROM attractions WHERE destinations_id = %s" % (int(destinations_id)))
            rows = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM attractions")
            rows = cursor.fetchall()

        #similar to destinations function
        current=0
        for i, attraction in enumerate(rows):
            attraction = {
                "attraction_id": attraction[0],
                "attraction_name": attraction[2],
                "attraction_image_path": attraction[9]
            }
            image = Image.open(attraction["attraction_image_path"])
            image = image.resize((200, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            attraction_button = Button(self.frame2, image=photo, command=lambda attraction=attraction: self.show_attraction_details_user(attraction))
            attraction_button.image = photo
            attraction_button.grid(row=row, column=col, padx=10, pady=10)
            attraction_name=Label(self.frame2, text=attraction["attraction_name"], font=("Arial", 15), bg="black", fg="white")
            attraction_name.grid(row=row+1 ,column=col, padx=10, pady=10)

            current = i

        cnx.close()

    #show attraction details function
    def show_attraction_details_user(self, attraction):
        attraction_id = attraction["attraction_id"]
        attraction_name = attraction["attraction_name"]
        attraction_image_path = attraction["attraction_image_path"]

        #clear contents frame
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #get attraction details from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT * FROM attractions WHERE attractions_id = %s" % (attraction_id))
        attraction = cursor.fetchone()
        cnx.close()
        
        print(attraction)

        #label attraction details
        self.label = Label(self.frame1, text="Attraction Details", font=("Arial", 20),bg="black",fg="white")
        self.label.place(x=400, y=10)

        #Name
        self.label1 = Label(self.frame1, text="Name", font=("Arial", 15),bg="black",fg="white")
        self.label1.place(x=100, y=100)
        
        self.label1_data = Label(self.frame1, text=attraction[2], font=("Arial", 15),bg="black",fg="white")
        self.label1_data.place(x=330, y=100)

        #country
        self.label2 = Label(self.frame1, text="Country", font=("Arial", 15),bg="black",fg="white")
        self.label2.place(x=100, y=150)
        
        self.label2_data = Label(self.frame1, text=attraction[3], font=("Arial", 15),bg="black",fg="white")
        self.label2_data.place(x=330, y=150)

        #continent
        self.label3 = Label(self.frame1, text="Continent", font=("Arial", 15),bg="black",fg="white")
        self.label3.place(x=100, y=200)
        
        self.label3_data = Label(self.frame1, text=attraction[4], font=("Arial", 15),bg="black",fg="white")
        self.label3_data.place(x=330, y=200)

        #description
        self.label4 = Label(self.frame1, text="Description", font=("Arial", 15),bg="black",fg="white")
        self.label4.place(x=100, y=250)
        
        self.label4_data = Label(self.frame1, text=attraction[5], font=("Arial", 15),bg="black",fg="white")
        self.label4_data.place(x=330, y=250)

        #recommended_duration
        self.label5 = Label(self.frame1, text="Recommended Duration", font=("Arial", 15),bg="black",fg="white")
        self.label5.place(x=100, y=300)

        self.label5_data = Label(self.frame1, text=attraction[7], font=("Arial", 15),bg="black",fg="white")
        self.label5_data.place(x=330, y=300)

        #recommended_day
        self.label6 = Label(self.frame1, text="Recommended Day", font=("Arial", 15),bg="black",fg="white")
        self.label6.place(x=100, y=350)
        
        self.label6_data = Label(self.frame1, text=attraction[8], font=("Arial", 15),bg="black",fg="white")
        self.label6_data.place(x=330, y=350)



        self.image_path = attraction[9]

        self.delete_attraction_id = attraction_id

        #display image
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(self.image)
        self.image_label = Label(self.frame1, image=photo)
        self.image_label.image = photo
        self.image_label.place(x=700, y=100)


        #back button
        self.back_button = Button(self.frame1, text="Back", font=("Arial", 15), command=self.main_menu)
        self.back_button.place(x=600, y=400)

    #my bookings function
    def my_bookings(self):
        #clear the frame    
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #label
        self.label = Label(self.frame1, text="My Bookings", font=("Arial", 20),bg="black",fg="white")
        self.label.place(x=400, y=10)

        #treeview
        self.treeview = ttk.Treeview(self.frame1, columns=("ID","From", "To", "Start Date", "End Date", "Status"), show="headings")
        self.treeview.pack(fill="both", expand=True)
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("From", text="From")
        self.treeview.heading("To", text="To")
        self.treeview.heading("Start Date", text="Start Date")
        self.treeview.heading("End Date", text="End Date")
        self.treeview.heading("Status", text="Status")
        self.treeview.place(x=100, y=100)
        self.treeview.column("ID", width=130,anchor="center")
        self.treeview.column("From", width=130,anchor="center")
        self.treeview.column("To", width=130,anchor="center")
        self.treeview.column("Start Date", width=130,anchor="center")
        self.treeview.column("End Date", width=130,anchor="center")
        self.treeview.column("Status", width=130,anchor="center")

        #get data from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT * FROM booking")
        rows = cursor.fetchall()
        for row in rows:
            start=row[2]
            end=row[3]
            #get destination details from database
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor=cnx.cursor(buffered=True)
            cursor.execute("SELECT * FROM destinations WHERE destinations_id = %s" % (row[3]))
            destination = cursor.fetchone()
            #close
            cnx.close()

            self.treeview.insert("", "end", values=(row[0],start, destination[1], row[4], row[5], "Pending"))

        #back button
        self.back_button = Button(self.frame1, text="Back", font=("Arial", 15), command=self.main_menu)
        self.back_button.place(x=600, y=350)

        #Cancel booking
        self.cancel_button = Button(self.frame1, text="Cancel Booking", font=("Arial", 15), command=self.cancel_booking)
        self.cancel_button.place(x=400, y=350)


    #cancel booking function
    def cancel_booking(self):
        #get data from selection
        booking_id = self.treeview.item(self.treeview.focus(),"values")[0]

        #check if booking
        if booking_id:

            #delete from booking_attractions table
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor = cnx.cursor(buffered=True)
            #delete from bookings_attractions table
            cursor.execute("DELETE FROM booking_attractions WHERE booking_id = %s" % (booking_id))

            cursor.execute("DELETE FROM booking WHERE booking_id = %s" % (booking_id))
            cnx.commit()
            cnx.close()

            #display message
            messagebox.showinfo("Success", "Booking Cancelled")
            self.main_menu()
        else:
            messagebox.showerror("Error", "Please select a booking")




    #explore destinations function
    def explore_destinations(self):
        

        #create a canvas in frame1
        self.canvas = Canvas(self.frame1, width=1000, height=400, bg ='black',highlightthickness=0)
        self.canvas.place(x=0, y=0)

        #frame inside in canvas
        self.frame2 = Frame(self.canvas, width=1000, height=400, bg ='black')
        self.frame2.place(x=0, y=0)

        #scrollbar
        self.scrollbar = Scrollbar(self.frame1, command=self.canvas.yview)
        self.scrollbar.place(x=1000, y=0)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.create_window((0, 0), window=self.frame2, anchor="nw")

        self.frame2.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        #get all destinations from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)

        cursor.execute("SELECT * FROM destinations")
        rows = cursor.fetchall()

        current_i = 0
        for i, destination in enumerate(rows):
            # display destination image as button
            destination = list(destination)
            destination = {
                "destination_id": destination[0],
                "destination_name": destination[1],
                "destination_image_path": destination[6]
            }
            image = Image.open(destination["destination_image_path"])
            image = image.resize((200, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = i // 6
            col = i % 6

            destination_button = Button(self.frame2, image=photo, command=lambda destination=destination: self.show_destination_details_user(destination))
            destination_button.image = photo
            destination_button.grid(row=row, column=col, padx=10, pady=10)
            destination_name = Label(self.frame2, text=destination["destination_name"], font=("Arial", 15), bg="black", fg="white")
            destination_name.grid(row=row+1, column=col, padx=10, pady=10)
            current_i = i

        cnx.close()

    #show_destination_details_user function
    def show_destination_details_user(self, destination):
        
        destination_id = destination["destination_id"]

        #get destination details from database
        cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT * FROM destinations WHERE destinations_id = %s" % (destination_id))
        destination = cursor.fetchone()
        cnx.close()



        #clear contents frame
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #label destination details
        self.label = Label(self.frame1, text="Destination Details", font=("Arial", 20),bg="black",fg="white")
        self.label.place(x=400, y=10)

        #Name
        self.label1 = Label(self.frame1, text="Name", font=("Arial", 15),bg="black",fg="white")
        self.label1.place(x=100, y=100)
        
        self.label1_value = Label(self.frame1, text=destination[1], font=("Arial", 15),bg="black",fg="white")
        self.label1_value.place(x=320, y=100)

        #country
        self.label2 = Label(self.frame1, text="Country", font=("Arial", 15),bg="black",fg="white")
        self.label2.place(x=100, y=150)
        
        self.label2_value = Label(self.frame1, text=destination[2], font=("Arial", 15),bg="black",fg="white")
        self.label2_value.place(x=320, y=150)

        #continent
        self.label3 = Label(self.frame1, text="Continent", font=("Arial", 15),bg="black",fg="white")
        self.label3.place(x=100, y=200)

        self.label3_value = Label(self.frame1, text=destination[3], font=("Arial", 15),bg="black",fg="white")
        self.label3_value.place(x=320, y=200)

        #description
        self.label4 = Label(self.frame1, text="Description", font=("Arial", 15),bg="black",fg="white")
        self.label4.place(x=100, y=250)

        self.label4_value = Label(self.frame1, text=destination[4], font=("Arial", 15),bg="black",fg="white")
        self.label4_value.place(x=320, y=250)

        #recommended duration
        self.label5 = Label(self.frame1, text="Recommended Duration", font=("Arial", 15),bg="black",fg="white")
        self.label5.place(x=100, y=300)

        self.label5_value = Label(self.frame1, text=destination[5], font=("Arial", 15),bg="black",fg="white")
        self.label5_value.place(x=320, y=300)



        self.image_path=destination[6]

        #display image 
        image = Image.open(destination[6])
        image = image.resize((200, 250), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        attraction_button = Button(self.frame1, image=photo)
        attraction_button.image = photo
        attraction_button.place(x=700, y=100)

        self.delete_destination_id=destination_id


        #back button
        self.button2 = Button(self.frame1, text="Back", font=("Arial", 15), command=self.main_menu)
        self.button2.place(x=330, y=350)

        #go into attraction details
        self.button3 = Button(self.frame1, text="Attractions", font=("Arial", 15), command=lambda destination=destination: self.explore_attractions(destination[0]))
        self.button3.place(x=400, y=350)




    #recommendations function
    def recommendations(self):
          #clear contents frame
        for widget in self.frame1.winfo_children():
            widget.destroy()

        #display destinations from recommendation destinations

        #create a canvas in frame1
        self.canvas = Canvas(self.frame1, width=1000, height=400, bg ='black',highlightthickness=0)
        self.canvas.place(x=0, y=0)

        #frame inside in canvas
        self.frame2 = Frame(self.canvas, width=1000, height=400, bg ='black')
        self.frame2.place(x=0, y=0)

        #scrollbar
        self.scrollbar = Scrollbar(self.frame1, command=self.canvas.yview)
        self.scrollbar.place(x=1000, y=0)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.frame2, anchor="nw")
        self.frame2.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        #get data from recommended_destinations list

        current=0
        for row in self.recommended_destinations:
            destination_id = row["destination_id"]

            #get data from table
            cnx = mysql.connector.connect(host='localhost', user='root', passwd='Niharika@408', database='tp')
            cursor = cnx.cursor(buffered=True)
            cursor.execute('''SELECT * FROM destinations WHERE destinations_id = %s''', (destination_id,))
            row = cursor.fetchone()
            cursor.close()

            destination = list(row)
            destination = {
                "destination_id": destination[0],
                "destination_name": destination[1],
                "destination_image_path": destination[6]
            }

            image = Image.open(destination["destination_image_path"])
            image = image.resize((200, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            row = current // 6
            col = current % 6

            destination_button = Button(self.frame2, image=photo, command=lambda destination=destination: self.show_destination_details_user(destination))
            destination_button.image = photo
            destination_button.grid(row=row, column=col, padx=10, pady=10)
            destination_name = Label(self.frame2, text=destination["destination_name"], font=("Arial", 15), bg="black", fg="white")
            destination_name.grid(row=row+1, column=col, padx=10, pady=10)
            current += 1




    

    

if __name__ == "__main__":
    tp=tp()
    tp.root.mainloop()
