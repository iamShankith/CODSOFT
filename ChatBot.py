import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

class ChatBot:
    def __init__(self,intent_file,words_file,class_file,model_file):
        self.lemmatizer=WordNetLemmatizer()
        self.intents=json.loads(open(intent_file).read())
        self.words=pickle.load(open(words_file,'rb'))
        self.classes=pickle.load(open(class_file,'rb'))
        self.model=load_model(model_file)
        self.error_threshold=0.2

    def clean_up_sentence(self,sentence):
        sentence_words=nltk.word_tokenize(sentence)
        sentence_words=[self.lemmatizer.lemmatize(word)for word in sentence_words]
        return sentence_words

    def bag_of_words(self,sentence):
        sentence_words=self.clean_up_sentence(sentence)
        bag=[0]*len(self.words)
        for w in sentence_words:
            for i,word in enumerate(self.words):
                if word==w:
                    bag[i]=1
        return np.array(bag)

    def predict_class(self,sentence):
        bow=self.bag_of_words(sentence)
        res=self.model.predict(np.array([bow]))[0]
        result=[[i,r]for i,r in enumerate(res)if r>self.error_threshold]
        result.sort(key=lambda x: x[1],reverse=True)
        return [{'intent':self.classes[r[0]],"probability":str(r[1])}for r in result]

    def get_response(self,intent_list):
        tag=intent_list[0]['intent']
        list_of_inntents=self.intents['intents']
        for i in list_of_inntents:
            if i['tag']==tag:
                return random.choice(i['responses'])
        return "i am sorry,I don't undersatnd"
    
    def handel_appoint(self,action):
        if action=='schedule':
            self.schedule_appoint()
        elif action=='cancel':
            self.cancel_appoint()

    def schedule_appoint(self):
        patient_name=input("CHATBOT:Enter your NAME:")
        doctor_name=input("CHATBOT:Enter doctor's name:Dr.")
        age=input("CHATBOT:Enter your age:")
        date=input("CHATBOT:Enter the preferred date:")
        time=input("CHATBOT:Enter the prefferred time:")

        print(f"CAHTBOT:Appointment scheduled foe {patient_name} with {doctor_name} on {date} at {time}")
        print("CHATBOT:Great! Your appointment has been scheduled.")
    
    def cancel_appoint(self):
        pateint_name=input("CHATBOT:Enter your NAME:")
        doctor_name=input("CHATBOT:Enter doctor NAME:Dr.")
        print(f"CHATBOT:Appointment canceled for {pateint_name} with {doctor_name}")
        print("CHATBOT:Great! Your appointment has been canceled")

    def display_available_doctors(self):
        doctor_intent=[intent for intent in self.intents['intents'] if intent['tag']=='display_available_doctors']
        if doctor_intent:
            available_doctors=doctor_intent[0].get('doctors', [])
            if available_doctors:
                print("Available Doctors:")
                for doctor in available_doctors:
                    print(f"{doctor['name']} - {doctor['profession']}")
            else:
                print("No doctors available.")
        else:
            print("Intent not found for available doctors")
            
    def run_chat(self):
        print("GO! BOT is running")
        while True:
            message=input("You: ")
            if message.lower() in ['exit','quit']:
                print("Chatbot: shutting down...")
                break
            if not message:
                print("CHATBOT: Enter a valid input")
                continue
            intents=self.predict_class(message)
            response=self.get_response(intents)

            if intents[0]['intent']=='display_available_doctors':
                self.display_available_doctors()
            elif intents[0]['intent'] in ['schedule_appointment','cancel_appointment']:
                action=intents[0]['intent'].split('_')[0]
                self.handel_appoint(action)
            else:
                print("CHATBOT:",response)

if __name__=="__main__":
    chatbot=ChatBot('intents.json','words.pkl','classes.pkl','chatbotmodel.h5')
    chatbot.run_chat()