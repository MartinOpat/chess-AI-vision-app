import chess
import chess.svg
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
import cairosvg

class ChessBoardApp(App):
    font_size = NumericProperty(sp(18))  # Initial font size in scale-independent pixels

    def build(self):
        self.board = chess.Board()
        self.filepath = ''  # Initialize the filepath variable
        layout = BoxLayout(orientation='vertical')

        # Chess board image
        self.img = Image(keep_ratio=True, allow_stretch=True)
        layout.add_widget(self.img)

        # Input for moves
        self.input = TextInput(hint_text='Enter move (e.g., e2e4)', multiline=False, size_hint=(1, 0.1), font_size=self.font_size)
        self.input.bind(on_text_validate=self.on_enter)
        layout.add_widget(self.input)

        # Button to submit move
        self.button = Button(text='Make Move', size_hint=(1, 0.1), font_size=self.font_size)
        self.button.bind(on_press=self.make_move)
        layout.add_widget(self.button)

        # Button to load image file
        load_button = Button(text='Load Image', size_hint=(1, 0.1), font_size=self.font_size)
        load_button.bind(on_press=self.show_load)
        layout.add_widget(load_button)

        # Bind the font size property to window size changes for dynamic scaling
        self.bind(font_size=self.update_font_size)
        self.update_board()
        return layout

    def update_board(self):
        svg_data = chess.svg.board(self.board).encode('utf-8')
        png_data = cairosvg.svg2png(bytestring=svg_data)
        with open("board.png", "wb") as png_file:
            png_file.write(png_data)
        self.img.source = 'board.png'
        self.img.reload()

    def make_move(self, instance):
        try:
            move = self.board.parse_san(self.input.text)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_board()
                self.input.text = ''  # Clear the input after a move
        except ValueError:
            self.input.text = 'Invalid move!'  # Provide feedback on invalid input

    def on_enter(self, instance):
        self.make_move(None)  # Use the make_move function directly, with instance as None

    def show_load(self, instance):
        content = FileChooserIconView()
        content.bind(on_selection=self.load_image)
        popup = Popup(title="Select image", content=content, size_hint=(0.9, 0.9))
        popup.open()

    def load_image(self, filechooser):
        if filechooser.selection:
            self.filepath = filechooser.selection[0]
            print("Selected file:", self.filepath)  # Debug print to verify file path

    def update_font_size(self, instance, value):
        # Update the font size of text input and all buttons based on window size
        self.input.font_size = value
        self.button.font_size = value
        self.load_button.font_size = value

if __name__ == "__main__":
    ChessBoardApp().run()
