import flet as ft


class GradeCalculator:
    def __init__(self, page: ft.Page):
        self.page = page
        self.grades = []

        self.name_input = ft.TextField(label="Enter Student Name", width=650, bgcolor=ft.Colors.WHITE)
        self.dropdown = ft.Dropdown(
            label="Select Subject",
            bgcolor=ft.Colors.WHITE,
            options=[
                ft.dropdown.Option("Math"),
                ft.dropdown.Option("Science"),
                ft.dropdown.Option("English"),
                ft.dropdown.Option("History"),
                ft.dropdown.Option("Computer Science"),
            ],
            width=650,
        )
        self.grade_input = ft.TextField(label="Enter Grade (0–100)", width=650, bgcolor=ft.Colors.WHITE, keyboard_type=ft.KeyboardType.NUMBER)

        self.add_button = ft.FloatingActionButton(icon=ft.Icons.ADD,bgcolor=ft.Colors.BLUE,width=650, on_click=self.add_grade_clicked)

        self.stat_text = ft.Text("No grades recorded", color=ft.Colors.GREY_700, size=16, weight=ft.FontWeight.BOLD)
        self.stat_bar = ft.ProgressBar(width=650, value=0, color=ft.Colors.GREY)

        self.grades_list = ft.Column(spacing=10, width=600)

        self.view = ft.Column(
            width=650,
            spacing=25,
            controls=[
                self.name_input,
                self.dropdown,
                self.grade_input,
                self.add_button,
                ft.Column(
                    [self.stat_text, self.stat_bar],
                    spacing=5,
                ),
                self.grades_list,
            ],
        )

    def add_grade(self):
        name = self.name_input.value.strip()
        subject = self.dropdown.value
        grade_str = self.grade_input.value.strip()

        if not name:
            return self.show_error("Please enter a student name.")
        if not subject:
            return self.show_error("Please select a subject.")
        if not grade_str.isdigit():
            return self.show_error("Please enter a valid grade between 0 and 100.")

        grade = float(grade_str)
        if grade < 0 or grade > 100:
            return self.show_error("Grade must be between 0 and 100.")
        
        self.grades.append(grade)
        container_color = self.get_grade_color(grade)

        delete_button =  ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED,bgcolor=ft.Colors.RED_50,tooltip="Delete Grade")
        
        grade_row = ft.Row(
            controls=[
                ft.Container(
                    ft.Text(f"{subject} - {name}: {grade}", color=ft.Colors.BLACK),
                    bgcolor=container_color,
                    padding=10,
                    border_radius=10,
                    expand=True,
                ), delete_button
            ]
        )
        self.grades_list.controls.append(grade_row)
        self.update_statistics()

        self.name_input.value = ""
        self.dropdown.value = ""
        self.grade_input.value = ""
        self.page.update()

    def show_error(self, message: str):
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Input Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dialog)
        self.page.update()

    def close_dialog(self, dialog):
        dialog.open = False
        self.page.update()

    def update_statistics(self):
        if not self.grades:
            self.stat_text.value = "No grades recorded"
            self.stat_bar.value = 0
            self.stat_bar.color = ft.Colors.GREY
        else:
            total = len(self.grades)
            average = sum(self.grades) / total
            highest = max(self.grades)
            lowest = min(self.grades)

            self.stat_text.value = (
                f"Total Grades: {total} | Average: {average:.1f} | "
                f"Highest: {highest} | Lowest: {lowest}"
            )
            self.stat_bar.value = average / 100
            self.stat_bar.color = self.get_average_color(average)

        self.page.update()

    def get_grade_color(self, grade):
        if grade >= 90:
            return ft.Colors.BLUE_100
        elif grade >= 75:
            return ft.Colors.GREEN_100
        elif grade >= 60:
            return ft.Colors.ORANGE_100
        else:
            return ft.Colors.RED_100

    def get_average_color(self, average):
        if average >= 75:
            return ft.Colors.GREEN
        elif average >= 60:
            return ft.Colors.ORANGE
        else:
            return ft.Colors.RED

    def add_grade_from_event(self, e):
        self.add_grade()

    def add_grade_clicked(self, e):
        self.add_grade()

def main(page: ft.Page):
    page.title = "FRANCISCO GRADE CALCULATOR"
    page.window.width = 450
    page.window.height = 750
    page.window.resizable = False
    page.bgcolor = ft.Colors.PURPLE_50
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO
    page.window.center()

    app = GradeCalculator(page)
    page.add(app.view)


if __name__ == "__main__":
    ft.app(target=main)