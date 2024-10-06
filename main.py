import requests
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("CLASH_API_KEY")
mongo_uri = os.getenv("MONGO_URI")

headers = {
    "Authorization": f"Bearer {api_key}"
}

player_tag = "9ULPU0QL"  

url_player = f"https://api.clashroyale.com/v1/players/%23{player_tag}"
url_battlelog = f"https://api.clashroyale.com/v1/players/%23{player_tag}/battlelog"

# requisição jogador
response_player = requests.get(url_player, headers=headers)

# requisição batalhas recentes
response_battles = requests.get(url_battlelog, headers=headers)

# verificação das requisições
if response_player.status_code == 200 and response_battles.status_code == 200:
    player_data = response_player.json()
    battles_data = response_battles.json()
    print("Dados do jogador e batalhas obtidos com sucesso!")
    
    # conectando ao mongo
    client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
    db = client['clashroyale'] 
    
    # coleção de jogadores
    players_collection = db['players']
    
    # coleção de batalhas recentes
    battles_collection = db['battles']
    
    # inserção de dados no banco
    players_collection.insert_one(player_data)
    
    for battle in battles_data:
        battles_collection.insert_one(battle)
    
    print("Dados do jogador e batalhas inseridos no MongoDB Atlas!")
    
    client.close()

elif response_player.status_code == 404:
    print("Erro 404: Jogador não encontrado.")
else:
    print(f"Erro: {response_player.status_code}, {response_battles.status_code}")
