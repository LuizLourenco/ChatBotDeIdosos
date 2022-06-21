###############################
## Arquivo: main.py
## Arquivo usando como aplicação Webhook para projeto do DialogFlow
###############################

# Importando bibliotas necessarias ao projeto 
from flask import Flask, request, jsonify

# Instanciando a biblioteca Flask na variavel App
app = Flask(__name__)

#iniciando uma matriz para colecionar dados
pedidos = []

# atribuindo a instancia a rota de entrada como http://hostname/webhook e usando metodo POST para troca de mensagens 
@app.route('/webhook', methods=['POST']) 
def main():
    data = request.get_json(silent=True)

    contexts = data['queryResult']['outputContexts']
    for context in contexts:
        if 'pizzapedido-followup' in context['name']:
            parametros = context['parameters']
            sabor = parametros['sabor']
            nome = parametros['nome']['name']
            pedidos.append({ 'nome': nome, 'sabor': sabor })
    print(data)
    print(pedidos)
    data['fulfillmentText'] = 'Confirmado. Seu pedido está sendo preparado.'

    return jsonify(data)

# run Flask app
if __name__ == "__main__":
    app.debug = False
    app.run()
    