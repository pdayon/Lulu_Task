import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import tkinter
from tkinter import *
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('Luluintents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


# This function cleans up the sentences which the user inputs in the GUI 
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# This function takes the cleaned sentences from clean_up_sentence() & creates a bag of words for predicting the classes.
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

# This function will output a list of intents & the probabilities ( How much possibility is there for matching the correct intent )
def predict_class(sentence, model):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# This function takes the list output from predict_class() & checks the JSON file & returns the most suitable answer with the highest probability.
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

# This function takes the message from the user as an input
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Arial", 8 ))
        res = chatbot_response(msg)
        ChatLog.insert(END, "Lulu Bot: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


base = Tk()
base.title("Lulu International Chatbot | Made by Ayon Roy")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)
ChatLog = Text(base, bd=0, bg="white", height="8", width="100", font="Arial",)
ChatLog.config(state=DISABLED)
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Verdana")
scrollbar.place(x=386,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=1000)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)
base.mainloop()
