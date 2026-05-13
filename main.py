from textual.app import App
from textual.widgets import Footer, Header

class AppHome(App):
    BINDINGS = [(("q", "quit", "Esci"))]
    
    def compose(self):
        yield Header()  
        yield Footer() 


def main():
    AppHome().run()


if __name__== "__main__":
    main()