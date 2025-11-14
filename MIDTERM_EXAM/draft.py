import flet as ft
from database import get_connection

def main(page: ft.Page):
    page.title = "Coffeestry System"
    page.bgcolor = ft.Colors.BROWN_100
    page.window_maximized = True
    page.window_resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.appbar = ft.AppBar(
        title=ft.Text("Coffeestry System", size=18, color=ft.Colors.WHITE),
        center_title=True,
        bgcolor=ft.Colors.BROWN_700,
    )

    # HOME SCREEN FUNCTION

    def show_home():
        page.clean()

        # Background image (responsive full-screen)
        bg_image = ft.Container(
            content=ft.Image(
                src="coffebg.png",
                fit=ft.ImageFit.COVER,
                opacity=0.25,
            ),
            expand=True,
        )

        # Foreground content
        home_content = ft.Column(
            [
                # LOGO (adjust position using margin)
                ft.Container(
                    content=ft.Image(
                        src="logo.png",
                        width=300,
                        height=300,
                        border_radius=70,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    alignment=ft.alignment.top_center,
                    margin=ft.margin.only(top=5, bottom=5),  
                ),

                # Title Texts
                ft.Text(
                    "Welcome to Coffeestry",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BROWN_900,
                ),
                ft.Text(
                    "Your cozy coffee shop system",
                    size=16,
                    color=ft.Colors.BROWN_600,
                ),

                ft.Container(
                    content=ft.ElevatedButton(
                        "Login",
                        on_click=lambda e: show_login(),
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                        width=220,
                    ),
                    alignment=ft.alignment.center,
                ),

                ft.Container(
                    content=ft.ElevatedButton(
                        "About",
                        on_click=lambda e: show_about(),
                        bgcolor=ft.Colors.BROWN_300,
                        width=220,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Exit",
                        on_click=lambda e: page.window_close(),
                        bgcolor=ft.Colors.BROWN_700,
                        color=ft.Colors.WHITE,
                        width=220,
                ),
                    alignment=ft.alignment.center,
                ),

                # Footer
                ft.Text(
                    "© 2025 Coffeestry",
                    size=12,
                    color=ft.Colors.BROWN_400,
                    italic=True,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
        )

        # Stack → background + content
        page.add(
            ft.Stack(
                [
                    bg_image,
                    ft.Container(
                        content=home_content,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                ]
            )
        )

    # LOGIN SCREEN FUNCTION

    def show_login():
        page.clean()

        username_field = ft.TextField(label="Username", width=300, color=ft.Colors.BROWN_900,)
        password_field = ft.TextField(
            label="Password", password=True, can_reveal_password=True, width=300, color=ft.Colors.BROWN_900,
        )
        message = ft.Text(value="", color=ft.Colors.RED_700, )

        def login_clicked(e):
            username = username_field.value
            password = password_field.value

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role FROM users WHERE username=? AND password=?",
                (username, password),
            )
            result = cursor.fetchone()
            conn.close()

            if result:
                role = result[0].lower()
                message.value = f"Welcome, {role.capitalize()}!"
                message.color = ft.Colors.GREEN_700
                page.update()

                # Redirect based on role
                if role == "owner":
                    show_owner_dashboard()
                elif role == "staff":
                    page.snack_bar = ft.SnackBar(ft.Text("Redirecting to Staff Dashboard..."))
                    page.snack_bar.open = True
                    # You can make another function like show_staff_dashboard()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Unknown role."))
                    page.snack_bar.open = True
            else:
                message.value = "Invalid username or password!"
                message.color = ft.Colors.RED_700
                page.update()


        login_button = ft.ElevatedButton(
            "Login",
            on_click=login_clicked,
            width=300,
            bgcolor=ft.Colors.BROWN_500,
            color=ft.Colors.WHITE,
        )
        back_button = ft.OutlinedButton(
            "Back", on_click=lambda e: show_home(), width=300
        )

        page.add(
        ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                        ft.Text(
                                    "Login to Coffeestry",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BROWN_800,
                                ),
                                username_field,
                                password_field,
                                login_button,
                                back_button,
                                message,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        padding=30,
                        width=350,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1, blur_radius=10, color=ft.Colors.GREY_400
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER, 
                vertical_alignment=ft.CrossAxisAlignment.CENTER,  
                expand=True,  
            ),
            expand=True,
        )
    )

    # ABOUT SCREEN FUNCTION

    def show_about():
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "About Coffeestry",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BROWN_800,
                    ),
                    ft.Text(
                        "Coffeestry is a coffee shop that serves fresh brewed coffee and freshly baked pastries.\n"
                        "Coffeestry aims to provide a cozy and inviting atmosphere for coffee and pastry lovers.",
                        size=14,
                        color=ft.Colors.BROWN_700,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.ElevatedButton(
                        "Back",
                        on_click=lambda e: show_home(),
                        width=200,
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
            ),
            alignment=ft.alignment.center,  
            expand=True,                    
        )
    )
    
    # OWNER DASHBOARD FUNCTION

    def show_owner_dashboard():
        page.clean()
        page.appbar = None  # We’ll make our own header bar inside

        # ----- Sidebar Navigation -----
        sidebar = ft.Container(
            bgcolor=ft.Colors.BROWN_600,
            width=220,
            padding=15,
            content=ft.Column(
                [
                    ft.Text(
                        "CoffeeStry",
                        size=24,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Divider(color=ft.Colors.BROWN_300, thickness=1),
                    ft.ElevatedButton(
                        "Dashboard",
                        icon=ft.Icons.DASHBOARD,
                        bgcolor=ft.Colors.BROWN_300,
                        color=ft.Colors.BROWN_900,
                        width=190,
                    ),
                    ft.ElevatedButton(
                        "Products and Price Management",
                        icon=ft.Icons.INVENTORY,
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                        width=190,
                    ),
                    ft.ElevatedButton(
                        "Financial Reports",
                        icon=ft.Icons.ASSESSMENT,
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                        width=190,
                    ),

                    ft.ElevatedButton(
                        "Inventory and Supplier Management",
                        icon=ft.Icons.INVENTORY,
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                        width=190,
                    ),

                    ft.ElevatedButton(
                        "User Management",
                        icon=ft.Icons.MANAGE_ACCOUNTS,
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                        width=190,
                    ),


                    ft.Container(expand=True),  # pushes logout to bottom
                    ft.ElevatedButton(
                        "Logout",
                        icon=ft.Icons.LOGOUT,
                        bgcolor=ft.Colors.GREY_400,
                        color=ft.Colors.BROWN_900,
                        width=190,
                        on_click=lambda e: show_home(),
                    ),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # ----- Header (top bar inside right content area) -----
        header = ft.Row(
            [
                ft.Text(
                    "CoffeeStry Menu",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BROWN_900,
                ),
                ft.Container(expand=True),
                ft.Text(
                    "Welcome, Coffeestry",
                    size=14,
                    color=ft.Colors.BROWN_800,
                ),
                ft.CircleAvatar(
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.BROWN_700,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        # ----- Menu Cards (Main Content Grid) -----
        def menu_card(name, desc, price):
            return ft.Container(
                width=180,
                height=200,
                bgcolor=ft.Colors.BROWN_50,
                border_radius=10,
                padding=10,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=5,
                    color=ft.Colors.GREY_400,
                ),
                content=ft.Column(
                    [
                        ft.Container(
                            bgcolor=ft.Colors.BROWN_200,
                            height=100,
                            border_radius=8,
                            content=ft.Row(
                                [
                                    ft.Container(expand=True),
                                    ft.Icon(ft.Icons.EDIT, size=18, color=ft.Colors.BROWN_700),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                        ft.Text(name, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900),
                        ft.Text(desc, size=12, color=ft.Colors.BROWN_600),
                        ft.Text(f"₱{price:.2f}", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
                    ],
                    spacing=4,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
            )

        menu_items = [
            ("Americano", "A black coffee", 99.00),
            ("Espresso", "A black strong coffee", 99.00),
            ("Pilipino", "A roasted rice coffee", 99.00),
            ("Croissant", "With different filled", 75.00),
            ("Brownies", "A moist chocolatey", 75.00),
            ("Butter Cookies", "Crisp and moisty", 75.00),
        ]

        grid = ft.ResponsiveRow(
            [
                ft.Container(
                    content=menu_card(name, desc, price),
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                )
                for name, desc, price in menu_items
            ],
            spacing=20,
        )

        # ----- Right Content Area -----
        main_content = ft.Container(
            expand=True,
            bgcolor=ft.Colors.BROWN_100,
            padding=20,
            content=ft.Column(
                [
                    header,
                    ft.Divider(color=ft.Colors.BROWN_300),
                    grid,
                ],
                spacing=15,
            ),
        )

        # ----- Combine Sidebar + Main Content -----
        layout = ft.Row(
            [
                sidebar,
                main_content,
            ],
            expand=True,
        )

        page.add(layout)


        

    # Start the app with the home screen
    show_home()

ft.app(target=main)
