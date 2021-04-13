# Importa as Credenciais
from keys import *

# Dependencias
import locale
import tweepy
import filecmp
from shutil import copyfile

###############################################################################

# Configura as autorizações da Conta do Twitter
def configure_authorization_keys():
    global AUTH
    global API
    AUTH = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    AUTH.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    API = tweepy.API(AUTH)

# -----------------------------------------------------------------------------------
# Faz o tweet

def make_tweet():

    dados = []

    # Recolhe os dados
    with open("outFile") as origin_file:
        for line in origin_file:
            dados.append(line)
           
    # print(dados)

    data_atualizacao  = dados[0]
    casos_ativos      = dados[2]
    casos_confirmados = dados[4]
    obitos            = dados[6]
    leitos_livres     = dados[8]
    ocupacao          = dados[10]

    data_vacinacao    = dados[13]
    primeira_dose     = int(dados[15])
    segunda_dose      = int(dados[17])

    bandeira_atual    = dados[18]
     

    status = data_atualizacao + '\n' + \
            "Situação Atual\n" + bandeira_atual               + '\n' + \
            "Casos ativos\n"   + casos_ativos                 + '\n' + \
            "Confirmados\n"   + casos_confirmados             + '\n' + \
            "Óbitos\n"         + obitos                       + '\n' + \
            "Ocupação UTI\n"   + ocupacao                     + '\n' + \
            "Leitos Livres\n"  + leitos_livres                + '\n' + \
            "\nVACINACAO"                                     + '\n' + \
            data_vacinacao                                    + '\n' + \
            "Primeira Dose\n"  + '{:n}'.format(primeira_dose) + '\n' + \
            "Segunda Dose\n"   + '{:n}'.format(segunda_dose)
    

    status_file = open("status/current_status", "w+")
    status_file.write(status)
    status_file.close()
    print(status)

    if(filecmp.cmp("status/current_status", "status/old_status", shallow=True)):
        print("Sem Atualizações")
    else:
        # Posta o tweet
        API.update_status(status)
        # Atualiza o ultimo status postado
        copyfile("status/current_status", "status/old_status")
        print(status)

# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# MAIN

locale.setlocale(locale.LC_ALL,'')
configure_authorization_keys()
make_tweet()
