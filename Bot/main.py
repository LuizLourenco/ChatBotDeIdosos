#######################################################################################
## Webhook desenvolvido para comunicar com o DialogFlow 
## e assim trazer dados da DF para webhook processar dados esperciais ou registralos em banco de dados.
#######################################################################################

from flask import Flask, request, jsonify

app = Flask(__name__)


pedidos = []

@app.route('/', methods=['POST'])
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