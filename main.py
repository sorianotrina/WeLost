from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemLeadingIcon, MDListItemSupportingText, \
    MDListItemTertiaryText
from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

from datetime import datetime

from db import db, ItemsDb
from model import ItemsModel

class CustomIconButton(MDIconButton):
    def __init__(self, icon, style, theme_icon_color, icon_color, items, btn_pressed, app_root, **kwargs):
        super(CustomIconButton, self).__init__(**kwargs)
        self.icon = icon
        self.style = style
        self.theme_icon_color = theme_icon_color
        self.icon_color = icon_color
        self.items = items
        self.btn_pressed = btn_pressed
        self.app_root = app_root

    def on_release(self):
        if self.btn_pressed in ["update_lost", "update_found"]:
            self.on_update_btn_pressed()
        else:
            self.on_archive_btn_pressed()

    def on_update_btn_pressed(self):
        print("update button pressed")

    def on_archive_btn_pressed(self):
        print("archive button pressed")


class CustomIconButtonLost(CustomIconButton):
    def __init__(self, icon, style, theme_icon_color, icon_color, lost_items, btn_pressed, app_root, **kwargs):
        super(CustomIconButtonLost, self).__init__(icon, style, theme_icon_color, icon_color, lost_items, btn_pressed, app_root, **kwargs)
        self.items = lost_items

    def on_release(self):
        if self.btn_pressed == "update_lost":
            self.on_update_btn_lost_pressed()
        else:
            self.on_archive_btn_lost_pressed()

    def on_update_btn_lost_pressed(self):
        print(f"update button pressed: {self.items.id}")
        self.app_root.current = "update_lost_screen"
        self.app_root.get_screen("update_lost_screen").ids.u_lost_id.text = str(self.items.id)
        self.app_root.get_screen("update_lost_screen").ids.u_lost_student_number.text = str(self.items.student_number)
        self.app_root.get_screen("update_lost_screen").ids.u_lost_name.text = self.items.name
        self.app_root.get_screen("update_lost_screen").ids.u_lost_description.text = self.items.description
        self.app_root.get_screen("update_lost_screen").ids.u_lost_date.text = self.items.date
        self.app_root.get_screen("update_lost_screen").ids.u_lost_location.text = self.items.location
        self.app_root.get_screen("update_lost_screen").ids.u_lost_contact.text = str(self.items.contact)
        self.app_root.get_screen("update_lost_screen").ids.u_lost_status.text = self.items.status

    def on_archive_btn_lost_pressed(self):
        if db.archive_lost_item_by_id(self.items.id):
            if hasattr(self.app_root, 'load_items'):
                self.app_root.load_items()
                self.app_root.current = "admin_screen"

class CustomIconButtonFound(CustomIconButton):
    def __init__(self, icon, style, theme_icon_color, icon_color, found_items, btn_pressed, app_root, **kwargs):
        super(CustomIconButtonFound, self).__init__(icon, style, theme_icon_color, icon_color, found_items, btn_pressed, app_root, **kwargs)
        self.items = found_items

    def on_release(self):
        if self.btn_pressed == "update_found":
            self.on_update_btn_found_pressed()
        else:
            self.on_archive_btn_found_pressed()

    def on_update_btn_found_pressed(self):
        print(f"update button pressed: {self.items.id}")
        self.app_root.current = "update_found_screen"
        self.app_root.get_screen("update_found_screen").ids.u_found_id.text = str(self.items.id)
        self.app_root.get_screen("update_found_screen").ids.u_found_student_number.text = str(self.items.student_number)
        self.app_root.get_screen("update_found_screen").ids.u_found_name.text = self.items.name
        self.app_root.get_screen("update_found_screen").ids.u_found_description.text = self.items.description
        self.app_root.get_screen("update_found_screen").ids.u_found_date.text = self.items.date
        self.app_root.get_screen("update_found_screen").ids.u_found_location.text = self.items.location
        self.app_root.get_screen("update_found_screen").ids.u_found_contact.text = str(self.items.contact)
        self.app_root.get_screen("update_found_screen").ids.u_found_status.text = self.items.status

    def on_archive_btn_found_pressed(self):
        if db.archive_found_item_by_id(self.items.id):
            if hasattr(self.app_root, 'load_items_found'):
                self.app_root.load_items_found()
                self.app_root.current = "found_screen"


