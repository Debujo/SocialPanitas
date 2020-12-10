import tweepy, time, os
import pandas as pd

from string import *
from twitter_keys import *


def csv_save(df):
    name = str("datos_usuarios.csv")
    if data_save == True:
        df.to_csv(data_location + name)
        sleep(0.3)
    else:
        try:
            os.remove(data_location + name)
        except OSError:
            pass

def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def check():
    new_since_id = since_id
    list_dms = api.list_direct_messages(since_id = since_id)

    for dm in list_dms:
        user_id = dm.message_create['sender_id']
        user = api.get_user(user_id = user_id)
        new_since_id = max(int(dm.id), int(new_since_id))

        if user.id != me.id:
            if any(keyword in dm.message_create['message_data']['text'].lower() for keyword in keywords1):
                message1 = message_template.substitute(PERSON_NAME=user.name)
                api.send_direct_message(recipient_id=user.id, text = str(message1))
                api.send_direct_message(recipient_id=user.id, text = str(ejemplo))
                print("First message sent to: "+str(user.name))
            if any(keyword in dm.message_create['message_data']['text'].lower() for keyword in keywords2):
                texto0 = dm.message_create['message_data']['text'].lower().replace("\n",":")
                texto = texto0.split(":")
                api.send_direct_message(recipient_id=user.id, text = message2)
                print("Second message sent to: "+str(user.name))
                try:
                    data = {'user_id':  [str(user_id)],
                            'user_name': [str(user.name)],
                            'genero': [texto[1]],
                            'rango_edad': [texto[3]],
                            'objetivo': [texto[5]]
                            }
                    df = pd.DataFrame (data, columns = ['user_id','user_name','genero','rango_edad','objetivo'])
                    csv_save(df)
                except:
                    continue
keywords1 = ["information", "info", "informacion", "about", "hello", "hola", "holaa", "ey", "quiero", "comenzar",
            "entrar", "socializar", "SocialPanitas"]
keywords2 = ["rango", "edad", "objetivo"]

data_save = True
data_location = 'C:/Users/ignac/pyprojects/SocialPanitas/SocialPanitas/'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
me = api.me()

message_template = read_template('message1.txt')
ejemplo = "Por favor, rellenalo como en el siguiente ejemplo: \nGENERO: 2 \nRANGO EDAD: 2 \nOBJETIVO: 1"
message2 = "En las próximas 24h te mandaremos un enlace con el que serás introducido a la comunidad de SocialPanitas."
since_id = 1322982087625003012

check()

"""
#while True:
#    # check()
#    time.sleep(300) #Actualización cada 5 mins
"""
