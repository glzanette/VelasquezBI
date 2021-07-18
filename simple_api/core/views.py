
import re
from collections import OrderedDict
from datetime import datetime

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


class GetHistory:
    """
    Retorna os Historicos
    """
    history = requests.get('http://www.mocky.io/v2/598b16861100004905515ec7').json()


class GetClient:
    """
    Retorna os Clientes
    """
    client = requests.get('http://www.mocky.io/v2/598b16291100004705515ec5').json()


def change_id_for_name(id_recived):
    """
    Essa função troca o cpf pelo nome, ela até trata os caracteres especiais.
    Se o valor vem errado, eu não posso alterar a consistencia dos dados que estão sendo consumidos.
    """

    queryset = GetClient()
    name = None
    for x in queryset.client:
        if re.sub('[^A-Za-z0-9]+', '', x['cpf']) == re.sub('[^A-Za-z0-9]+', '', id_recived):
            name = x['nome']

    return name if name else id_recived


def change_all_keys(dict_keys):

    new_dict = {}
    for x in dict_keys.keys():
        new_dict[change_id_for_name(x)] = dict_keys[x]

    return new_dict


class ShowHighestBuyer(GetHistory, View):
    """
    Essa view retorna os valores do historico somados e ordenados por cliente / quantidade.
    Eu até retornaria o nome dos clientes se os cpf estivessem certos.
    """

    def get(self, request):
        by_value = {}
        for x in self.history:
            if not by_value.get(x['cliente']):
                by_value[x['cliente']] = 0
            
            by_value[x['cliente']] += x['valorTotal']

        ordered_tuple = sorted(by_value.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        ordened_final = {}
        for w in ordered_tuple:
            ordened_final[w[0]] = w[1]

        ordened_final = change_all_keys(ordened_final)

        return JsonResponse(ordened_final)
            

class ShowHighestBuy(GetHistory, View):
    """
    Essa view retorna a compra de maior valor por cliente em 2016.
    """
    def get(self, request):
        by_value = {}
        for x in self.history:
            if datetime.strptime(x["data"], "%d-%m-%Y") > datetime(
                2016, 1, 1
            ) and datetime.strptime(x["data"], "%d-%m-%Y") < datetime(
                2017, 1, 1
            ):
                by_value[x['cliente']] = x['valorTotal']
            
        ordered_tuple = sorted(by_value.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        highest = {ordered_tuple[0][0]: ordered_tuple[0][1]}

        highest = change_all_keys(highest)

        return JsonResponse(highest)


class ShowFavoriteClient(GetHistory, View):
    """
    Retorna o clinete mais fiel contando o numero de vezes que ele comprou.
    """

    def get(self, request):
        by_value = {}
        for x in self.history:
            if not by_value.get(x['cliente']):
                by_value[x['cliente']] = 1
            
            by_value[x['cliente']] += 1

        ordered_tuple = sorted(by_value.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        highest = {ordered_tuple[0][0]: ordered_tuple[0][1]}

        highest = change_all_keys(highest)

        return JsonResponse(highest)


class ShowMostBuyWineByClient(GetHistory, View):
    """
    Retorna o nome do vinho mais bebido de um cliente, nao considerando a safra e o tipo (mas poderia)
    """

    def get(self, request):
        by_value = {}
        for x in self.history:
            if not by_value.get(x['cliente']):
                by_value[x['cliente']] = {'wines': {}}
            for z in x['itens']:
                if not by_value[x['cliente']]['wines'].get(z['produto']):
                    by_value[x['cliente']]['wines'][z['produto']] = 1
                by_value[x['cliente']]['wines'][z['produto']] += 1

        final_wines = {}
        for x in by_value:
            ordered_tuple = sorted(by_value[x]['wines'].items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
            final_wines[x] = {'wines': {ordered_tuple[0][0]: ordered_tuple[0][1]}}

        final_wines = change_all_keys(final_wines)

        return JsonResponse(final_wines)
            
