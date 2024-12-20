# Importing libraries
from contextlib import nullcontext
from distutils.command.clean import clean
from http.client import responses
from urllib import response
import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
import os
import string
import pathlib
import textwrap
import time
import requests
import spacy
import wikipedia

# Function to connect to the database and print error or success
def DB_Connect():    
    # Defining db info
    hostname = "wzx.h.filess.io"
    database = "nlpdb_tobaccosum"
    port = "3307"
    username = "nlpdb_tobaccosum"
    password = "8bb9dbad1e1f5b0f4d1fbbfac09c50427e8d5f7d"

    # Try to connect if error print error
    try:
        connection = mysql.connector.connect(host=hostname, database=database, user=username, password=password, port=port)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)

# Function to insert a user into the db for login
def insert_user(connection, username, password, email, full_name, age, Canvas):
    try:
        cursor = connection.cursor()
        query_user = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query_user, (username, password))
        connection.commit()
        user_id = cursor.lastrowid
        
        query_user_info = "INSERT INTO user_info (user_id, email, full_name, age) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_user_info, (user_id, email, full_name, age))
        connection.commit()
        Canvas.create_text(400, 600, text='Account Created!', font=lower_font, fill='green')
        return 'Account Created!'
    except Error as e:
        print("Error inserting user:", e)
        Canvas.create_text(400, 600, text=e, font=lower_font, fill='red')

# Function to verify if password and username correct
def VerifyUser(connection, username, password):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        if user:
            print("User verified successfully")
            return True
        else:
            print("Invalid username or password")
            return False
    except Error as e:
        print("Error verifying user:", e)
        return False

# Function to get the name of user
def get_full_name_by_username(connection, username):
    try:
        cursor = connection.cursor()
        # Query to get user ID using username
        query_user_id = "SELECT id FROM users WHERE username = %s"
        cursor.execute(query_user_id, (username,))
        user_id = cursor.fetchone()
        if user_id:
            # Query to get full name using user ID
            query_full_name = "SELECT full_name FROM user_info WHERE user_id = %s"
            cursor.execute(query_full_name, (user_id[0],))
            full_name = cursor.fetchone()
            if full_name:
                return full_name[0]
            else:
                print("Full name not found for the user")
                return None
        else:
            print("User not found")
            return None
    except Error as e:
        print("Error fetching user info:", e)
        return None

# Function to draw main menu canvas elements
def draw_menu():
    Canvas = ClearGUI()

    waiting_meeting = "0"

    # Display the resized background image on the canvas
    Canvas.create_image(0, 0, anchor="nw", image=background)

    # Display the resized logo image on the canvas
    Canvas.create_image(30, 30, anchor="nw", image=logo)

    # Display title text in canvas with font 
    Canvas.create_text(400, 250, text="Assistify", font=title_font, anchor="center", fill='black')

    # Display lower text in canvas
    Canvas.create_text(400, 300, text="Assistance made easy.", font=lower_font, anchor="center", fill='black')
    
    # Create the submit button on the canvas
    LoginButton = Button(Canvas, text='Login', command=Login, **button_style)
    Canvas.create_window(400, 400, window=LoginButton)
    
    RegisterButton = Button(Canvas, text='Register', command=Register, **button_style)
    Canvas.create_window(400, 500, window=RegisterButton)

# Function to run when login button pressed
def Login():
    Canvas = ClearGUI()
    
    # Create labels and entries on the canvas
    Canvas.create_text(350, 200, text='Username:', font=lower_font, fill='black')
    username_entry = Entry(Canvas, font=('calibre', 10, 'normal'))
    Canvas.create_window(500, 200, window=username_entry)

    Canvas.create_text(350, 250, text='Password:', font=lower_font, fill='black')
    password_entry = Entry(Canvas, font=('calibre', 10, 'normal'), show='*')
    Canvas.create_window(500, 250, window=password_entry)
    
    # Display title text in canvas with font 
    Canvas.create_text(400, 100, text="Login", font=title_font, anchor="center", fill='black')
    
    # Define the function to be called when the button is clicked
    def submit():
        username = username_entry.get()
        password = password_entry.get()
        ValidUser = VerifyUser(DB_Connection, username, password)
        if ValidUser == True:
            Canvas.create_text(400, 600, text='Login Successful!', font=lower_font, fill='green')
            FirstTime = False
            DrawChatbot(DB_Connection, username)
        else:
            Canvas.create_text(400, 600, text='Username or password incorrect!', font=lower_font, fill='red')
    
    # Create the submit button on the canvas
    submit_button = Button(Canvas, text='Submit', command=submit, **button_style)
    Canvas.create_window(400, 300, window=submit_button)
    
    back_button = Button(Canvas, text='Back', command=draw_menu, **button_style, anchor="center")
    Canvas.create_window(400, 400, window=back_button, anchor="center")
    
