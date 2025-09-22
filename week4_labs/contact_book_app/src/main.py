import flet as ft
import re
from database import init_db
from app_logic import display_contacts, add_contact

def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 600
    page.scroll= ft.ScrollMode.AUTO

    db_conn = init_db()

    name_input = ft.TextField(label="Name", width=350, prefix_icon=ft.Icons.PERSON,)
    phone_input = ft.TextField(label="Phone",width=350, prefix_icon=ft.Icons.PHONE,)
    email_input = ft.TextField(label="Email", width=350, prefix_icon=ft.Icons.EMAIL,)
    
    inputs = (name_input, phone_input, email_input)

    contacts_list_view = ft.ListView(spacing=10, auto_scroll=False)
    contacts_container = ft.Container(content=contacts_list_view, height=300)

    search_field = ft.TextField(
        label="Search Contacts",
        on_change=lambda e: display_contacts(page, contacts_list_view, db_conn, search_field.value)
    )

    def handle_add(e):
        has_error = False

        if not name_input.value.strip():
            name_input.error_text = "Name cannot be empty."
            has_error = True
        else:
            name_input.error_text = None

        if not phone_input.value.strip():
            phone_input.error_text = "Phone cannot be empty."
            has_error = True
        else:
            phone_input.error_text = None


        if not email_input.value.strip():
            email_input.error_text = "Email cannot be empty."
            has_error = True
        else:
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(pattern, email_input.value):
                email_input.error_text = "Invalid email format."
                has_error = True
            else:
                email_input.error_text = None
        
        page.update()


        if has_error:
            return

        add_contact(page, inputs, contacts_list_view, db_conn)

    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=handle_add
    )
    

#for dark modeee
    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if theme_switch.value else ft.ThemeMode.LIGHT

        )
        page.update()


    theme_switch = ft.Switch(label="Dark Mode", on_change=theme_changed)

    toggle_container = ft.Container(
        content=theme_switch,
        alignment=ft.alignment.top_right,
        scale=0.8
    )

    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Contact Book", size=30, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=theme_switch,
                            alignment=ft.alignment.center_right,
                            scale=0.8
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,),

                ft.Text("Enter Contact Details:", size=20, weight=ft.FontWeight.BOLD),
                name_input,
                phone_input,
                email_input,
                add_button,
                        
                ft.Divider(),
                ft.Text("Contacts:", size=20, weight=ft.FontWeight.BOLD),
                search_field,
                contacts_container,
            ],
            expand = False,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    display_contacts(page, contacts_list_view, db_conn)

if __name__ == "__main__":
    ft.app(target=main)