class MainScreen(MDScreen):
    pass

class LoginScreen(MDScreen):
    pass

class AdminLoginScreen(MDScreen):
    pass

class StudentScreen(MDScreen):
    pass

class AdminScreen(MDScreen):
    pass

class FoundScreen(MDScreen):
    pass

class UpdateLostScreen(MDScreen):
    pass

class UpdateFoundScreen(MDScreen):
    pass

class DashboardScreen(MDScreen):
    pass

class WindowManager(MDScreenManager):
    pass

class WeLostApp(MDApp):
    def build(self):
        return Builder.load_file("welost.kv")

    def on_start(self):
        self.load_items()
        self.load_items_db()
        self.load_items_found()
        self.load_items_found_db()
        self.update_dashboard()

    def show_date_picker(self, focus):
        if not focus:
            return
        date_dialog = MDModalDatePicker()
        date_dialog.bind(on_ok=self.on_ok, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_ok(self, instance):
        dt = str(instance.get_date()[0])

        self.root.get_screen("student_screen").ids.date.text = dt
        instance.dismiss()

    def on_cancel(self, instance):
        instance.dismiss()

    def report_lost_item(self):
        student_number = self.root.get_screen("student_screen").ids.student_number
        name = self.root.get_screen("student_screen").ids.name
        description = self.root.get_screen("student_screen").ids.description
        date = self.root.get_screen("student_screen").ids.date
        location = self.root.get_screen("student_screen").ids.location
        status = self.root.get_screen("student_screen").ids.status
        contact = self.root.get_screen("student_screen").ids.contact

        today = datetime.today().strftime("%Y-%M-%D %H:%M:%S")

        if student_number.text != "" and name.text != "" and description.text != "" and date.text != "" and location.text != "" and contact.text != "":
            payload = {
                "student_number": student_number.text,
                "name": name.text,
                "description": description.text,
                "date": date.text,
                "location": location.text,
                "contact": contact.text,
                "status": status.text,
                "updated": today
            }

            res = db.insert_lost_item(list(payload.values()))

            if res:
                self.show_success_lost()

                student_number.text = ""
                name.text = ""
                description.text = ""
                date.text = ""
                location.text = ""
                contact.text = ""
                status.text = ""

                self.load_items()
                self.load_items_db()
                self.update_dashboard()

    def load_items(self):
        items = db.select_all_lost_items_a()
        lost_item_list = self.root.get_screen("admin_screen").ids.lost_item_list
        lost_item_list.clear_widgets()

        if len(items) > 0:
            for item in items:
                row: ItemsModel = ItemsModel(*item)
                if row.archived:
                    continue

                lost_items = MDListItem(
                    MDListItemLeadingIcon(
                        icon="account-circle"
                    ),
                    MDListItemHeadlineText(
                        text=f"({row.id}) Item Description: {row.description} | Status: {row.status}",
                    ),
                    MDListItemSupportingText(
                        text=f"Student Number: {row.student_number} | Name: {row.name} | Contact: {row.contact}",
                    ),
                    MDListItemTertiaryText(
                        text=f"Date Lost: {row.date} at {row.location}"
                    )
                )

                update_btn_lost = CustomIconButtonLost(
                    icon="pencil",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(0, 0, 0, 1),
                    btn_pressed="update_lost",
                    lost_items=row,
                    app_root=self.root
                )

                archive_btn_lost = CustomIconButtonLost(
                    icon="archive",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(1, 0, 0, 1),
                    btn_pressed="archive_lost",
                    lost_items=row,
                    app_root=self.root
                )
                gl = MDGridLayout(
                    cols=2,
                    adaptive_width=True,
                )
                gl.add_widget(update_btn_lost)
                gl.add_widget(archive_btn_lost)
                lost_items.add_widget(gl)
                lost_item_list.add_widget(lost_items)

        else:
            lost_item_list.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text="No reported lost item."
                    )
                )
            )

    def load_items_db(self):
        items = db.select_all_lost_items()
        lost_item_list_db = self.root.get_screen("dashboard_screen").ids.lost_item_list_db
        lost_item_list_db.clear_widgets()

        if len(items) > 0:
            for item in items:
                row: ItemsModel = ItemsModel(*item)
                lost_items = MDListItem(
                    MDListItemLeadingIcon(
                        icon="account-circle"
                    ),
                    MDListItemHeadlineText(
                        text=f"({row.id}) Item Description: {row.description} | Status: {row.status}",
                    ),
                    MDListItemSupportingText(
                        text=f"Student Number: {row.student_number} | Name: {row.name} | Contact: {row.contact}",
                    ),
                    MDListItemTertiaryText(
                        text=f"Date Lost: {row.date} at {row.location}"
                    )
                )

                lost_item_list_db.add_widget(lost_items)

        else:
            lost_item_list_db.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text="No reported lost item."
                    )
                )
            )

    def search_value_lost(self, search_text):
        results = db.search_engine_lost(search_text)
        lost_item_list = self.root.get_screen("admin_screen").ids.lost_item_list
        lost_item_list.clear_widgets()

        if results:
            for item in results:
                row = ItemsModel(*item)
                lost_items = MDListItem(
                    MDListItemLeadingIcon(
                        icon="account-circle"
                    ),
                    MDListItemHeadlineText(
                        text=f"({row.id}) Item Description: {row.description} | Status: {row.status}",
                    ),
                    MDListItemSupportingText(
                        text=f"Student Number: {row.student_number} | Name: {row.name} | Contact: {row.contact}",
                    ),
                    MDListItemTertiaryText(
                        text=f"Date Lost: {row.date} at {row.location}"
                    )
                )
                update_btn_lost = CustomIconButtonLost(
                    icon="pencil",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(0, 0, 0, 1),
                    btn_pressed="update_lost",
                    lost_items=row,
                    app_root=self.root
                )

                archive_btn_lost = CustomIconButtonLost(
                    icon="archive",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(1, 0, 0, 1),
                    btn_pressed="archive_lost",
                    lost_items=row,
                    app_root=self
                )
                gl = MDGridLayout(
                    cols=2,
                    adaptive_width=True,
                )
                gl.add_widget(update_btn_lost)
                gl.add_widget(archive_btn_lost)
                lost_items.add_widget(gl)
                lost_item_list.add_widget(lost_items)
        else:
            lost_item_list.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text="No results found."
                    )
                )
            )

    def update_status_lost(self):
        id = self.root.get_screen("update_lost_screen").ids.u_lost_id
        student_number = self.root.get_screen("update_lost_screen").ids.u_lost_student_number
        name = self.root.get_screen("update_lost_screen").ids.u_lost_name
        description = self.root.get_screen("update_lost_screen").ids.u_lost_description
        date = self.root.get_screen("update_lost_screen").ids.u_lost_date
        location = self.root.get_screen("update_lost_screen").ids.u_lost_location
        contact = self.root.get_screen("update_lost_screen").ids.u_lost_contact
        status = self.root.get_screen("update_lost_screen").ids.u_lost_status

        today = datetime.today().strftime("%Y-%M-%D %H:%M:%S")

        if id.text != "" and student_number.text != "" and name.text != "" and description.text != "" and date.text != "" and location.text != "" and contact.text != "":
            payload = {
                "student_number": student_number.text,
                "name": name.text,
                "description": description.text,
                "date": date.text,
                "location": location.text,
                "contact": contact.text,
                "status": status.text,
                "updated": today,
                "id": int(id.text),
            }

            # UPDATE QUERY RETURNS A BOOLEAN VALUE
            res = db.update_lost_item_by_id(list(payload.values()))

            if res:
                id.text = ""
                student_number.text = ""
                name.text = ""
                description.text = ""
                date.text = ""
                location.text = ""
                contact.text = ""
                status.text = ""

                self.load_items()
                self.load_items_db()
                self.update_dashboard()

                self.root.current = "admin_screen"

    def archive_lost(self, lost_items):
        if db.archive_lost_item_by_id(lost_items.id):
            self.load_items()

    def report_found_item(self):
        student_number = self.root.get_screen("student_screen").ids.student_number
        name = self.root.get_screen("student_screen").ids.name
        description = self.root.get_screen("student_screen").ids.description
        date = self.root.get_screen("student_screen").ids.date
        location = self.root.get_screen("student_screen").ids.location
        status = self.root.get_screen("student_screen").ids.status
        contact = self.root.get_screen("student_screen").ids.contact

        today = datetime.today().strftime("%Y-%M-%D %H:%M:%S")

        if student_number.text != "" and name.text != "" and description.text != "" and date.text != "" and location.text != "" and contact.text != "":
            payload = {
                "student_number": student_number.text,
                "name": name.text,
                "description": description.text,
                "date": date.text,
                "location": location.text,
                "contact": contact.text,
                "status": status.text,
                "updated": today
            }

            res = db.insert_found_item(list(payload.values()))
            self.show_success_found()

            if res:
                student_number.text = ""
                name.text = ""
                description.text = ""
                date.text = ""
                location.text = ""
                contact.text = ""

                self.load_items_found()
                self.load_items_found_db()
                self.update_dashboard()

    def load_items_found(self):
        items = db.select_all_found_items_a()
        found_item_list = self.root.get_screen("found_screen").ids.found_item_list
        found_item_list.clear_widgets()

        if len(items) > 0:
            for item in items:
                row: ItemsModel = ItemsModel(*item)
                if row.archived:
                    continue

                found_items = MDListItem(
                    MDListItemLeadingIcon(
                        icon="account-circle"
                    ),
                    MDListItemHeadlineText(
                        text=f"({row.id}) Item Description: {row.description} | Status: {row.status}",
                    ),
                    MDListItemSupportingText(
                        text=f"Student Number: {row.student_number} | Name: {row.name} | Contact: {row.contact}",
                    ),
                    MDListItemTertiaryText(
                        text=f"Date Found: {row.date} at {row.location}"
                    )
                )

                update_btn_found = CustomIconButtonFound(
                    icon="pencil",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(0, 0, 0, 1),
                    btn_pressed="update_found",
                    found_items=row,
                    app_root=self.root
                )

                archive_btn_found = CustomIconButtonFound(
                    icon="archive",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(1, 0, 0, 1),
                    btn_pressed="archive_found",
                    found_items=row,
                    app_root=self
                )
                gl = MDGridLayout(
                    cols=2,
                    adaptive_width=True,
                )
                gl.add_widget(update_btn_found)
                gl.add_widget(archive_btn_found)
                found_items.add_widget(gl)
                found_item_list.add_widget(found_items)

        else:
            found_item_list.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text="No reported found item."
                    )
                )
            )

    def load_items_found_db(self):
        items = db.select_all_found_items()
        found_item_list_db = self.root.get_screen("dashboard_screen").ids.found_item_list_db
        found_item_list_db.clear_widgets()

        if len(items) > 0:
            for item in items:
                row: ItemsModel = ItemsModel(*item)
                found_items = MDListItem(
                    MDListItemLeadingIcon(
                        icon="account-circle"
                    ),
                    MDListItemHeadlineText(
                        text=f"({row.id}) Item Description: {row.description} | Status: {row.status}",
                    ),
                    MDListItemSupportingText(
                        text=f"Student Number: {row.student_number} | Name: {row.name} | Contact: {row.contact}",
                    ),
                    MDListItemTertiaryText(
                        text=f"Date Lost: {row.date} at {row.location}"
                    )
                )

                found_item_list_db.add_widget(found_items)

        else:
            found_item_list_db.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text="No reported lost item."
                    )
                )
            )

    def search_value_found(self, search_term):
        results = db.search_engine_found(search_term)
        found_item_list = self.root.get_screen("found_screen").ids.found_item_list
        found_item_list.clear_widgets()

        if results:
            for item in results:
                row = ItemsModel(*item)
                found_items = MDListItem(
                    MDListItemLeadingIcon(
                        icon="account-circle"
                    ),
                    MDListItemHeadlineText(
                        text=f"({row.id}) Item Description: {row.description} | Status: {row.status}",
                    ),
                    MDListItemSupportingText(
                        text=f"Student Number: {row.student_number} | Name: {row.name} | Contact: {row.contact}",
                    ),
                    MDListItemTertiaryText(
                        text=f"Date Lost: {row.date} at {row.location}"
                    )
                )
                update_btn_found = CustomIconButtonFound(
                    icon="pencil",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(0, 0, 0, 1),
                    btn_pressed="update_found",
                    found_items=row,
                    app_root=self.root
                )

                archive_btn_found = CustomIconButtonFound(
                    icon="archive",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(1, 0, 0, 1),
                    btn_pressed="archive_found",
                    found_items=row,
                    app_root=self
                )
                gl = MDGridLayout(
                    cols=2,
                    adaptive_width=True,
                )
                gl.add_widget(update_btn_found)
                gl.add_widget(archive_btn_found)
                found_items.add_widget(gl)
                found_item_list.add_widget(found_items)
        else:
            found_item_list.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text="No results found."
                    )
                )
            )

    def update_status_found(self):
        id = self.root.get_screen("update_found_screen").ids.u_found_id
        student_number = self.root.get_screen("update_found_screen").ids.u_found_student_number
        name = self.root.get_screen("update_found_screen").ids.u_found_name
        description = self.root.get_screen("update_found_screen").ids.u_found_description
        date = self.root.get_screen("update_found_screen").ids.u_found_date
        location = self.root.get_screen("update_found_screen").ids.u_found_location
        contact = self.root.get_screen("update_found_screen").ids.u_found_contact
        status = self.root.get_screen("update_found_screen").ids.u_found_status

        today = datetime.today().strftime("%Y-%M-%D %H:%M:%S")

        if id.text != "" and student_number.text != "" and name.text != "" and description.text != "" and date.text != "" and location.text != "" and contact.text != "":
            payload = {
                "student_number": student_number.text,
                "name": name.text,
                "description": description.text,
                "date": date.text,
                "location": location.text,
                "contact": contact.text,
                "status": status.text,
                "updated": today,
                "id": int(id.text),
            }

            # UPDATE QUERY RETURNS A BOOLEAN VALUE
            res = db.update_found_item_by_id(list(payload.values()))

            if res:
                id.text = ""
                student_number.text = ""
                name.text = ""
                description.text = ""
                date.text = ""
                location.text = ""
                contact.text = ""
                status.text = ""

                self.load_items_found()
                self.load_items_found_db()
                self.update_dashboard()

                self.root.current = "found_screen"

    def archive_found(self, found_items):
        if db.archive_found_item_by_id(found_items.id):
            self.load_items_found()

    def validate_admin_login(self):
        email = self.root.get_screen("admin_login_screen").ids.admin_email
        password = self.root.get_screen("admin_login_screen").ids.admin_password

        # Dummy validation
        if email.text == "admin@example.com" and password.text == "admin123":
            self.root.current = "admin_screen"
        else:
            self.show_error_popup()

    def show_error_popup(self):
        content = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 10
    spacing: 10

    MDLabel:
        text: "Invalid email or password. Please try again."
        font_style: "Title"
        font_size: 100
        halign: 'center'
        size_hint_y: None
        height: self.texture_size[1]
        text_color: (255/255, 255/255, 255/255, 1)
        
    Widget:
        size_hint_y: None
        height: dp(20)

    MDButton:
        text: 'Try Again'
        size_hint_y: None
        height: 40
        on_release: app.try_again()
        theme_text_color: "Custom"
        text_color: (1, 1, 1, 1)
        md_bg_color: (1, 0, 0, 1)
        pos_hint: {"center_x": .5, "center_y": .5}

        MDButtonText:
            theme_text_color: "Custom"
            text_color: (0, 0, 0, 1)
            text: "Try Again"
            halign: "center"
        
    Widget:
        size_hint_y: None
        height: dp(20)
