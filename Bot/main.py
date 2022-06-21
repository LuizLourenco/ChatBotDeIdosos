#######################################################################################
## Webhook desenvolvido para comunicar com o DialogFlow 
## e assim trazer dados da DF para webhook processar dados esperciais ou registralos em banco de dados.
#######################################################################################

#Importando bibliotacas 
from flask import Flask, request, jsonify

#instanciando o objeto com as bibliotecas flask
app = Flask(__name__)

#pedidos = []

#instanciando a chamada da qual endereco sera conhecido e seu metodo de comunicacao
@app.route('/webhook', methods=['POST'])
def main(): 
    dfData = request.get_json(silent=True)
    contexts = dfData['queryResult']['outputContexts'] # coletando as interações e seus contextos do DF na varial contexts

    for context in contexts: 
        #if 'pizzapedido-followup' in context['name']:
        #    parametros = context['parameters']
        #    sabor = parametros['sabor']
        #    nome = parametros['nome']['name']
        #    #pedidos.append({ 'nome': nome, 'sabor': sabor })

    
    print(dfData)
    #print(pedidos)
    
    #Devolvendo uma mensagem para DialogFlow 
    #Essa mensagem será apresentada ao usuário
    dfData['fulfillmentText'] = 'Essa e uma msg do webhook'
    return jsonify(dfData)


# run Flask app
if __name__ == "__main__":
    app.run(Debug=TRUE)