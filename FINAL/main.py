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

    # -------------------------------------------------
    # HOME SCREEN
    # -------------------------------------------------
    def show_home():
        page.clean()

        bg_image = ft.Container(
            content=ft.Image(src="coffebg.png", fit=ft.ImageFit.COVER, opacity=0.25),
            expand=True,
        )

        home_content = ft.Column(
            [
                ft.Container(
                    content=ft.Image(src="logo.png", width=300, height=300, fit=ft.ImageFit.CONTAIN),
                    alignment=ft.alignment.top_center,
                    margin=ft.margin.only(top=5, bottom=5),
                ),
                ft.Text("Welcome to Coffeestry", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900),
                ft.Text("Your cozy coffee shop system", size=16, color=ft.Colors.BROWN_600),
                ft.Container(
                    content=ft.ElevatedButton("Login", on_click=lambda e: show_login(),
                        bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE, width=220),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton("About", on_click=lambda e: show_about(),
                        bgcolor=ft.Colors.BROWN_300, width=220),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton("Exit", on_click=lambda e: page.window_close(),
                        bgcolor=ft.Colors.BROWN_700, color=ft.Colors.WHITE, width=220),
                    alignment=ft.alignment.center,
                ),
                ft.Text("© 2025 Coffeestry", size=12, color=ft.Colors.BROWN_400,
                        italic=True, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
        )

        page.add(ft.Stack([bg_image, ft.Container(content=home_content, alignment=ft.alignment.center, expand=True)]))

    # -------------------------------------------------
    # ABOUT SCREEN
    # -------------------------------------------------
    def show_about():
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("About Coffeestry", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
                        ft.Text(
                            "Coffeestry is a coffee shop that serves fresh brewed coffee and freshly baked pastries.\n"
                            "Coffeestry aims to provide a cozy and inviting atmosphere for coffee and pastry lovers.",
                            size=14, color=ft.Colors.BROWN_700, text_align=ft.TextAlign.CENTER,
                        ),
                        ft.ElevatedButton("Back", on_click=lambda e: show_home(),
                                          width=200, bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )

    # -------------------------------------------------
    # LOGIN SCREEN
    # -------------------------------------------------
    def show_login():
        page.clean()

        username_field = ft.TextField(label="Username", width=300, color=ft.Colors.BROWN_900)
        password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, color=ft.Colors.BROWN_900)
        message = ft.Text(value="", color=ft.Colors.RED_700)

        def login_clicked(e):
            username = username_field.value
            password = password_field.value

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                role = result[0].lower()
                message.value = f"Welcome, {role.capitalize()}!"
                message.color = ft.Colors.GREEN_700
                page.update()

                if role == "owner":
                    show_owner_dashboard()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Redirecting to Staff Dashboard..."))
                    page.snack_bar.open = True
            else:
                message.value = "Invalid username or password!"
                message.color = ft.Colors.RED_700
                page.update()

        login_button = ft.ElevatedButton("Login", on_click=login_clicked, width=300, bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE)
        back_button = ft.OutlinedButton("Back", on_click=lambda e: show_home(), width=300)

        page.add(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Login to Coffeestry", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
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
                            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.GREY_400),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                expand=True,
            )
        )
        

    # -------------------------------------------------
    # OWNER DASHBOARD
    # -------------------------------------------------
    def show_owner_dashboard():
        page.clean()
        main_content = ft.Container(expand=True)

        def show_dashboard_page():
            owner_title = ft.Text("Owner Dashboard", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900)
            main_content.content = ft.Container(
            padding=20,
            bgcolor=ft.Colors.BROWN_100,
            content=ft.Column([
                ft.Text("📊 Dashboard Overview", size=22, weight=ft.FontWeight.BOLD),
                # your dashboard content here
            ], spacing=20)
        )

            # --- DASHBOARD CARDS ---
            dashboard_cards = ft.Row(
                [
                    ft.Container(width=210, height=140, bgcolor=ft.Colors.WHITE, border=ft.border.all(1, ft.Colors.BROWN_200),
                                 border_radius=8, alignment=ft.alignment.center,
                                 content=ft.Column([
                                     ft.Icon(ft.Icons.SELL, color=ft.Colors.BROWN_700),
                                     ft.Text("Total Sales", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900)
                                 ], alignment=ft.MainAxisAlignment.CENTER)),
                    ft.Container(width=210, height=140, bgcolor=ft.Colors.WHITE, border=ft.border.all(1, ft.Colors.BROWN_200),
                                 border_radius=8, alignment=ft.alignment.center,
                                 content=ft.Column([
                                     ft.Icon(ft.Icons.LOCAL_CAFE, color=ft.Colors.BROWN_700),
                                     ft.Text("Total Products", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900)
                                 ], alignment=ft.MainAxisAlignment.CENTER)),
                    ft.Container(width=210, height=140, bgcolor=ft.Colors.WHITE, border=ft.border.all(1, ft.Colors.BROWN_200),
                                 border_radius=8, alignment=ft.alignment.center,
                                 content=ft.Column([
                                     ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED_400),
                                     ft.Text("Low Stock Alert", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900)
                                 ], alignment=ft.MainAxisAlignment.CENTER)),
                    ft.Container(width=210, height=140, bgcolor=ft.Colors.WHITE, border=ft.border.all(1, ft.Colors.BROWN_200),
                                 border_radius=8, alignment=ft.alignment.center,
                                 content=ft.Column([
                                     ft.Icon(ft.Icons.RECEIPT_LONG, color=ft.Colors.BROWN_700),
                                     ft.Text("Recent Orders", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900)
                                 ], alignment=ft.MainAxisAlignment.CENTER)),
                ],
                alignment=ft.MainAxisAlignment.START, spacing=35,
            )

            dashboard_section = ft.Container(
                padding=15,
                margin=ft.margin.only(top=10),
                border=ft.border.all(1, ft.Colors.BROWN_300),
                border_radius=10,
                bgcolor=ft.Colors.WHITE,
                content=ft.Column(
                    [ft.Text("Dashboard Overview", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900),
                     ft.Container(height=5), dashboard_cards],
                    spacing=10,
                ),
            )
            

            # --- MENU SECTION ---
            def menu_card(name, desc, price):
                return ft.Container(
                    width=180, height=200, bgcolor=ft.Colors.BROWN_50, border_radius=10,
                    padding=10, shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.GREY_400),
                    content=ft.Column(
                        [
                            ft.Container(bgcolor=ft.Colors.BROWN_200, height=100, border_radius=8,
                                         content=ft.Row([ft.Container(expand=True),
                                                         ft.Icon(ft.Icons.EDIT, size=18, color=ft.Colors.BROWN_700)],
                                                        alignment=ft.MainAxisAlignment.END)),
                            ft.Text(name, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900),
                            ft.Text(desc, size=12, color=ft.Colors.BROWN_600),
                            ft.Text(f"₱{price:.2f}", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
                        ],
                        spacing=4,
                    ),
                )

            menu_items = [
                ("Americano", "A black coffee", 99.00),
                ("Espresso", "A strong black coffee", 99.00),
                ("Pilipino", "A roasted rice coffee", 99.00),
                ("Croissant", "With different fillings", 75.00),
                ("Brownies", "A moist chocolatey treat", 75.00),
                ("Butter Cookies", "Crisp and buttery", 75.00),
            ]

            menu_grid = ft.ResponsiveRow(
                [ft.Container(content=menu_card(name, desc, price), col={"xs": 12, "sm": 6, "md": 4, "lg": 3})
                 for name, desc, price in menu_items],
                spacing=20,
            )

            menu_section = ft.Container(
                padding=15,
                margin=ft.margin.only(top=20),
                border=ft.border.all(1, ft.Colors.BROWN_300),
                border_radius=10,
                bgcolor=ft.Colors.WHITE,
                content=ft.Column(
                    [ft.Text("Menu’s", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900),
                     ft.Container(height=5), menu_grid],
                    spacing=10,
                ),
            )

            dashboard_view = ft.Column([owner_title, dashboard_section, menu_section],
                                       spacing=20, scroll=ft.ScrollMode.AUTO)

            main_content.content = ft.Container(padding=20, bgcolor=ft.Colors.BROWN_100, content=dashboard_view)
            page.update()

            # -------------------------------------------------
    # PRODUCT & PRICE MANAGEMENT PAGE
    # -------------------------------------------------
    def show_product_management_page():
        # Page title
        title = ft.Text(
            "🛍️ Product and Price Management",
            size=22,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BROWN_900,
        )

        # Search + Add row
        search_field = ft.TextField(
            hint_text="Search products...",
            prefix_icon=ft.Icons.SEARCH,
            width=400,
            bgcolor=ft.Colors.WHITE,
        )

        add_button = ft.IconButton(
            icon=ft.Icons.ADD,
            tooltip="Add new product",
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BROWN_700,
            on_click=lambda e: page.snack_bar.open or page.snack_bar,  # placeholder — replace with add dialog
        )

        search_row = ft.Row([search_field, add_button], spacing=10)

        # Table header
        header_row = ft.Row(
            [
                ft.Text("Product", weight=ft.FontWeight.BOLD, width=150),
                ft.Text("Category", weight=ft.FontWeight.BOLD, width=150),
                ft.Text("Price (₱)", weight=ft.FontWeight.BOLD, width=100),
                ft.Text("Action", weight=ft.FontWeight.BOLD, width=150),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

        # TEMP sample data (replace with DB query later)
        products = [
            {"product": "Espresso", "category": "Coffee", "price": 99.00},
            {"product": "Latte", "category": "Coffee", "price": 109.00},
            {"product": "Croissant", "category": "Pastry", "price": 75.00},
            {"product": "Butter Cookies", "category": "Pastry", "price": 70.00},
        ]

        # Build rows
        rows = []
        for p in products:
            rows.append(
                ft.Row(
                    [
                        ft.Text(p["product"], width=150),
                        ft.Text(p["category"], width=150),
                        ft.Text(f"{p['price']:.2f}", width=100),
                        ft.Row(
                            [
                                ft.ElevatedButton("Edit", bgcolor=ft.Colors.BROWN_400, color=ft.Colors.WHITE, width=70,
                                                  on_click=lambda e, prod=p: page.snack_bar.open or page.snack_bar),
                                ft.ElevatedButton("Delete", bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE, width=70,
                                                  on_click=lambda e, prod=p: page.snack_bar.open or page.snack_bar),
                            ],
                            spacing=5,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            )

        table_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            padding=15,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BROWN_300),
            content=ft.Column([header_row, *rows], spacing=8),
        )

        product_management_view = ft.Column(
            [title, search_row, table_container],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )
        
        main_content.content = ft.Container(
            padding=20,
            bgcolor=ft.Colors.BROWN_100,
            content=product_management_view,
        )
        page.update()


        # --- SIDEBAR ---
        sidebar = ft.Container(
            bgcolor=ft.Colors.BROWN_600, width=220, padding=15,
            content=ft.Column(
                [
                    ft.Text("Coffeestry", size=24, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Divider(color=ft.Colors.BROWN_300, thickness=1),
                    ft.ElevatedButton("Dashboard", icon=ft.Icons.DASHBOARD, bgcolor=ft.Colors.BROWN_300,
                                      color=ft.Colors.BROWN_900, width=190, on_click=lambda e: show_dashboard_page()),
                    ft.ElevatedButton("Products and Price Management", icon=ft.Icons.INVENTORY,
                                      width=190, bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE, on_click=lambda e: show_product_management_page()),
                    ft.ElevatedButton("Financial Reports", icon=ft.Icons.ASSESSMENT, width=190,
                                      bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Inventory & Supplier Management", icon=ft.Icons.STORE, width=190,
                                      bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE),
                    ft.ElevatedButton("User Management", icon=ft.Icons.MANAGE_ACCOUNTS, width=190,
                                      bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE),
                    ft.Container(expand=True),
                    ft.ElevatedButton("Logout", icon=ft.Icons.LOGOUT, bgcolor=ft.Colors.GREY_400,
                                      color=ft.Colors.BROWN_900, width=190, on_click=lambda e: show_home()),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        
        layout = ft.Row([sidebar, main_content], expand=True)
        page.add(layout)

        show_dashboard_page()

    # Start with home
    show_home()

ft.app(target=main)
