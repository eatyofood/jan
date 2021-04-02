from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create a new chat bot named Charlie
chatbot = ChatBot('Ron Obvious')

#import pandas as pd
#df = pd.read_csv('Bender_training.csv')


#trainer = ListTrainer(chatbot)

#trainer.train(list(df['Bender']))


#    "Hi, can I help you?",
#    "Sure, I'd like to book a flight to Iceland.",
#    "Your flight has been booked."
#])

# Get a response to the input text 'I would like to book a flight.'
#response = chatbot.get_response('I would like to book a flight.')

#while True:
def ronBot(req):
    #req = input('YOU:')
    response = chatbot.get_response(req)

    print('BOT:',response)
    return response
