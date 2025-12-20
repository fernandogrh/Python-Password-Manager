from tkinter import messagebox
from random import shuffle, randint, choice
import pyperclip
import json
from tkinter import *



def create_password():
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
               "V",
               "W", "X", "Y", "Z", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
               'r',
               's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["@", "§", "&", "%", "?", "!", "(", ")"]
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def save():
    password = password_entry.get()
    website = website_entry.get().strip()
    email = email_entry.get().strip()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(password) == 0 or len(email) == 0 or len(website) == 0:
        messagebox.showinfo(title="Oops", message=f"Please make sure you haven't left any fields empty")

    elif "@" not in email:
        messagebox.showinfo(title="Oops", message=f"Please enter a valid email")

    elif len(password) < 6:
        messagebox.showinfo(title="Oops", message=f"Your password must be at least 6 characters long")

    else:
        is_ok = messagebox.askokcancel(
            title=website,
            message=f"These are the details entered:\n\nEmail: {email}\nPassword: {password}\n\nDo you want to save?")
        if not is_ok:
            return
        else: 
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
    
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
    
            else:
                data.update(new_data)
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
    
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                email_entry.delete(0, END)


def find_website():
    desired_website = website_entry.get().strip().lower()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if desired_website in data:
            email = data[desired_website]["email"]
            password = data[desired_website]["password"]
            messagebox.showinfo(title=desired_website, message=f"Email: {email}\nPassword: {password}")

        else:
            messagebox.showinfo(title="Error", message=f"No results for {desired_website}")


def get_default_email():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return ""
    emails = [site["email"] for site in data.values() if "email" in site]
    if not emails:
        return ""
    return max(set(emails), key=emails.count)

# MAIN module
window = Tk()
window.title(" FR Password Manager")
window.config(padx=50, pady=50)

canva = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canva.create_image(150, 150, image=logo_image)
canva.grid(row=0, column=1)


website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)



website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, get_default_email())
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

generate_password_button = Button(text="Generate Password", command=create_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", width=13, command=find_website)
search_button.grid(row=1, column=2)

window.mainloop()

