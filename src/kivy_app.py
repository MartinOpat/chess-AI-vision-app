import chess
import chess.svg
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
import cairosvg
from image_to_board import ImageToBoard
from engine import PychessBot
import os
from time import sleep
import signal

class ChessBoardApp(App):
    font_size = NumericProperty(sp(18))  # Initial font size in scale-independent pixels

    def build(self):
        self.bind(font_size=self.update_font_size)  # Ensure the binding is at app level, not window
        Window.bind(on_request_close=self.on_request_close)  # Bind closing event

        self.board = chess.Board()
        self.bot = PychessBot('src/stockfish/stockfish-ubuntu-x86-64-avx2')
        self.filepath = ''
        layout = BoxLayout(orientation='vertical')

        self.img = Image(keep_ratio=True, allow_stretch=True)
        layout.add_widget(self.img)

        self.message_label = Label(text='No image loaded', size_hint=(1, 0.1), font_size=self.font_size)
        layout.add_widget(self.message_label)

        self.input = TextInput(hint_text='Enter move (e.g., e2e4)', multiline=False, size_hint=(1, 0.1), font_size=self.font_size)
        self.input.bind(on_text_validate=self.on_enter)
        layout.add_widget(self.input)

        self.button = Button(text='Make Move', size_hint=(1, 0.1), font_size=self.font_size)
        self.button.bind(on_press=self.make_move)
        layout.add_widget(self.button)

        self.load_button = Button(text='Load Image', size_hint=(1, 0.1), font_size=self.font_size)
        self.load_button.bind(on_press=self.show_load)
        layout.add_widget(self.load_button)

        self.bot_button = Button(text='Ask Bot for Move', size_hint=(1, 0.1), font_size=self.font_size)
        self.bot_button.bind(on_press=self.ask_bot)
        layout.add_widget(self.bot_button)

        button_layout = BoxLayout(size_hint=(1, 0.1))  # Container for toggle and new button
        self.toggle_turn_button = Button(text='Toggle Turn', size_hint=(1, 1), font_size=self.font_size)
        self.toggle_turn_button.bind(on_press=self.toggle_turn)
        button_layout.add_widget(self.toggle_turn_button)

        self.us = 1  # White by default
        self.us_button = Button(text='Switch to Black View', size_hint=(1, 1), font_size=self.font_size)
        self.us_button.bind(on_press=self.switch_us)
        button_layout.add_widget(self.us_button)
        layout.add_widget(button_layout)


        self.update_board()
        return layout
    
    def on_start(self):
        Window.bind(size=self.adjust_font_size)

    def on_request_close(self, *args):
        self.stop()  # Cleanly stop the application
        self.bot.engine.quit()
        return True

    def update_board(self, fen=None):
        if fen:
            try:
                self.board.set_fen(fen)
            except ValueError:
                self.message_label.text = "Invalid FEN string from image."
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

    def ask_bot(self, instance):
        fen = self.board.fen()
        best_move = self.bot(fen)  # Call the PychessBot with the current FEN
        self.message_label.text = f"Bot suggests move: {best_move}"  # Display the bot's suggested move

    def toggle_turn(self, instance):
        # Toggle whose turn it is
        if ' w ' in self.board.fen():
            new_fen = self.board.fen().replace(' w ', ' b ')
        else:
            new_fen = self.board.fen().replace(' b ', ' w ')
        self.board.set_fen(new_fen)
        self.update_board()  # Update the board to reflect the change
        self.message_label.text = "Turn toggled."  # Update message label

    def switch_us(self, instance):
        self.us = 1 - self.us
        if self.us == 1:
            self.us_button.text = 'Switch to Black View'
        else:
            self.us_button.text = 'Switch to White View'

        if self.filepath:
            fen = ImageToBoard(self.filepath)(us=self.us)
            if fen:
                self.update_board(fen)
                self.message_label.text = f"Image {self.filepath} has been loaded and board updated."
            else:
                self.message_label.text = "No valid chess board found in the image."
            self.update_board()

    def on_enter(self, instance):
        self.make_move(None)

    def show_load(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView()
        content.add_widget(filechooser)

        button_layout = BoxLayout(size_hint_y=None, height='50sp')
        load_btn = Button(text='Load')
        load_btn.bind(on_release=lambda x: self.load_image(filechooser, popup))
        button_layout.add_widget(load_btn)

        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_release=lambda x: popup.dismiss())
        button_layout.add_widget(cancel_btn)

        content.add_widget(button_layout)
        popup = Popup(title="Select image", content=content, size_hint=(0.9, 0.9))
        popup.open()

    def load_image(self, filechooser, popup):
        if filechooser.selection:
            self.filepath = filechooser.selection[0]
            fen = ImageToBoard(self.filepath)(us=self.us)
            if fen:
                self.update_board(fen)
                self.message_label.text = f"Image {self.filepath} has been loaded and board updated."
            else:
                self.message_label.text = "No valid chess board found in the image."
        popup.dismiss()

    def adjust_font_size(self, instance, value):
        new_size = sp(18) + (Window.width - 500) / 100
        self.font_size = new_size

    def update_font_size(self, instance, value):
        # Update all widgets' font sizes
        self.input.font_size = value
        self.button.font_size = value
        self.load_button.font_size = value
        self.message_label.font_size = value
        self.bot_button.font_size = value
        self.toggle_turn_button.font_size = value
        self.us_button.font_size = value

