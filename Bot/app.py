###############################
## Arquivo: app.py
## Arquivo usando como aplicação Webhook para projeto do DialogFlow
###############################

# Importando bibliotas necessarias ao projeto 
from flask import Flask, request, jsonify

# Instanciando a biblioteca Flask na variavel App
app = Flask(__name__)

#iniciando uma matriz para colecionar dados

# atribuindo a instancia a rota de entrada como http://ajudaidoso.app.br:5000/ e usando metodo POST para troca de mensagens 
@app.route('/', methods=['POST']) 
def main():
    data = request.get_json(silent=True)

    contexts = data['queryResult']['outputContexts']
    for context in contexts:
        if 'input.welcome' in context['name']:
            parametros = context['parameters']
            nomeDoUsuario = parametros['nomeDoUsuario']
    print(nomeDoUsuario+" acabou de chegar")
    ##data['fulfillmentText'] = 'Devolvendo uma mensagem para Chat'
    return jsonify(data)
# run Flask app
if __name__ == "__main__":
    app.debug = False
    app.run()