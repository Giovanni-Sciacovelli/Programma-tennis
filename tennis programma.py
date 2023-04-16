Python 3.11.2 (tags/v3.11.2:878ead1, Feb  7 2023, 16:38:35) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import pin2dmd
import RPi.GPIO as GPIO
import time

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

match = TennisMatch()

while True:
    if GPIO.input(11) == GPIO.LOW:
        match.score_point(1)
        time.sleep(0.5) # attesa per evitare il debounce

    if GPIO.input(12) == GPIO.LOW:
        match.score_point(2)
        time.sleep(0.5) # attesa per evitare il debounce

    if GPIO.input(13) == GPIO.LOW:
        # ritorna al click precedente
        match.player1_score = match.player1_score - 1 if match.player1_score > 0 else match.player1_score
        match.player2_score = match.player2_score - 1 if match.player2_score > 0 else match.player2_score
        time.sleep(0.5) # attesa per evitare il debounce

    if GPIO.input(22) == GPIO.LOW:
        # riavvia il gioco
        match.reset_game()
        time.sleep(0.5) # attesa per evitare il debounce


display1 = pin2dmd.Pin2DMD(1) # il primo parametro è il numero del primo dispositivo
display2 = pin2dmd.Pin2DMD(2) # il primo parametro è il numero del secondo dispositivo

# crea un'immagine vuota per inizializzare le matrici
empty_image = pin2dmd.create_image((64, 64), mode='RGB')

# definisci i colori utilizzati per il punteggio e il testo
white = (255, 255, 255)


# definisci le coordinate per il punteggio del giocatore 1
player1_score_x = 10
player1_score_y = 22

# definisci le coordinate per il punteggio del giocatore 2
player2_score_x = 42
player2_score_y = 22

# variabili per il punteggio dei giocatori
player1_score = 0
player2_score = 0

# variabili per il numero di set vinti dai giocatori
player1_sets_won = 0
player2_sets_won = 0
current_set = 1

# variabili per il numero di volte consecutive in cui un giocatore ha fatto punto
player1_consecutive_points = 0
player2_consecutive_points = 0

while True:
    # aggiorna l'immagine con il punteggio corrente
    image1 = empty_image
    image2 = empty_image

    # disegna il punteggio del giocatore 1
    for i in range(player1_score):
        image1[player1_score_x + i][player1_score_y] = white
        image2[player1_score_x + i][player1_score_y] = white

    # disegna il punteggio del giocatore 2
    for i in range(player2_score):
        image1[player2_score_x + i][player2_score_y] = white
        image2[player2_score_x + i][player2_score_y] = white

    # disegna il numero di set vinti dal giocatore 1
    for i in range(player1_sets_won):
        for j in range(4):
            image1[4 + i*8 + j][2] = white
            image2[4 + i*8 + j][2] = white

    # disegna il numero di set vinti dal giocatore 2
    for i in range(player2_sets_won):
        for j in range(4):
            image1[4 + i*8 + j][60] = white
