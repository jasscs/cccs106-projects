import flet as ft
import mysql.connector
from db_connection import connect_db

def main(page: ft.Page):
    #counter = ft.Text("0", size=50, data=0)
    page.window.center()
    page.window.frameless = True

    page.title = "User Login"
    page.vertical_alignment = 

    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)
        counter.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=increment_click
    )
    page.add(
        ft.SafeArea(
            ft.Container(
                counter,
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )


ft.app(main)
