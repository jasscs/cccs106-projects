# main.py
"""Weather Application using Flet v0.28.3"""

import asyncio
import flet as ft
from weather_service import WeatherService
from config import Config
import json
from pathlib import Path


class WeatherApp:
    """Main Weather Application class."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()
        self.history_file = Path("search_history.json")
        self.search_history = self.load_history()
        self.setup_page()
        self.build_ui()

    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
        self.page.padding = 20
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        self.page.window.center()

    def build_ui(self):
        """Build the user interface."""
        # Title
        self.title = ft.Text(
            "Weather App",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
        )

        # Theme button
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            tooltip="Toggle theme",
            on_click=self.toggle_theme,
        )

        # City input field
        self.city_input = ft.TextField(
            label="Enter city name",
            hint_text="e.g., London, Tokyo, New York",
            border_color=ft.Colors.BLUE_400,
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            on_submit=self.on_search,
            expand=True,
            on_focus=self.show_history_dropdown,
            on_blur=self.hide_history_dropdown,
            suffix=ft.IconButton(
                icon=ft.Icons.SEARCH,
                tooltip="Search",
                on_click=self.on_search,
            ),
        )

        # Recent searches column
        self.history_column = ft.Column(
            controls=[],
            spacing=5,
        )

        # Weather display container
        self.weather_container = ft.Container(
            visible=False,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            padding=20,
        )

        # Error message
        self.error_message = ft.Text("", color=ft.Colors.RED_700, visible=False)

        # Loading indicator
        self.loading = ft.ProgressRing(visible=False)

        # Clear history button
        self.clear_history_button = ft.ElevatedButton(
            "Clear History",
            on_click=self.clear_history,
            color=ft.Colors.BLUE,
            visible=bool(self.search_history),
        )
        

        self.history_dropdown = ft.Container(
            content=self.history_column,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=10,
            visible=False,
            shadow=ft.BoxShadow(
                blur_radius=8,
                color=ft.Colors.BLACK,
            ),
        )

        # Input row (input + buttons)
        input_row = ft.Row(
            [
                self.city_input,
                self.history_dropdown,
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        # Stack input row + recent searches below
        input_and_history = ft.Column(
            [
                self.city_input,
                self.history_dropdown,
                ft.Container(height=5),
                self.clear_history_button,
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Page layout
        self.page.add(
            ft.Column(
                [
                    self.title,
                    self.theme_button,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    input_and_history,  # input + history
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.loading,
                    self.error_message,
                    self.weather_container,
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        # Populate initial history
        self.update_history_column()

    def on_search(self, e):
        """Handle search button click or enter key press."""
        city = self.city_input.value.strip()
        if city:
            self.add_to_history(city)
            self.page.run_task(self.get_weather)
        else:
            self.show_error("Please enter a city name")

    async def get_weather(self):
        """Fetch and display weather data."""
        city = self.city_input.value.strip()
        if not city:
            self.show_error("Please enter a city name")
            return

        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.page.update()

        try:
            weather_data = await self.weather_service.get_weather(city)
            self.display_weather(weather_data)
        except Exception as e:
            self.show_error(str(e))
        finally:
            self.loading.visible = False
            self.page.update()

    def display_weather(self, data: dict):
        """Display weather information."""
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp", 0)
        feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)

        self.weather_container.content = ft.Column(
            [
                ft.Text(f"{city_name}, {country}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                ft.Row(
                    [
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                            width=100,
                            height=100,
                        ),
                        ft.Text(description, size=20, italic=True, color=ft.Colors.BLACK),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(f"{temp:.1f}°C", size=48, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ft.Text(f"Feels like {feels_like:.1f}°C", size=16, color=ft.Colors.BLACK),
                ft.Divider(),
                ft.Row(
                    [
                        self.create_info_card(ft.Icons.WATER_DROP, "Humidity", f"{humidity}%"),
                        self.create_info_card(ft.Icons.AIR, "Wind Speed", f"{wind_speed} m/s"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.weather_container.visible = True
        self.clear_history_button.visible = True
        self.page.update()

    def create_info_card(self, icon, label, value):
        """Create an info card for weather details."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=30, color=ft.Colors.BLUE_700),
                    ft.Text(label, size=12, color=ft.Colors.BLACK),
                    ft.Text(value, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
            width=150,
        )

    def show_error(self, message: str):
        """Display error message."""
        self.error_message.value = f"❌ {message}"
        self.error_message.visible = True
        self.weather_container.visible = False
        self.page.update()

    def toggle_theme(self, e):
        """Toggle light/dark theme."""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_button.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_button.icon = ft.Icons.DARK_MODE
        self.page.update()

    def load_history(self):
        if self.history_file.exists():
            with open(self.history_file, "r") as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.search_history, f)

    def add_to_history(self, city: str):
        city = city.title()
        if city in self.search_history:
            self.search_history.remove(city)
        self.search_history.insert(0, city)
        self.search_history = self.search_history[:10]
        self.save_history()
        self.update_history_column()

    def update_history_column(self):
        """Update the recent searches panel below input."""
        self.history_column.controls = [
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(city, size=14, color=ft.Colors.WHITE),
                        padding=ft.Padding(5, 2, 5, 2),
                        bgcolor=ft.Colors.BLUE_700,
                        border_radius=10,
                        on_click=lambda e, c=city: self.select_history_city(c),
                    )
                ],
            )
            for city in self.search_history
        ]
        self.page.update()

    def select_history_city(self, city):
        """Select a city from history."""
        self.city_input.value = city
        self.page.update()
        self.page.run_task(self.get_weather)

    def clear_history(self, e):
        """Clear search history."""
        self.search_history = []
        self.save_history()
        self.update_history_column()
        self.clear_history_button.visible = False
        self.page.update()

    def show_history_dropdown(self, e):
        if len(self.search_history) > 0:
            self.history_dropdown.visible = True
            self.page.update()
            
    def hide_history_dropdown(self, e):
        asyncio.create_task(self._hide_after_delay())
        
    async def _hide_after_delay(self):
        await asyncio.sleep(0.15)
        self.history_dropdown.visible = False
        self.page.update()

    def toggle_units(self, e):
        if self.current_unit == "metric":
            self.current_unit = "imperial"
            self.current_temp = (self.current_temp * 9 / 5) + 32
            self.unit_button.text = "°F"
        else:
            self.current_unit = "metric"
            self.current_temp = (self.current_temp - 32) * 5 / 9
            self.unit_button.text = "°C"
        self.refresh_watchlist_panel()
        self.update_display()

    def update_display(self):
        if hasattr(self, "temp_text"):
            self.temp_text.value = f"{self.current_temp:.1f}°{'C' if self.current_unit=='metric' else 'F'}"
            self.page.update()


def main(page: ft.Page):
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)
