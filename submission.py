import smtplib
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Label Submission Automator")
root.geometry("500x500")
root.configure(bg='#242424')
root.option_add('*Background', '#242424')
root.option_add('*Foreground', 'white')
root.option_add('*Font', 'Helvetica 10')


def on_closing():
    messagebox.showinfo("INFO", "Tool Created By TakumoZero [TK0] \n Spotify: TakumoZero")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

def update_email_list():
    selected_emails.clear()  # Clear the current list
    for email, var in zip(emails, vars):
        if var.get() == 1:
            selected_emails.append(email)
    print("Selected Emails:", selected_emails)



emails = [
    "vinicius@vyrusrecords.com",
    "submissions@tribaltrap.com",
    "Demo@MagicMusic.io",
    "demo@polarisrecords.net",
    "demo@aurorianrecords.com",
    "demo@houseofphonk.com",
    "etherealdreamsrecords@gmail.com",
    "contact.bassdarkness@gmail.com"
]

labels = [
    "VYRUS Records",
    "Tribal Trap",
    "Magic Music",
    "Polaris",
    "Aurorian Records",
    "House of Phonk",
    "Etheral Dreams",
    "Bass Darkness"
]

vars = []
row_index = 2  # Start row index for checkboxes
col_index = 0

for i, label in enumerate(labels):
    var = tk.IntVar()
    checkbox = tk.Checkbutton(root, text=label, variable=var, command=update_email_list)
    checkbox.grid(row=row_index, column=col_index, sticky="w", padx=50, pady=5)
    vars.append(var)
    
    # Update column and row index
    col_index += 1
    if col_index > 1:
        col_index = 0
        row_index += 1

# Label for the subject entry
songname_label = tk.Label(root, text="Song Name: ")
songname_label.place(x=63, y=180)

# Entry widget for the subject
songname_entry = tk.Entry(root, width=20)
songname_entry.place(x=30, y=200)


artists_label = tk.Label(root, text="Artist/s (Seperate multilple with comma): ")
artists_label.place(x=228, y=180)

# Entry widget for the subject
artists_entry = tk.Entry(root, width=33)
artists_entry.place(x=230, y=200)


message_label = tk.Label(root, text="Message: ")
message_label.place(x=228, y=250)

# Entry widget for the subject
message_entry = tk.Text(root, height=5, width=62)
message_entry.place(x=30, y=280)

selected_emails = []


def submit():
    message_content = message_entry.get("1.0", tk.END)
    final_message = message_content.strip()
    errorlevel = 0
    if len(selected_emails) == 0:
        errorlevel += 1
        messagebox.showwarning("Error", "No E-Mail Selected!")

    if songname_entry.get() == "":
        errorlevel += 1
        messagebox.showwarning("Error", "No Song Name entered!")

    if artists_entry.get() == "":
        errorlevel += 1
        messagebox.showwarning("Error", "No Artist(s) entered!")

    if final_message == "":
        errorlevel += 1
        messagebox.showwarning("Error", "No Message entered!")

    if email_entry.get() == "":
        errorlevel += 1
        messagebox.showwarning("Error", "No E-Mail adress entered!")

    if not email_entry.get().endswith("@gmail.com"):
        errorlevel += 1
        messagebox.showwarning("Error", "Use a gmail adress (@gmail.com)!")

    if errorlevel < 1: 
        try:   
            server = smtplib.SMTP("smtp.gmail.com", 587)
            text = f"Subject: {"Demo Sumbission: " + " " + songname_entry.get()+" " + " - " + " " + artists_entry.get()}\n\n{final_message}"
            server.starttls()
            server.login(email_entry.get(), auth_code_entry.get())
            for mail in selected_emails:
                server.sendmail(email_entry.get(), mail, text)
            messagebox.showinfo("Success", "Email(s) send look into your inbox!\n\n\n")
        except Exception as e:
            log_file_path = "log.txt"
            try:   
                messagebox.showwarning("Error", "An Error occured check the log file!")
                with open(log_file_path, "w") as log_file:
                    log_file.write(f"{e}")
                    # Ensure the message is flushed to the file
                    log_file.flush()
            except Exception as file_error:
                # Print file operation errors to the console
                print(f"An error occurred while writing to the log file: {file_error}")
            

# Label for the subject entry
email_label = tk.Label(root, text="Your E-Mail: ")
email_label.place(x=83, y=380)

# Entry widget for the subject
email_entry = tk.Entry(root, width=25)
email_entry.place(x=30, y=400)

auth_code_label = tk.Label(root, text="Google App Code: ")
auth_code_label.place(x=290, y=380)

# Entry widget for the subject
auth_code_entry = tk.Entry(root, width=33)
auth_code_entry.place(x=230, y=400)

submit_button = tk.Button(root, text="Submit", width=10, command=submit)
submit_button.place(x=210, y=450)

root.mainloop()