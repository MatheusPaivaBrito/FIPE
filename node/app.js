var url_tabela_referencia = "https://veiculos.fipe.org.br/api/veiculos//ConsultarTabelaDeReferencia"
var url_marcas = "https://veiculos.fipe.org.br/api/veiculos//ConsultarMarcas"
var url_modelo = "https://veiculos.fipe.org.br/api/veiculos//ConsultarModelos"
var url_ano_modelo = "https://veiculos.fipe.org.br/api/veiculos//ConsultarAnoModelo"
var url_tabela_modelos_pelo_ano = "https://veiculos.fipe.org.br/api/veiculos//ConsultarModelosAtravesDoAno"
var url_valor_parametros = "https://veiculos.fipe.org.br/api/veiculos//ConsultarValorComTodosParametros"

const axios = require('axios');
const fs = require('fs');

// Função para enviar JSON e salvar a resposta em um arquivo
async function request_data_fipe(url, jsonData) {
        const response = await axios.post(url, jsonData);
        if (response.status === 200) {
            return response.data
        }else{
            return null
        }
    }

async function get_veiculos_marca(idMarca,tabela){
    const vaiculos=[]
    const form_modelos = {
    "codigoTipoVeiculo": 1,
    "codigoTabelaReferencia": tabela,
    "codigoModelo":null ,
    "codigoMarca": idMarca,
    "ano": null,
    "codigoTipoCombustivel": null,
    "anoModelo": null,
    "modeloCodigoExterno": null,
    };
    modelos_lista = await request_data_fipe(url_modelo ,form_modelos)
    for (var i = 0; i < modelos_lista['Modelos'].length; i++) {
      const form_ano_modelo = {
        "codigoTipoVeiculo": 1,
        "codigoTabelaReferencia": tabela,
        "codigoModelo": modelos_lista['Modelos'][i]['Value'],
        "codigoMarca": idMarca,
        "ano": null,
        "codigoTipoCombustivel": null,
        "anoModelo": null,
        "modeloCodigoExterno": null,
        }
        ano_modelo_lista = await request_data_fipe(url_ano_modelo  ,form_ano_modelo)
        for (let x = 0; x < ano_modelo_lista.length; x++) {
            const form_modelos_ano = {
            "codigoTabelaReferencia": tabela,
            "codigoMarca": idMarca,
            "codigoModelo": modelos_lista['Modelos'][i]['Value'],
            "codigoTipoVeiculo": 1,
            "anoModelo": parseInt(ano_modelo_lista[x]['Value'].split('-')[0]),
            "codigoTipoCombustivel": parseInt(ano_modelo_lista[x]['Value'].split('-')[1]),
            "tipoVeiculo": "carro",
            "modeloCodigoExterno":null,
            "tipoConsulta": 'tradicional',
            
            }
            await delay(3000);
            modelo_ano_lista = await request_data_fipe(url_valor_parametros,form_modelos_ano)

                const objeto = modelo_ano_lista;
                const jsonString = JSON.stringify(objeto) + '\n'; // Adiciona uma quebra de linha no final
                fs.writeFile('response.json', jsonString, {flag: 'a'}, (err) => {
                    if (err) {
                        console.error(err);
                        return;
                    }
                    console.log(`Objeto ${i} adicionado ao arquivo response.json`);
                });
            }
        }
    }

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

const param1 = process.env.PARAM1;
const param2 = process.env.PARAM2;

get_veiculos_marca(param1, param2);
