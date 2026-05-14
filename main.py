import argparse
from pathlib import Path
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
    
    def __init__(self, source_text: str):
        super().__init__()
        self.source_text = source_text 
    
    def compose(self):
        """Create the UI structure."""
        yield Header()
        
        with Container(id="button-container"):
            yield Button("REPLACE", id="replace-button")
        
        # Comparison area
        with Horizontal(id="main-body"):
            with VerticalScroll(id="source-text-raw", classes="text-box"):
                yield Static("SOURCE TEXT (WITH ERRORS)...\n"+self.source_text)
            with VerticalScroll(id="source-text-corrected", classes="text-box"):
                yield Static("SOURCE TEXT (WITH CORRECTIONS)...")
        
        # Bottom area for analysis
        with VerticalScroll(id="bottom-section"):
            yield Static("ANALYSIS ERROR...")
         
        yield Footer() 


def main():
    parser = argparse.ArgumentParser()
    
    # Create the argument that accepts the file
    parser.add_argument(
        "-f", "--file", 
        type=Path,       # <-- Tells argparse that this is a file path
        # TODO: Uncomment 'required=True' to make the file argument mandatory in production.        
        # required=True,   # <-- True if the file is mandatory to start the app
        help="Path to the original file to analyze (supports .txt and .md)"
    )
    
    args = parser.parse_args()
    
    # TODO: Remove this entire if/else block before final release.
    # It is currently used to inject a default testing string when no file is provided.    
    
    if args.file:
        # Check if the file actually exists on the computer
        if not args.file.exists() or not args.file.is_file():
            print(f"Error: The file '{args.file}' does not exist.")
            return # Stops execution
        
        # Find out what type of file it is using ".suffix"
        extension = args.file.suffix.lower() # Returns '.txt', '.md', etc.
        
        if extension == '.md':
            # Read and prepare your Markdown file here
            extracted_text = args.file.read_text(encoding='utf-8')
            # (Any other specific operations for Markdown)
            
        elif extension == '.txt':
            # Read and prepare your Text file here
            extracted_text = args.file.read_text(encoding='utf-8')
            
        else:
            # If the user passes a .pdf, .docx or other file, we stop them
            print(f"Error: Format '{extension}' is not supported. Use only .txt or .md")
            return
    else:
        extracted_text = """# The Solar System 🪐
        
The Solar System is the planetary system in which our Earth is located. It consists of the Sun and all the celestial bodies that orbit around it, kept in motion by its immense gravitational pull.

### The Main Planets
The planets are divided into two main categories:
* **Terrestrial planets:** Mercury, Venus, Earth, and Mars. They are relatively small, have a solid rocky surface, and are located closer to our star.
* **Gas giants:** Jupiter, Saturn, Uranus, and Neptune. They are enormous and composed mainly of gas and ice.

> "Astronomy compels the soul to look upwards and leads us from this world to another."
> *— Plato*

**Some space facts:**
1. The Sun alone contains about `99.8%` of all the mass in the entire Solar System.
2. A single day on Venus lasts longer than an entire Venusian year.
3. Saturn is not the only planet to have rings, but its rings are by far the most spectacular and visible.
"""
    
    
    
    app_home = AppHome(source_text=extracted_text)
    app_home.run()


if __name__== "__main__":
    main()