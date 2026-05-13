from textual.app import App
from textual.widgets import Footer, Header, Static, Button
from textual.containers import Horizontal, VerticalScroll, Container


class AppHome(App):
    
    """A terminal UI skeleton for comparing original and corrected text."""

    CSS = """
    #button-container {
        height: 10%;
        width: 100%;
        align: center middle;
    }
    
    #main-body {
        height: 60%;
        width: 100%;
    }

    .text-box {
        width: 50%;
        height: 100%;
        border: solid $primary; /* Basic standard border */
        padding: 1;
    }

    #bottom-section {
        height: 30%;
        width: 100%;
        border: solid $primary; /* Basic standard border */
        padding: 1;
        }
    """
    
    BINDINGS = [("q", "quit", "Exit")]
    
    def compose(self):
        """Create the UI structure."""
        yield Header()
        
        with Container(id="button-container"):
            yield Button("REPLACE", id="replace-button")
        
        # Comparison area
        with Horizontal(id="main-body"):
            with VerticalScroll(id="source-text-raw", classes="text-box"):
                yield Static("SOURCE TEXT (WITH ERRORS)...")
            with VerticalScroll(id="source-text-corrected", classes="text-box"):
                yield Static("SOURCE TEXT (WITH CORRECTIONS)...")
        
        # Bottom area for analysis
        with VerticalScroll(id="bottom-section"):
            yield Static("ANALYSIS ERROR...")
         
        yield Footer() 


def main():
    AppHome().run()


if __name__== "__main__":
    main()