''')

        self.popup = Popup(title="Error", content=content, size_hint=(0.4, 0.3), auto_dismiss=False)
        self.popup.background_color = (1, 0, 0, 1)
        self.popup.open()

    def show_success_lost(self):
        content = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 10
    spacing: 10

    MDLabel:
        text: "Lost item reported successfully!"
        font_style: "Title"
        font_size: 100
        halign: 'center'
        size_hint_y: None
        height: self.texture_size[1]
        text_color: (255/255, 255/255, 255/255, 1)

    Widget:
        size_hint_y: None
        height: dp(20)

    MDButton:
        text: 'OK'
        size_hint_y: None
        height: 40
        on_release: app.ok_lost()
        theme_text_color: "Custom"
        text_color: (1, 1, 1, 1)
        md_bg_color: (1, 0, 0, 1)
        pos_hint: {"center_x": .5, "center_y": .5}

        MDButtonText:
            theme_text_color: "Custom"
            text_color: (0, 0, 0, 1)
            text: "OK"
            halign: "center"

    Widget:
        size_hint_y: None
        height: dp(20)
''')
        self.popup = Popup(title="Success", content=content, size_hint=(0.4, 0.3), auto_dismiss=False)
        self.popup.background_color = (1, 0, 0, 1)
        self.popup.open()

    def show_success_found(self):
        content = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 10
    spacing: 10
    
    MDLabel:
        text: "Found item reported successfully!"
        font_style: "Title"
        font_size: 100
        halign: 'center'
        size_hint_y: None
        height: self.texture_size[1]
        text_color: (255/255, 255/255, 255/255, 1)
    
    Widget:
        size_hint_y: None
        height: dp(20)
    
    MDButton:
        text: 'OK'
        size_hint_y: None
        height: 40
        on_release: app.ok_found()
        theme_text_color: "Custom"
        text_color: (1, 1, 1, 1)
        md_bg_color: (1, 0, 0, 1)
        pos_hint: {"center_x": .5, "center_y": .5}
    
        MDButtonText:
            theme_text_color: "Custom"
            text_color: (0, 0, 0, 1)
            text: "OK"
            halign: "center"
    
    Widget:
        size_hint_y: None
        height: dp(20)
    ''')
        self.popup = Popup(title="Success", content=content, size_hint=(0.4, 0.3), auto_dismiss=False)
        self.popup.background_color = (1, 0, 0, 1)
        self.popup.open()

    def try_again(self):
        email = self.root.get_screen("admin_login_screen").ids.admin_email
        password = self.root.get_screen("admin_login_screen").ids.admin_password
        email.text = ""
        password.text = ""
        self.popup.dismiss()

    def ok_lost(self):
        self.popup.dismiss()
        self.load_items()
        self.load_items_db()
        self.update_dashboard()

    def ok_found(self):
        self.popup.dismiss()
        self.load_items_found()
        self.load_items_found_db()
        self.update_dashboard()

    def log_out(self):
        email = self.root.get_screen("admin_login_screen").ids.admin_email
        password = self.root.get_screen("admin_login_screen").ids.admin_password
        email.text = ""
        password.text = ""

    def get_total_claimed_items(self):
        return db.claimed_lost_item()

    def get_total_unclaimed_items(self):
        return db.unclaimed_lost_item()

    def get_total_claimed_items_f(self):
        return db.claimed_found_item()

    def get_total_unclaimed_items_f(self):
        return db.unclaimed_found_item()

    def get_total_lost(self):
        total_claimed = self.get_total_claimed_items()
        total_unclaimed = self.get_total_unclaimed_items()
        return total_claimed + total_unclaimed

    def get_total_found(self):
        total_claimed_f = self.get_total_claimed_items_f()
        total_unclaimed_f = self.get_total_unclaimed_items_f()
        return total_claimed_f + total_unclaimed_f

    def update_dashboard(self):
        total_claimed = self.get_total_claimed_items()
        total_unclaimed = self.get_total_unclaimed_items()
        total_claimed_f = self.get_total_claimed_items_f()
        total_unclaimed_f = self.get_total_unclaimed_items_f()
        total_lost = self.get_total_lost()
        total_found = self.get_total_found()

        self.root.get_screen("dashboard_screen").ids.total_claimed.text = f"{total_claimed}"
        self.root.get_screen("dashboard_screen").ids.total_unclaimed.text = f"{total_unclaimed}"
        self.root.get_screen("dashboard_screen").ids.total_lost.text = f"{total_lost}"
        self.root.get_screen("dashboard_screen").ids.total_claimed_f.text = f"{total_claimed_f}"
        self.root.get_screen("dashboard_screen").ids.total_unclaimed_f.text = f"{total_unclaimed_f}"
        self.root.get_screen("dashboard_screen").ids.total_found.text = f"{total_found}"


if __name__ == '__main__':
    WeLostApp().run()