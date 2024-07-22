from sys import exit
from tkinter import messagebox
from customtkinter import *
import subprocess
import requests
import json


class App(CTk):
    """
    Subclass of CTk, needed to create app window (Unnecessary actually, but it was easier for me)
    It is possible to write app = CTk()
    """
    def __init__(self):
        super().__init__()


class BaseFrame(CTkFrame):
    """
    Subclass of CTkFrame, needed to show which frame is the main one and how to return to it from the other.
    Also simplifies code structure.
    """
    def __init__(self, root, main):
        super().__init__(root, fg_color='transparent')
        self.root = root
        self.root.title('AppTap')
        self.main = main
        self.scroll = CTkScrollableFrame(self, width=500)
        self.checkboxes = []

    def to_main_frame(self):
        self.pack_forget()
        self.main.pack()

    def create_checkboxes(self, option):
        if option == 1:
            self.checkboxes = create_install_checkboxes(self.scroll)
            self.scroll.grid(pady=20)
        if option == 2:
            self.checkboxes = create_edit_checkboxes(self.scroll)
            self.scroll.grid(pady=20)


class InstallFrame(BaseFrame):
    """
    Subclass of BaseFrame, needed to create install frame
    """
    def __init__(self, root, main):
        super().__init__(root, main)
        self.create_checkboxes(option=1)

        self.button_frame = CTkFrame(self, fg_color='transparent')
        self.button_frame.grid()

        self.button1 = CTkButton(self.button_frame, text='Install', command=install)
        self.button1.grid(pady=15)

        self.button2 = CTkButton(self.button_frame, text='Return', command=self.to_main_frame)
        self.button2.grid()


class EditFrame(BaseFrame):
    """
    Subclass of BaseFrame, needed to create edit frame
    """
    def __init__(self, root, main):
        super().__init__(root, main)
        self.create_checkboxes(option=2)

        self.button_frame = CTkFrame(self, fg_color='transparent')
        self.button_frame.grid()

        self.button1 = CTkButton(self.button_frame, text='Add new', command=addition)
        self.button1.grid(pady=15)

        self.button2 = CTkButton(self.button_frame, text='Delete selected', command=deletion)
        self.button2.grid()

        self.button3 = CTkButton(self.button_frame, text='Return', command=self.to_main_frame)
        self.button3.grid(pady=15)


class SettingsFrame(BaseFrame):
    """
    Subclass of BaseFrame, needed to create settings frame
    """
    def __init__(self, root, main):
        super().__init__(root, main)

        self.button_frame = CTkFrame(self, fg_color='transparent')
        self.button_frame.grid(pady=50)

        self.button1 = CTkButton(self.button_frame, text='Change theme', command=change_appearance_mode)
        self.button1.grid(pady=15)

        self.button3 = CTkButton(self.button_frame, text='Return', command=self.to_main_frame)
        self.button3.grid(pady=15)


class BaseCheckbox:
    """
    As this app has dynamic amount of the checkboxes, regulated by user, we need to create class, which will help in
    changing checkboxes in real time (without reloading app)
    """
    def __init__(self, name, var, frame):
        self.var = var
        self.name = name
        self.frame = frame

    # .json files serve as databases
    def handle_install_checkbox_selection(self):
        with open('Data/User_install.json', 'r') as u:
            user = json.load(u)

        if self.var.get() == 1:
            user[self.name] = "True"
        else:
            user[self.name] = "False"

        with open('Data/User_install.json', 'w') as u:
            json.dump(user, u)

    def handle_edit_checkbox_selection(self):
        with open('Data/User_edit.json', 'r') as u:
            user = json.load(u)

        if self.var.get() == 1:
            user[self.name] = "True"
        else:
            user[self.name] = "False"

        with open('Data/User_edit.json', 'w') as u:
            json.dump(user, u)


class DerivedInstallCheckbox(BaseCheckbox):
    """
    Created specially for install frame
    """
    def __init__(self, name, var, frame):
        super().__init__(name, var, frame)
        self.checkbox = CTkCheckBox(self.frame, text=self.name, variable=self.var,
                                    command=self.handle_install_checkbox_selection)
        self.checkbox.grid(pady=5)


