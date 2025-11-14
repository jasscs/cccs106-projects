import pytest
import flet as ft
from unittest.mock import Mock
from main import GradeCalculator


class MockPage:
    """Mock Flet Page object for testing."""
    
    def __init__(self):
        self.controls = []
        self.dialogs = []
        self.title = ""
        self.horizontal_alignment = None
        self.vertical_alignment = None
        self.bgcolor = None
        self.scroll = None
        self.window = MockWindow()
        self.updated = False
    
    def add(self, control):
        self.controls.append(control)
        self._register_control(control)
    
    def update(self, *args, **kwargs):
        self.updated = True
    
    def open(self, dialog):
        self.dialogs.append(dialog)
    
    def close(self, dialog):
        if dialog in self.dialogs:
            self.dialogs.remove(dialog)
    
    def _register_control(self, control):
        """Recursively register all controls with mock page."""
        if hasattr(control, '_Control__page'):
            control._Control__page = self
        if hasattr(control, 'controls'):
            for child in control.controls:
                self._register_control(child)
        if hasattr(control, 'content'):
            if control.content:
                self._register_control(control.content)


class MockWindow:
    """Mock Window object for testing."""
    
    def __init__(self):
        self.width = None
        self.height = None
        self.resizable = None
    
    def center(self):
        pass


@pytest.fixture
def mock_page():
    """Fixture to create a mock page for testing."""
    return MockPage()


@pytest.fixture
def grade_calc(mock_page):
    """Fixture to create a GradeCalculator instance for testing."""
    app = GradeCalculator(mock_page)
    # Register all controls with the mock page
    mock_page._register_control(app.name_input)
    mock_page._register_control(app.subject_dropdown)
    mock_page._register_control(app.grade_input)
    mock_page._register_control(app.grades_list)
    mock_page._register_control(app.stats_text)
    mock_page._register_control(app.stats_bar)
    mock_page._register_control(app.view)
    
    # Mock the focus method
    app.name_input.focus = lambda: None
    
    return app


def test_grade_calculator_initialization(grade_calc):
    """Test 1: GradeCalculator initializes with correct default values."""
    assert grade_calc.name_input is not None
    assert grade_calc.subject_dropdown is not None
    assert grade_calc.grade_input is not None
    assert grade_calc.grades_list is not None
    assert grade_calc.stats_text.value == "No grades recorded"
    assert grade_calc.stats_bar.value == 0
    assert len(grade_calc.grades_list.controls) == 0


def test_add_valid_grade(grade_calc, mock_page):
    """Test 2: Adding a valid grade adds it to the list."""
    grade_calc.name_input.value = "John Doe"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "85"
    
    initial_count = len(grade_calc.grades_list.controls)
    grade_calc.add_grade()
    
    assert len(grade_calc.grades_list.controls) == initial_count + 1
    assert mock_page.updated is True


def test_dropdown_resets_after_adding_grade(grade_calc):
    """Test 3: Dropdown resets to empty after adding a grade."""
    grade_calc.name_input.value = "John Doe"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "85"
    
    grade_calc.add_grade()
    
    # After adding, dropdown should be reset to empty/None
    assert grade_calc.subject_dropdown.value == "" or grade_calc.subject_dropdown.value is None
    assert grade_calc.name_input.value == ""
    assert grade_calc.grade_input.value == ""


def test_reject_empty_student_name(grade_calc, mock_page):
    """Test 4: Adding grade with empty student name shows error."""
    grade_calc.name_input.value = ""
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "85"
    
    initial_count = len(grade_calc.grades_list.controls)
    grade_calc.add_grade()
    
    assert len(grade_calc.grades_list.controls) == initial_count
    assert len(mock_page.dialogs) > 0


def test_reject_whitespace_student_name(grade_calc):
    """Test 5: Adding grade with whitespace-only name shows error."""
    grade_calc.name_input.value = "   "
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "85"
    
    initial_count = len(grade_calc.grades_list.controls)
    grade_calc.add_grade()
    
    assert len(grade_calc.grades_list.controls) == initial_count


