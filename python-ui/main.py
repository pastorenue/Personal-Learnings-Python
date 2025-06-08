from nicegui import ui


@ui.page("/")
def home():
    ui.label("Welcome to NICEGUI")

    # A simple interactive counter
    counter = ui.label("0")

    def incr():
        count = int(counter.text) + 1
        counter.set_text(str(count))
    
    ui.button("Increment", on_click=incr)



ui.run()