# Function to run when register button is pressed
def Register():
    # Clear GUI and save canvas
    Canvas = ClearGUI()
    
    # Create labels and entries on the canvas
    Canvas.create_text(350, 150, text='Username*:', font=lower_font, fill='black')
    username_entry = Entry(Canvas, font=('calibre', 10, 'normal'))
    Canvas.create_window(500, 150, window=username_entry)

    Canvas.create_text(350, 200, text='Password*:', font=lower_font, fill='black')
    password_entry = Entry(Canvas, font=('calibre', 10, 'normal'), show='*')
    Canvas.create_window(500, 200, window=password_entry)

    Canvas.create_text(350, 250, text='Email:', font=lower_font, fill='black')
    email_entry = Entry(Canvas, font=('calibre', 10, 'normal'))
    Canvas.create_window(500, 250, window=email_entry)

    Canvas.create_text(350, 300, text='Age:', font=lower_font, fill='black')
    age_entry = Entry(Canvas, font=('calibre', 10, 'normal'))
    Canvas.create_window(500, 300, window=age_entry)

    Canvas.create_text(350, 350, text='Name*:', font=lower_font, fill='black')
    name_entry = Entry(Canvas, font=('calibre', 10, 'normal'))
    Canvas.create_window(500, 350, window=name_entry)

    # Define the function to be called when the button is clicked
    def submit():
        # Retrieve values from entry widgets
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        age = age_entry.get()
        name = name_entry.get()

        # Check if username, password, and name are not empty
        if username == "":
            print("Username cannot be empty")
            return
        if password == "":
            print("Password cannot be empty")
            return
        if name == "":
            print("Name cannot be empty")
            return
        if not name.isalpha():
            print("Name must not contain numebers or special characters")
            return
        # If all fields are nont empty, proceed with user registration
        insert_status = insert_user(DB_Connection, username, password, email, name, age, Canvas)
        if insert_status == 'Account Created!':
            FirstTime = True
            DrawChatbot(FirstTime, username)
    
    # Create the submit button on the canvas
    submit_button = Button(Canvas, text='Submit', command=submit, **button_style)
    Canvas.create_window(400, 400, window=submit_button)
    
    back_button = Button(Canvas, text='Back', command=draw_menu, **button_style)
    Canvas.create_window(400, 450, window=back_button)

