#
# Blackjack Game, graphics version
#

image_path="./blackJack/"

import random
import time
import sys
from cs1graphics import *

FACES = range(2, 11) + ['Jack', 'Queen', 'King', 'Ace' ]
SUITS = [ 'Clubs', 'Diamonds', 'Hearts', 'Spades' ]
CARD_SIZE = (40, 80)

# --------------------------------------------------------------------

"""A card has a face and suit."""
class Card(object):

  """A card need to have an image"""
  def __init__(self, suit, face):
      self.face = face
      self.suit = suit
      self.image = Image(image_path + str(self.suit) + "_" + str(self.face) + ".gif")

  """Returns the string of a card (example : "8 of Diamonds") """
  def __str__(self):
      return str(self.face) + " of " + self.suit

  """Returns the face value of the card."""
  def value(self):
      if ((self.face == 'JACK') or (self.face == 'Queen') or (self.face == 'King')):
          return 10
      elif (self.face == 'Ace'):
          return 11
      else:
          return int(self.face)
# --------------------------------------------------------------------

"""A deck of cards."""
class Deck(object):

  """Create a deck of 52 cards and shuffle them."""
  def __init__(self):
      self.card = []
      for i in range(len(SUITS)):
          for j in range(len(FACES)):
              self.card.append([SUITS[i],FACES[j]])
      random.shuffle(self.card)

  """Draw the top card from the deck."""
  def draw(self):
      return self.card.pop()
# --------------------------------------------------------------------

"""Graphical representation of a card."""
class CardGraphics(object):

  def __init__(self, card, hidden = False):
    self.l = Layer()      #layer for a card image
    self.hidden = hidden  # False : hidden card, True : visible card

    self.bg = Image(image_path+"Back.gif")
    if hidden:
      self.bg.setDepth(0)
      self.l.add(self.bg)

    self.l.add(card.image)

  def show(self):
    """make a hidden card visible"""
    self.bg.setDepth(100)

# --------------------------------------------------------------------

"""A hand of cards displayed on a table."""
class Hand(object):

  """Create an empty hand displayed at indicated position on canvas."""
  def __init__(self, x, y, canvas):
      self.hand = Layer()
      self.handList = []
      self.graphics = []
      self.hand.moveTo(x,y)
      canvas.add(self.hand)

  """Make hand empty."""
  def clear(self):
      #not yet
      self.hand.remove(1)

  """Add a new card to the hand."""
  def add(self, card, hidden = False):
      self.card = Card(card[0],card[1])
      self.handList.append(self.card)
      if (hidden == True):
          self.graphics.append(CardGraphics(self.card, True))
      elif (hidden == False):
          self.graphics.append(CardGraphics(self.card, False))

  """Make a hidden card(first card) in his hand visible."""
  def show(self):
      self.graphics[0].CardGraphics.show()

  """Return value of the hand."""
  def value(self):
      return self.handList[0].value() + self.handList[1].value()

# --------------------------------------------------------------------

"""A graphical Blackjack for playing Blackjack."""
class Table(object):
  def __init__(self):
    self.canvas = Canvas(600, 400, 'dark green', 'Black Jack')
    self.player = Hand(CARD_SIZE[0], CARD_SIZE[1], self.canvas)
    self.dealer = Hand(CARD_SIZE[0], 3 * CARD_SIZE[1], self.canvas)

    self.score = [ Text(), Text() ]
    for i in range(2):
      self.score[i].setFontColor('white')
      self.score[i].setFontSize(20)
      self.score[i].moveTo(self.canvas.getWidth() - CARD_SIZE[0], CARD_SIZE[1])
      self.canvas.add(self.score[i])
    self.score[1].move(0, 2 * CARD_SIZE[1])

    self.message = Text()
    self.message.setFontColor('red')
    self.message.setFontSize(20)
    dim = self.message.getDimensions()
    self.message.moveTo(self.canvas.getWidth() / 2 - dim[0] / 2,
                        self.canvas.getHeight() - 80)
    self.canvas.add(self.message)

    self.question = Text()
    self.question.setFontColor('white')
    self.question.setFontSize(20)
    dim = self.question.getDimensions()
    self.question.moveTo(self.canvas.getWidth() / 2 - dim[0] / 2,
                        self.canvas.getHeight() - 40)
    self.canvas.add(self.question)
    #time.sleep(5)

  def clear(self):
    """Clear everything on the table."""
    self.player.clear()
    self.dealer.clear()
    self.message.setMessage("")
    self.question.setMessage("")
    for i in range(2):
      self.score[i].setMessage("")

  def set_score(self, which, text):
      self.score[which].setMessage(text)

  def show_message(self, text):
      self.message.setMessage(text)

  def ask(self, prompt):
    self.question.setMessage(prompt)
    while True:
      e = self.canvas.wait()
      d = e.getDescription()
      if d == "canvas close":
        sys.exit(1)
      if d == "keyboard":
        key = e.getKey()
        print key
        if key == 'y':
          self.question.setMessage(prompt+" "+key)
          #time.sleep(30)
          return True
        if key == 'n':
          self.question.setMessage(prompt+" "+key)
          #time.sleep(30)
          self.question.setMessage("")
          return False

# --------------------------------------------------------------------

def blackjack(table):
  """Play one round of Blackjack.
  Returns 1 if player wins, -1 if dealer wins, and 0 for a tie."""

  deck = Deck()

  # initial two cards
  table.player.add(deck.draw())
  table.dealer.add(deck.draw(), True) # deal the hidden card of dealer
  table.player.add(deck.draw())
  table.dealer.add(deck.draw())
  table.set_score(0, str(table.player.value()))

  # player's turn to draw cards

  while table.player.value() < 21:
    if not table.ask("Would you like another card?"):
      break

    table.player.add(deck.draw())
    table.set_score(0, str(table.player.value()))

  # if the player's score is over 21, the player loses immediately.
  if table.player.value() > 21:
    table.show_message("You went over 21! You lost!")
    table.dealer.show()  # make the hidden card of dealer visible
    return -1
  table.set_score(1, str(table.dealer.value()))
  while table.dealer.value() < 17:
    table.dealer.add(deck.draw())
    table.set_score(1, str(table.dealer.value()))

  player_total = table.player.value()
  dealer_total = table.dealer.value()

  if dealer_total > 21:
    msg = "The dealer went over 21! You win!"
    result = 1
  elif player_total > dealer_total:
    msg = "You win!"
    result = 1
  elif player_total < dealer_total:
    msg = "You lost!"
    result = -1
  else:
    msg = "You have a tie!"
    result = 0

  table.dealer.show()  # make the hidden card of dealer visible
  table.show_message(msg)
  return result

# --------------------------------------------------------------------

def game_loop():
	table = Table()
	while True:
		time.sleep(1)
		blackjack(table)
		if not table.ask("Another round?"):
			break
		table.clear()
	table.close()
	return
game_loop()

# --------------------------------------------------------------------
