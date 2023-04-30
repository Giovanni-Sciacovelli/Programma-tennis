Python 3.11.2 (tags/v3.11.2:878ead1, Feb  7 2023, 16:38:35) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
 import RPi.GPIO as GPIO
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class TennisMatch:
    def __init__(self):
        self.player1_score = 0
        self.player2_score = 0
        self.player1_sets_won = 0
        self.player2_sets_won = 0
        self.current_set = 1
    def score_point(self, player):
        if player == 1:
            self.player1_score += 1
        elif player == 2:
            self.player2_score += 1
        if self.player1_score >= 4 and self.player1_score - self.player2_score >= 2:
            self.player1_score = 0
            self.player2_score = 0
            self.player1_sets_won += 1
        elif self.player2_score >= 4 and self.player2_score - self.player1_score >= 2:
            self.player1_score = 0
            self.player2_score = 0
            self.player2_sets_won += 1
        if self.player1_sets_won >= 6 and self.player1_sets_won - self.player2_sets_won >= 2:
            self.player1_sets_won = 0
            self.player2_sets_won = 0
            self.current_set += 1
        elif self.player2_sets_won >= 6 and self.player2_sets_won - self.player1_sets_won >= 2:
            self.player1_sets_won = 0
            self.player2_sets_won = 0
            self.current_set += 1
    def reset_game(self):
        self.player1_score = 0
        self.player2_score = 0
        self.player1_sets_won = 0
        self.player2_sets_won = 0
        self.current_set = 1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP) # bottone del giocatore 1
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # bottone del giocatore 2
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) # bottone "undo"
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # bottone "reset"

... options = RGBMatrixOptions()
... options.rows = 64
... options.cols = 64
... options.chain_length = 2
... options.hardware_mapping = 'regular'
... options.gpio_slowdown = 4
... 
... matrix = RGBMatrix(options=options)
... font = graphics.Font()
... font.LoadFont("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", 24)
... 
... match = TennisMatch()
... 
... while True:
...     if GPIO.input(11) == GPIO.LOW:
...         match.score_point(1)
...         time.sleep(0.5) # attesa per evitare il debounce
...     if GPIO.input(12) == GPIO.LOW:
...         match.score_point(2)
...         time.sleep(0.5) # attesa per evitare il debounce
...     if GPIO.input(13) == GPIO.LOW:
...         # ritorna al click precedente
...         match.player1_score = match.player1_score - 1 if match.player1_score > 0 else match.player1_score
...         match.player2_score = match.player2_score - 1 if match.player2_score > 0 else match.player2_score
...         time.sleep(0.5)
...         if GPIO.input(22) == GPIO.LOW:
...         match.reset_game()
...         time.sleep(0.5) # attesa per evitare il debounce
...     
...     # Mostra i punteggi e il set corrente sulla matrice LED
...     canvas = matrix.CreateCanvas()
...     graphics.DrawText(canvas, font, 5, 30, graphics.Color(255, 255, 255), "Player 1: " + str(match.player1_score))
...     graphics.DrawText(canvas, font, 5, 55, graphics.Color(255, 255, 255), "Player 2: " + str(match.player2_score))
...     graphics.DrawText(canvas, font, 200, 30, graphics.Color(255, 255, 255), "Set: " + str(match.current_set))