def test_reject_unselected_subject(grade_calc, mock_page):
    """Test 6: Adding grade without selecting subject shows error."""
    grade_calc.name_input.value = "John Doe"
    grade_calc.subject_dropdown.value = None
    grade_calc.grade_input.value = "85"
    
    initial_count = len(grade_calc.grades_list.controls)
    grade_calc.add_grade()
    
    assert len(grade_calc.grades_list.controls) == initial_count
    assert len(mock_page.dialogs) > 0


def test_reject_invalid_grade_non_numeric(grade_calc, mock_page):
    """Test 7: Adding non-numeric grade shows error."""
    grade_calc.name_input.value = "John Doe"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "abc"
    
    initial_count = len(grade_calc.grades_list.controls)
    grade_calc.add_grade()
    
    assert len(grade_calc.grades_list.controls) == initial_count
    assert len(mock_page.dialogs) > 0


def test_reject_grade_below_zero(grade_calc):
    """Test 8: Adding grade below 0 shows error."""
    grade_calc.name_input.value = "John Doe"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "-5"
    
    initial_count = len(grade_calc.grades_list.controls)
    grade_calc.add_grade()
    
    assert len(grade_calc.grades_list.controls) == initial_count


def test_reject_grade_above_100(grade_calc):
    """Test 9: Adding grade above 100 shows error."""
    grade_calc.name_input.value = "John Doe"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "105"
    
    initial_count = len(grade_calc.grades_list.controls)
    grade_calc.add_grade()
    
    assert len(grade_calc.grades_list.controls) == initial_count


def test_statistics_with_no_grades(grade_calc):
    """Test 10: Statistics show correct message when no grades exist."""
    grade_calc.update_statistics()
    
    assert grade_calc.stats_text.value == "No grades recorded"
    assert grade_calc.stats_bar.value == 0


def test_statistics_calculation_with_one_grade(grade_calc):
    """Test 11: Statistics calculate correctly with one grade."""
    grade_calc.name_input.value = "John Doe"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "80"
    grade_calc.add_grade()
    
    assert "Total Grades: 1" in grade_calc.stats_text.value
    assert "Average: 80.0" in grade_calc.stats_text.value
    assert "Highest: 80" in grade_calc.stats_text.value
    assert "Lowest: 80" in grade_calc.stats_text.value
    assert grade_calc.stats_bar.value == pytest.approx(0.8, rel=0.01)


def test_statistics_calculation_with_multiple_grades(grade_calc):
    """Test 12: Statistics calculate correctly with multiple grades."""
    # Add three grades: 70, 80, 90
    grades_data = [
        ("Alice", "Math", "70"),
        ("Bob", "Science", "80"),
        ("Charlie", "English", "90"),
    ]
    
    for name, subject, grade in grades_data:
        grade_calc.name_input.value = name
        grade_calc.subject_dropdown.value = subject
        grade_calc.grade_input.value = grade
        grade_calc.add_grade()
    
    assert "Total Grades: 3" in grade_calc.stats_text.value
    assert "Average: 80.0" in grade_calc.stats_text.value
    assert "Highest: 90" in grade_calc.stats_text.value
    assert "Lowest: 70" in grade_calc.stats_text.value


def test_add_grade_from_event(grade_calc, mock_page):
    """Test 13: add_grade_from_event correctly adds grade from input fields."""
    grade_calc.name_input.value = "Test Student"
    grade_calc.subject_dropdown.value = "History"
    grade_calc.grade_input.value = "75"
    
    mock_event = type('Event', (), {})()
    grade_calc.add_grade_from_event(mock_event)
    
    assert len(grade_calc.grades_list.controls) == 1
    assert mock_page.updated is True