class DerivedEditCheckbox(BaseCheckbox):
    """
    Created specially for edit frame
    """
    def __init__(self, name, var, frame):
        super().__init__(name, var, frame)
        self.checkbox = CTkCheckBox(self.frame, text=self.name, variable=self.var,
                                    command=self.handle_edit_checkbox_selection)
        self.checkbox.grid(pady=5)


def window_options():

    window_width = 800
    window_height = 400
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    app.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    app.iconbitmap(default='Data/logo.ico')


def appearance_mode():

    with open('Data/Settings.json', 'r') as s:
        settings = json.load(s)

    mode = settings["Theme"]
    set_appearance_mode(mode)


def change_appearance_mode():   # If user changed the theme once, do it to save it

    with open('Data/Settings.json', 'r') as s:
        settings = json.load(s)

    mode = get_appearance_mode()
    if mode == 'Dark':
        set_appearance_mode('Light')
        settings["Theme"] = "Light"
    else:
        set_appearance_mode('Dark')
        settings["Theme"] = "Dark"

    with open("Data/Settings.json", "w") as s:
        json.dump(settings, s)


def main_frame_buttons():

    def to_install_frame():
        main_frame.pack_forget()
        install_frame.pack()

    def to_edit_frame():
        main_frame.pack_forget()
        edit_frame.pack()

    def to_settings_frame():
        main_frame.pack_forget()
        settings_frame.pack()

    main_button_frame = CTkFrame(main_frame, fg_color='transparent')
    main_button_frame.pack(pady=70)

    button_m1 = CTkButton(main_button_frame, text="Install", command=to_install_frame)
    button_m1.pack(pady=15)

    button_m2 = CTkButton(main_button_frame, text="Edit apps", command=to_edit_frame)
    button_m2.pack(pady=15)

    button_m3 = CTkButton(main_button_frame, text="Settings", command=to_settings_frame)
    button_m3.pack(pady=15)

    button_m4 = CTkButton(main_button_frame, text="EXIT", command=exit)
    button_m4.pack(pady=15)


def create_install_checkboxes(frame_name):

    with open('Data/Links.json', 'r') as l_:
        links = json.load(l_)

    with open('Data/User_install.json', 'r') as u:
        user = json.load(u)

    checkboxes = []     # This list is needed to change the amount of checkboxes in real time

    for app1 in links.keys():
        for app2 in user.keys():

            if app1 == app2:

                if user[app2] == "True":
                    checkbox = DerivedInstallCheckbox(name=app2, frame=frame_name, var=IntVar(value=1))
                    checkboxes.append(checkbox)
                elif user[app2] == "False":
                    checkbox = DerivedInstallCheckbox(name=app2, frame=frame_name, var=IntVar(value=0))
                    checkboxes.append(checkbox)
                else:
                    messagebox.showerror("Error", "An error occurred in database")

    return checkboxes


def create_edit_checkboxes(frame_name):

    with open('Data/Links.json', 'r') as l_:
        links = json.load(l_)

    with open('Data/User_edit.json', 'r') as u:
        user = json.load(u)

    checkboxes = []     # This list is needed to change the amount of checkboxes in real time

    for app1 in links.keys():
        for app2 in user.keys():

            if app1 == app2:

                if user[app2] == "True":
                    checkbox = DerivedEditCheckbox(name=app2, frame=frame_name, var=IntVar(value=1))
                    checkboxes.append(checkbox)
                elif user[app2] == "False":
                    checkbox = DerivedEditCheckbox(name=app2, frame=frame_name, var=IntVar(value=0))
                    checkboxes.append(checkbox)
                else:
                    messagebox.showerror("Error", "An error occurred in database")

    return checkboxes


def install():

    def choose_download_path():
        path = filedialog.askdirectory()
        if path:
            return path
        else:
            messagebox.showerror("Error", "Please select a download path.")

    def path_combiner(path, app_):
        c_p = path.format(str) + '/' + (app_ + '_installer.exe')
        return c_p

    def download_file(url, path):
        try:
            response = requests.get(url)
            with open(path, "wb") as f:
                f.write(response.content)

            ask = messagebox.askyesno("What to do?", f"{app_name} download complete! Installer saved at: "
                                                     f"{user_path}\nStart it?")
            return ask
        except requests.exceptions.MissingSchema:
            messagebox.showerror(title='Error', message=f'{app_name} download link invalid')

    def install_file(path):
        process = subprocess.Popen([path])
        process.wait()

    with open('Data/User_install.json', 'r') as u:
        user = json.load(u)

    with open('Data/Links.json', 'r') as l_:
        links = json.load(l_)

    user_path = choose_download_path()
    for item in user.items():
        if item[1] == "True":
            app_name = item[0]
            download_url = links[app_name]
            final_path = path_combiner(user_path, app_name)
            reply = download_file(download_url, final_path)
            if reply:
                install_file(final_path)


