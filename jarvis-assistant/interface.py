import turtle
#from jarvis_voiceassistant import speak

screen = turtle.Screen()

answer = screen.textinput("Welcome to Bowling!", "Are you ready to bowl?")

if answer is None or answer.lower().startswith('n'):
    print("Goodbye!")
    screen.clear()
    screen.bye()
else:
    print("Start!")