from google.colab import drive
import json
import requests
import time
url_tabela_referencia = "https://veiculos.fipe.org.br/api/veiculos//ConsultarTabelaDeReferencia"
url_marcas = "https://veiculos.fipe.org.br/api/veiculos//ConsultarMarcas"
url_modelo = "https://veiculos.fipe.org.br/api/veiculos//ConsultarModelos"
url_ano_modelo = "https://veiculos.fipe.org.br/api/veiculos//ConsultarAnoModelo"
url_tabela_modelos_pelo_ano = "https://veiculos.fipe.org.br/api/veiculos//ConsultarModelosAtravesDoAno"
url_valor_parametros = "https://veiculos.fipe.org.br/api/veiculos//ConsultarValorComTodosParametros"

drive.mount('/content/gdrive')
tryies=0
def request_data_fipe(url,form):
  response = requests.post(url,data=form)
  # time.sleep(3)
  # Check if the request was successful (status code 200)
  if response.status_code == 200:
    # Try converting the response content to JSON
    try:
      # Assuming the response is in JSON format
      json_data = response.json()
      marcas = json_data
      return marcas
      # print(json_data)
    except Exception as e:
      print(e)
      return None
  else:
    print(response.status_code,response,429)
    return None


def get_veiculos_marca(idMarca,tabela):
  veiculos=[]
  form_modelos = {
    "codigoTipoVeiculo": 1,
    "codigoTabelaReferencia": tabela,
    "codigoModelo":None ,
    "codigoMarca": idMarca,
    "ano": None,
    "codigoTipoCombustivel": None,
    "anoModelo": None,
    "modeloCodigoExterno": None,
  }
  modelos_lista = request_data_fipe(url_modelo ,form_modelos)['Modelos']
  # print(modelos_lista)
  for modelo in modelos_lista:
    form_ano_modelo = {
      "codigoTipoVeiculo": 1,
      "codigoTabelaReferencia": tabela,
      "codigoModelo": modelo['Value'],
      "codigoMarca": idMarca,
      "ano": None,
      "codigoTipoCombustivel": None,
      "anoModelo": None,
      "modeloCodigoExterno": None,
    }
    ano_modelo_lista=request_data_fipe(url_ano_modelo  ,form_ano_modelo)
    # print(ano_modelo_lista)
    # print(form_ano_modelo)
    for ano_m in ano_modelo_lista:
      # print(ano_m)
      # print(ano_modelo_lista)
      form_modelos_ano = {
          "codigoTipoVeiculo": 1,
          "codigoTabelaReferencia": tabela,
          "codigoModelo": modelo['Value'],
          "codigoMarca": idMarca,
          "ano": ano_m['Value'],
          "codigoTipoCombustivel": ano_m['Value'].split('-')[1],
          "anoModelo": ano_m['Value'].split('-')[0],
          "modeloCodigoExterno":None
      }
      ####
      modelo_ano_lista=request_data_fipe(url_tabela_modelos_pelo_ano,form_modelos_ano)
      # print(modelo_ano_lista)
      # print(form_modelos_ano)
      for modelo_a in modelo_ano_lista:

        form_valor_tabela={
            "codigoTabelaReferencia": tabela,
            "codigoMarca": idMarca,
            "codigoModelo": modelo_a['Value'],
            "codigoTipoVeiculo": 1,
            "anoModelo": ano_m['Value'].split('-')[0],
            "codigoTipoCombustivel": ano_m['Value'].split('-')[1],
            "tipoVeiculo": None,
            "modeloCodigoExterno": None,
            "tipoConsulta": 'tradicional',
        }
        veiculo_I=request_data_fipe(url_valor_parametros ,form_valor_tabela)
        veiculos.append(veiculo_I)
        print(len(veiculos)%20)
        if len(veiculos)%20==0:
          time.sleep(30)
        # print(veiculo_I)
        # print(veiculo_I,0)
      # print(modelo_ano_lista,0)

  return veiculos


# itens=get_veiculos_marca( marcas[0]['Value'])
# print(itens)
t =[310,298,286,271,256,243,230,214,192,180,167]
tbl=t[0]
form_data_marcas = {
     "codigoTabelaReferencia": tbl,
    "codigoTipoVeiculo": 1
}
marcas = request_data_fipe(url_marcas,form_data_marcas)
# tabelas = request_data_fipe(url_tabela_referencia,None)
# print(tabelas)
# print(marcas)
marca1= filter(lambda x: x['Label']  == 'Fiat', marcas)
# print(list(marca1))

for marca in list(marca1):
  print(marca)

  # try:
  itens=[]
  itens=get_veiculos_marca(marca['Value'],tbl)
  with open(f"/content/gdrive/My Drive/FIPE/carros_utilitarios/{marca['Label'].replace('/','_')}_{tbl}.json", "w") as file:
      file.write(json.dumps(itens))
  time.sleep(30)
  # except Exception as e:
  #   print("erro",marca,e)