def addition():     # If user needs to add new app

    with open('Data/Links.json', 'r') as l_:
        links = json.load(l_)

    app_name = CTkInputDialog(title='App name', text='Enter app name:').get_input()
    app_link = CTkInputDialog(title='App link', text='Enter download link:').get_input()

    reply = messagebox.askyesno("Addition", f"Is it correct?\n{app_name}: {app_link}")
    if reply:
        links.update({f"{app_name}": f"{app_link}"})

        with open('Data/Links.json', 'w') as l_:
            json.dump(links, l_)

        sync(option=1)
        destroy_old_checkboxes()
        install_frame.create_checkboxes(option=1)
        edit_frame.create_checkboxes(option=2)


def deletion():     # If user needs to delete an app

    reply = messagebox.askyesno("Deletion", f"Are you sure?")
    if reply:

        with open('Data/User_edit.json', 'r') as u_e:
            user = json.load(u_e)

        new_user = {}

        for item in user.items():
            if item[1] == "False":
                new_user.update({item[0]: item[1]})

        with open('Data/User_edit.json', 'w') as u_e:
            json.dump(new_user, u_e)

        sync(option=2)
        destroy_old_checkboxes()
        install_frame.create_checkboxes(option=1)
        edit_frame.create_checkboxes(option=2)


def sync(option):   # Renew databases after user's changes

    with open('Data/Links.json', 'r') as l_:
        links = json.load(l_)
    with open('Data/User_install.json', 'r') as u_i:
        user_install = json.load(u_i)
    with open('Data/User_edit.json', 'r') as u_e:
        user_edit = json.load(u_e)

    if option == 1:  # For addition()
        for app_name in links.keys():
            if app_name in user_install.keys():
                pass
            else:
                user_install.update({f"{app_name}": "False"})
            if app_name in user_edit.keys():
                pass
            else:
                user_edit.update({f"{app_name}": "False"})

    if option == 2:  # For deletion()
        links_keys = []
        user_install_keys = []
        for key in links.keys():
            links_keys.append(key)
        for key in user_install.keys():
            user_install_keys.append(key)

        for app_name in links_keys:
            if app_name in user_edit.keys():
                pass
            else:
                links.pop(app_name)
        for app_name in user_install_keys:
            if app_name in user_edit.keys():
                pass
            else:
                user_install.pop(app_name)

    with open('Data/Links.json', 'w') as l_:
        json.dump(links, l_)
    with open('Data/User_install.json', 'w') as u_i:
        json.dump(user_install, u_i)
    with open('Data/User_edit.json', 'w') as u_e:
        json.dump(user_edit, u_e)


def destroy_old_checkboxes():
    """
    When you address to checkbox in checkboxes list once (checkbox.destroy()), method destroy() won't work, as we
    created custom class for checkbox and didn't mention destroy().
    But within our custom class we used CTkCheckBox(), which has got method destroy().
    Therefore, to reach method destroy(), we need to address to checkbox twice.
    How it is actually looks: our_custom_class_checkbox.CTkCheckbox.destroy()
    """
    for checkbox in install_frame.checkboxes:
        checkbox.checkbox.destroy()
    for checkbox in edit_frame.checkboxes:
        checkbox.checkbox.destroy()


app = App()         # Create App window using App class (subclass of customtkinter)

# Make the app window look different from default
window_options()
appearance_mode()   # Can be changed by user

# Create and add the main frame of the app (main menu)
main_frame = CTkFrame(app, fg_color='transparent')
# If fg_color='not transparent', the color of the main frame will be different from the app window one
main_frame.pack()
main_frame_buttons()

# Create other frames using their classes
install_frame = InstallFrame(app, main_frame)

edit_frame = EditFrame(app, main_frame)

settings_frame = SettingsFrame(app, main_frame)

app.mainloop()  # Let the app work until user close it
