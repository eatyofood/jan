from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer#ListTrainer

# Create a new chat bot named Charlie
chatbot = ChatBot('Ron Obvious')

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train('chatterbot.corpus.english')
#    [
#    "Hi, can I help you?",
#    "Sure, I'd like to book a flight to Iceland.",
#    "Your flight has been booked."
#])

# Get a response to the input text 'I would like to book a flight.'
response = chatbot.get_response('I would like to book a flight.')

while True:
    req = input('YOU:')
    response = chatbot.get_response(req)

    print('BOT:',response)
