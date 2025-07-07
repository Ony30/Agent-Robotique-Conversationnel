# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time
import os
import subprocess
import requests

class QAModule(object):
    def __init__(self):
        self.nao_ip = "192.168.1.103"
        self.nao_port = 9559
        self.api_url = "http://192.168.1.100:8000/predict"
        
        try:
            self.tts = ALProxy("ALTextToSpeech", self.nao_ip, self.nao_port)
            self.dialog = ALProxy("ALDialog", self.nao_ip, self.nao_port)
            self.memory = ALProxy("ALMemory", self.nao_ip, self.nao_port)
            
            self.dialog.setLanguage("French")
            
            # Créer et copier le fichier .top
            self.create_topic_file()
            self.copy_topic_to_robot()
            
            topf_path = "/home/nao/dialogs/dialogRules_frf.top"
            self.topic = self.dialog.loadTopic(topf_path.encode('utf-8'))
            print("Topic chargé avec succès")
            
        except Exception as e:
            print("Erreur d'initialisation:", str(e))
            raise

    def create_topic_file(self):
        topic_content = """topic: ~Madagascar()
language: frf

# Accueil
u:(Nao Bonjour) Bonjour! Je suis prêt à répondre à vos questions sur Madagascar.

# Questions sur Madagascar
u:(Ou se trouve Madagascar?) $onShotWord="Ou se trouve Madagascar?"

u:(Quelle est la superficie  de Madagascar) $onShotWord="uelle est la superficie  de Madagascar"

u:(Combien d'habitants compte Madagascar) $onShotWord="Combien d'habitants compte Madagascar"

u:(À quel continent Madagascar est-il rattaché géographiquement) $onShotWord="À quel continent Madagascar est-il rattaché géographiquement"

u:(Quelle est la capitale  de Madagascar) $onShotWord="Quelle est la capitale de la république de Madagascar"

u:( Qui est l'actuel président de la republique ) $onShotWord=" Qui est l'actuel président de la republique 2019"

u:(Quelle est la nationalité des touristes qui visitent le plus Madagascar) $onShotWord="Quelle est la nationalité des touristes qui visitent le plus Madagascar"

# Capture des autres questions
u:(_*) $onShotWord=$1
"""
        with open("dialogRules_frf.top", "w") as f:
            f.write(topic_content)
        print("Fichier .top créé localement")

    def copy_topic_to_robot(self):
        try:
            cmd = "scp dialogRules_frf.top nao@{0}:/home/nao/dialogs/".format(self.nao_ip)
            retcode = subprocess.call(cmd, shell=True)
            if retcode == 0:
                print("Fichier .top copié sur le robot")
            else:
                raise Exception("Erreur SCP")
        except Exception as e:
            print("Erreur lors de la copie du fichier:", str(e))
            raise

    def get_answer_from_api(self, question):
        try:
            if isinstance(question, unicode):
                question = question.encode('utf-8')
                
            response = requests.post(self.api_url, json={"question": question})
            if response.status_code == 200:
                data = response.json()
                return data["answer"]
            else:
                print("Erreur API:", response.status_code)
                return None
        except Exception as e:
            print("Erreur lors de l'appel API:", str(e))
            return None

    def process_question(self):
        try:
            current_value = self.memory.getData("onShotWord")
            if current_value is not None and current_value != "":
                print("Question reçue:", current_value)
                
                # Obtenir la réponse de l'API
                answer = self.get_answer_from_api(current_value)
                
                if answer:
                    print("Réponse de l'API:", answer)
                    if isinstance(answer, unicode):
                        answer = answer.encode('utf-8')
                    print(answer)
                    self.tts.say(str(answer))
                else:
                    self.tts.say("Désolé, je n'ai pas pu obtenir de réponse")
                
                # Réinitialiser la valeur
                self.memory.insertData("onShotWord", None)
            
        except Exception as e:
            print("Erreur:", str(e))

    def start(self):
        try:
            self.dialog.activateTopic(self.topic)
            self.dialog.subscribe('qa_module')
            print("Module démarré. Ctrl+C pour quitter.")
            self.memory.insertData("onShotWord", "")
            
            while True:
                self.process_question()
                time.sleep(1)
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        self.dialog.deactivateTopic(self.topic)
        self.dialog.unloadTopic(self.topic)
        self.dialog.unsubscribe('qa_module')
        try:
            os.remove("dialogRules_frf.top")
        except:
            pass

if __name__ == '__main__':
    module = QAModule()
    module.start()