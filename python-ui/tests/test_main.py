from main import home
from nicegui import ui


def test_home_renders_welcome_label():
    with ui.page_context():
        home()

    # Find the label with the welcome text
    welcome_labels = [element for element in ui.elements if 
                    isinstance(element, ui.label) and 
                    element.text == "Welcome to NICEGUI"]

    assert len(welcome_labels) == 1, "Welcome label not found or found multiple times"