# Function to draw main chatbot
def DrawChatbot(FirstTime, Username):

    Canvas = ClearGUI()
    Canvas.create_text(400, 600, text='Chatbot', font=lower_font, fill='#FF0000')
    
    # Create the submit button on the Canvas
    Logout_button = Button(Canvas, text='Logout', command=draw_menu, **button_style)

    Canvas.create_window(750, 50, window=Logout_button)
       
    # Create a frame for the chat box
    chat_frame = tk.Frame(Canvas, bg="white", width=800, height=800)
    Canvas.create_window(500, 400, window=chat_frame, anchor="center")

    # Create a Text widget to display messages
    chat_box = tk.Text(chat_frame, width=50, height=20, wrap=tk.WORD, font=("Helvetica", 12), bg="white", fg="black", 
                       insertbackground="black", borderwidth=2, relief=tk.SOLID, padx=5, pady=5)
    chat_box.pack(padx=10, pady=10)

    # Create a scrollbar for the Text widget
    scrollbar = tk.Scrollbar(chat_frame, command=chat_box.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Text widget to use the scrollbar
    chat_box.config(yscrollcommand=scrollbar.set)

    # Create an entry widget to input messages
    entry = tk.Entry(chat_frame, width=50)
    entry.pack(padx=10, pady=5)
    
    # Set text widget to be bold
    chat_box.tag_configure("bold", font=("Helvetica", 12, "bold"))
    
    # Display informative message in box 
    chat_box.insert(tk.END, f"Type your first message in the box below to begin conversation...\n")
    
    if FirstTime == True:
        chat_box.insert(tk.END, f"Assistant: Hi! Welcome to Assistify. How can I help you?\n", "bold")
    else:
        chat_box.insert(tk.END, f"Assistant: Hi! Welcome back. How can I help you today?\n", "bold")
    # When sending a message
    def send_message(event=None):
        # Get the message from the entry box
        message = entry.get()
        
        # If there is a message
        if message:
            # display your message to the chatbox
            chat_box.insert(tk.END, f"You: {message}\n")
            entry.delete(0, tk.END)

            response = GetResponse(DB_Connection, Username, message, chat_box)

            # Display bot message in chatbox
            chat_box.insert(tk.END, f"Assistant: "+response+"\n", "bold")
            
            # Auto-scroll to the end of the chat box for easy use
            chat_box.see(tk.END)
            
    # Bind the <Return> key to the send_message function
    entry.bind("<Return>", send_message)
    
    # Create a button to send messages
    send_button = tk.Button(chat_frame, text="Send", command=send_message, **button_style)
    send_button.pack(side=tk.RIGHT, padx=(10, 5), pady=5)

# Function to get a response once a user sends a message
def GetResponse(DB_Connection, Username, message, chat_box):
    global waiting_meeting, MeetingTime, MeetingDate, MeetingNote
    
    RealName = get_full_name_by_username(DB_Connection, Username)

    Message = message.lower()
    CleanMessage = remove_punctuation(Message)

    # Perform named entity recognition (NER) using spaCy
    doc = nlp(CleanMessage)

    # Custom list of locations
    custom_locations = ["auckland", "christchurch", "hamilton", "tauranga", "lower hutt", "dunedin", "napier"]

    # Split the message into words
    words = CleanMessage.lower().split()

    locations = []
    for ent in doc.ents:
        if ent.label_ == "GPE":
            locations.append(ent.text.lower())

    # Check if any custom locations are mentioned in the message
    for word in CleanMessage.split():
        if word in custom_locations:
            locations.append(word.lower())
    if waiting_meeting == "1":
        MeetingTime = CleanMessage
        response = "Great. What date is the meeting? (YY/MM/DD)"
        waiting_meeting = "2"
    elif waiting_meeting == "2":
        MeetingDate = CleanMessage
        response = "Perfect, any notes you want to make for the meeting?"
        waiting_meeting = "3"
    elif waiting_meeting == "3":
        if "no" == CleanMessage:
            response = "No notes. Meeting created"
            waiting_meeting = "0"
            MeetingNote = "None"
        else:
            response = "Notes updated. Meeting created"
            MeetingNote = CleanMessage
        response = CreateMeeting(MeetingTime, MeetingDate, MeetingNote, Username, DB_Connection)
        waiting_meeting = "0"
    
    elif locations:
        # Choose the first location mentioned for simplicity
        location = locations[0]
        response = get_weather_update(location.capitalize(), api_key)
    elif "weather" in CleanMessage:
        response = "Sure, which city do you want the weather for?"
    elif CleanMessage in ["hello", "hi", "hey"]:
        response = "Hello, " + RealName + ". How can I help you today?"
    elif "search" in words or "summarize" in words:
        # Find the index of the command word
        command_index = words.index("search") if "search" in words else words.index("summarize")
    
        # Extract the subject which is the words after the command word
        subject = " ".join(words[command_index + 1:])
    
        # Get the summary for the subject
        response = get_first_sentence_summary(subject)
    
    elif "meeting" in CleanMessage and "create" in CleanMessage:
        if waiting_meeting == "0":
            response = "Sure I will create a meeting for you. What time is that for? (24-hr time hh:mm:ss)"
            waiting_meeting = "1"
    elif "meeting" in CleanMessage and "view" in CleanMessage:
            response = GetRecentMeetingsAsString(Username, DB_Connection)
    else:
        response = "I'm not sure what you mean? Could you explain more"
        print(waiting_meeting)
    
    PreviousCache = CleanMessage
    
    return response

# Function to create a meeting
def CreateMeeting(MeetingTime, MeetingDate, MeetingNote, Username, connection):
    UserID = GetUserID(Username, connection)
    print("Creating Meeting")
    try:
        cursor = connection.cursor()
        # Query to insert meeting details into the meetings table
        query_meeting = "INSERT INTO meetings (`meeting-time`, `meeting-date`, `meeting-note`, `user_id`) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_meeting, (MeetingTime, MeetingDate, MeetingNote, UserID))
        connection.commit()
        print("Meeting created successfully")
        return 'Meeting created successfully'
    except Error as e:
        error_message = str(e) 
        print("Error creating meeting:", error_message)
        if "date" in error_message:
            error_message = "Oops, looks like you entered the wrong date format. (YY/MM/DD)"
        elif "time" in error_message:
            error_message = "Oops, looks like you entered the wrong time format. (HH:MM:SS)"
        return error_message  

# Function to get the meeting details and retirn them as a string
def GetRecentMeetingsAsString(Username, connection):
    try:
        cursor = connection.cursor()

        # Get the user ID for the given username
        UserID = GetUserID(Username, connection)

        # Query to get the 5 most recent meetings for the user
        query_recent_meetings = "SELECT `meeting-id`, `meeting-time`, `meeting-date`, `meeting-note` FROM meetings WHERE user_id = %s ORDER BY `meeting-date` DESC, `meeting-time` DESC LIMIT 5"
        cursor.execute(query_recent_meetings, (UserID,))
        
        # Fetch all rows from the result set
        recent_meetings = cursor.fetchall()
        
        # Close cursor
        cursor.close()

        if not recent_meetings:
            return "No recent meetings found."
        else:
            meetings_string = ""
            for meeting in recent_meetings:
                meetings_string += f"Meeting ID: {meeting[0]}, Date: {meeting[2]}, Time: {meeting[1]}, Note: {meeting[3]}\n"
            return meetings_string
    except Error as e:
        error_message = "Error fetching recent meetings: " + str(e)
        print(error_message)
        return error_message

# Function to get wikipedia summary
def get_first_sentence_summary(topic):
    try:
        # Search for the topic on Wikipedia
        search_results = wikipedia.search(topic)

        if not search_results:
            return "No matching topics found."

        # Get the summary of the first search result
        summary = wikipedia.summary(search_results[0])

        # Split the summary based on punctuation to get the first sentence
        first_sentence = summary.split(".")[0]

        output = "First sentence summary of " + search_results[0] + ": " + first_sentence
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation pages
        output = "Disambiguation page encountered. Please provide a more specific topic."
    except wikipedia.exceptions.PageError as e:
        # Handle page not found errors
        output = "Page not found. Please check the topic and try again."
    except Exception as e:
        # Handle other exceptions
        output = "An error occurred: " + str(e)
    return output

# Removes functuation
def remove_punctuation(text):
    # Create a translation table to map punctuation characters to None
    translator = str.maketrans('', '', string.punctuation)
    
    # Use translate() method to remove punctuation
    cleaned_text = text.translate(translator)
    
    return cleaned_text

# Function to get the user id from username
def GetUserID(Username, connection):
    try:
        cursor = connection.cursor()
        # Query to get user ID using username
        query_user_id = "SELECT id FROM users WHERE username = %s"
        cursor.execute(query_user_id, (Username,))
        user_id = cursor.fetchone()
        if user_id:
            print(user_id[0])
            return user_id[0]  # Return user ID
        else:
            print("User not found")
            return None
    except Error as e:
        print("Error fetching user info:", e)
        return None

# Function to get the weather update from requests
def get_weather_update(location, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The weather in {location} is {weather_description} with a temperature of {temperature}\u00b0C."
    else:
        return "Failed to fetch weather data."

# Clears the GUI elements and draws a new canvas with essential elements like logo
def ClearGUI():
    # Clear existing content
    for widget in Window.winfo_children():
        widget.destroy()
    
    canvas = Canvas(Window, bg="black", width=1920, height=1080)
    canvas.pack()

    # Display the resized background image on the canvas
    canvas.create_image(0, 0, anchor="nw", image=background)

    # Display the resized logo image on the canvas
    canvas.create_image(30, 30, anchor="nw", image=logo)
    return canvas

# Main function where code runs from
if __name__ == '__main__':
    # key
    api_key = '082c66d7b07f386c7cb0bd56b7f539b1'
    
    global waiting_meeting
    waiting_meeting = "0"

    # Load spacy English language model
    nlp = spacy.load("en_core_web_sm")
    
    # Create a custom font for title
    title_font = ("Helvetica", 34)
    
    # Create a custom font for smaller text with font Helvetica and size of 18
    lower_font = ("Helvetica", 20)
    
    # Style for buttons
    button_style = {
        'bg': '#B3C8CF',        # Background color
        'fg': 'white',       # Text color
        'font': ('Helvetica', 12),  # Font
        'relief': 'ridge',  # Button border style
        'borderwidth': 1,    # Border width     
        'height': 2          # Button height
    }
    
    # Define image locations
    logo1 = 'images/assitify.png'
    background = 'images/background.png'
    
    # Resize images 
    original_image = Image.open(logo1)
    resized_image = original_image.resize((200, 200))
    
    # Resize images
    original_image22 = Image.open(background)
    background_img = original_image22.resize((1920, 1080))
    
    # Making main window, naming it and setting size
    Window = Tk()
    Window.title("Assistify")
    Window.geometry("800x800")

    # Set the window icon
    Window.iconbitmap("images/logoicon.ico")

    # Convert images to PhotoImage objects
    background = ImageTk.PhotoImage(background_img)
    logo = ImageTk.PhotoImage(resized_image)
    
    print("Loading DB...")
    
    # Establish Connection to DB
    DB_Connection = DB_Connect()
    
    # Draw menu
    draw_menu()
    
    # Begin mainloop
    Window.mainloop()
       
    if DB_Connection.is_connected():
        DB_Connection.close()
        print("MySQL connection is closed")