def test_add_grade_clicked(grade_calc, mock_page):
    """Test 14: add_grade_clicked correctly adds grade when button is clicked."""
    grade_calc.name_input.value = "Button Test"
    grade_calc.subject_dropdown.value = "Computer Science"
    grade_calc.grade_input.value = "95"
    
    mock_event = type('Event', (), {})()
    grade_calc.add_grade_clicked(mock_event)
    
    assert len(grade_calc.grades_list.controls) == 1
    assert mock_page.updated is True


def test_progress_bar_color_green_for_high_average(grade_calc):
    """Test 15: Progress bar color is green when average >= 75."""
    grade_calc.name_input.value = "Student"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "85"
    grade_calc.add_grade()
    
    assert grade_calc.stats_bar.color == ft.Colors.GREEN


def test_progress_bar_color_orange_for_medium_average(grade_calc):
    """Test 16: Progress bar color is orange when 60 <= average < 75."""
    grade_calc.name_input.value = "Student"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "65"
    grade_calc.add_grade()
    
    assert grade_calc.stats_bar.color == ft.Colors.ORANGE


def test_grade_row_color_excellent(grade_calc):
    """Test 17: Grade row has blue background for grade >= 90."""
    grade_calc.name_input.value = "Student"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "95"
    grade_calc.add_grade()
    
    grade_row = grade_calc.grades_list.controls[0]
    grade_container = grade_row.controls[0]
    
    assert grade_container.bgcolor == ft.Colors.BLUE_100


def test_grade_row_color_passed(grade_calc):
    """Test 18: Grade row has green background for 75 <= grade < 90."""
    grade_calc.name_input.value = "Student"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "80"
    grade_calc.add_grade()
    
    grade_row = grade_calc.grades_list.controls[0]
    grade_container = grade_row.controls[0]
    
    assert grade_container.bgcolor == ft.Colors.GREEN_100


def test_grade_row_color_fair(grade_calc):
    """Test 19: Grade row has orange background for 60 <= grade < 75."""
    grade_calc.name_input.value = "Student"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "65"
    grade_calc.add_grade()
    
    grade_row = grade_calc.grades_list.controls[0]
    grade_container = grade_row.controls[0]
    
    assert grade_container.bgcolor == ft.Colors.ORANGE_100


def test_grade_row_color_failed(grade_calc):
    """Test 20: Grade row has red background for grade < 60."""
    grade_calc.name_input.value = "Student"
    grade_calc.subject_dropdown.value = "Math"
    grade_calc.grade_input.value = "50"
    grade_calc.add_grade()
    
    grade_row = grade_calc.grades_list.controls[0]
    grade_container = grade_row.controls[0]
    
    assert grade_container.bgcolor == ft.Colors.RED_100


def test_subject_dropdown_options(grade_calc):
    """Test 21: Subject dropdown has all required options."""
    expected_subjects = ["Math", "Science", "English", "History", "Computer Science"]
    dropdown_keys = [opt.key for opt in grade_calc.subject_dropdown.options]
    
    assert len(dropdown_keys) == len(expected_subjects)
    for subject in expected_subjects:
        assert subject in dropdown_keys


def test_main_page_title():
    """Test 22: Main function sets page title with Grade Calculator."""
    from main import main
    mock_page = MockPage()
    main(mock_page)
    
    assert "Grade Calculator" in mock_page.title
    assert isinstance(mock_page.title, str)
    assert len(mock_page.title) > 0


def test_main_page_window_size():
    """Test 23: Main function sets correct window dimensions."""
    from main import main
    mock_page = MockPage()
    main(mock_page)
    
    assert mock_page.window.width == 450
    assert mock_page.window.height == 750


def test_main_page_background_color_and_window_resizable():
    """Test 24: Main function sets correct background color."""
    from main import main
    mock_page = MockPage()
    main(mock_page)

    assert mock_page.window.resizable is False
    assert mock_page.bgcolor == ft.Colors.PURPLE_50


def test_grade_calculator_view_width():
    """Test 25: GradeCalculator view has correct width."""
    mock_page = MockPage()
    app = GradeCalculator(mock_page)
    
    assert app.view.width == 650
