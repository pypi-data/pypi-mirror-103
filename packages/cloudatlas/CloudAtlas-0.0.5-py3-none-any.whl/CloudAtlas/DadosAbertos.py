import json
import requests
import xmltodict


def create_query(parameters):
    args = dict((k, v) for k, v in parameters.items() if v is not None)
    query = '&'.join("%s=%s" % (str(k), str(v)) for (k, v) in args.items())
    return query


class CamaraFederal():

    def __init__(self):
        self.version = "v2"
        self.base = "https://dadosabertos.camara.leg.br/api"

    def listar_proposicoes(self, **kwargs):
        """Lista informações básicas sobre projetos de lei, resoluções,
           medidas provisórias, emendas, pareceres e todos os outros tipos de
           proposições na Câmara.

        Args:
            dataInicio (str): Data de início para listagem das proposições.
            dataFim (str): Data de fim para listagem das proposições.

        Returns:
            dict: Listagem de proposições retornadas

        """
        rota = "proposicoes"
        query = self.create_query(kwargs)
        endpoint = f"{self.base}/{self.version}/{rota}?{query}"
        response = requests.get(url=endpoint)
        content = json.loads(response.content.decode("UTF-8"))
        return content, response


def xml_to_dict(xml):
    subst = xmltodict.parse(xml.content.decode("UTF-8"))
    dicionario = json.loads(json.dumps(subst))
    return dicionario


class SenadoFederal():

    def __init__(self):
        self.base = "https://legis.senado.leg.br/dadosabertos"

    def obter_agenda(self, data):
        rota = "plenario/agenda/dia"
        endpoint = f"{self.base}/{rota}/{data}"
        response = requests.get(url=endpoint)
        content = xml_to_dict(response)
        return content, response

    def listar_votacoes(self, data):
        rota = "plenario/lista/votacao"
        endpoint = f"{self.base}/{rota}/{data}"
        response = requests.get(url=endpoint)
        content = xml_to_dict(response)
        return content, response
