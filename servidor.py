#
#   Hillary A. Gramacho
#
#   Trabalho da disciplina: Sistema Distribuidos
#
#

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from email.parser import BytesParser
from email.policy import default

# ------ Pasta onde os arquivos serão incluidos --------

#pega caminho completo onde ta o server.py
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))

#cria o caminho completo para a pasta
PASTA_UPLOADS = os.path.join(PASTA_BASE,"uploads")

# classe base para tratar requisiçoes (GET, POST)
class ServidorArquivos(BaseHTTPRequestHandler):

    # ---------------- GET -----------------
    def do_GET(self):

        #pega a URL requisitada e separa o caminho
        url_parsed = urlparse(self.path)

        #pega só o caminho da URL
        caminho = url_parsed.path 

        ########## Listagem de arquivos ##########

        #endpoint para listar arquivos
        if caminho == "/files":

            #lista todos os arquivos da pasta
            arquivos = os.listdir(PASTA_UPLOADS)

            #envia código HTTP 200
            self.send_response(200) 
            self.send_header("Content-type", "text/plain; charset=utf-8")

            #Fim dos Headers HTTP
            self.end_headers() 

            #envia a lista de arquivos
            self.wfile.write("\n".join(arquivos).encode("utf-8")) 

        ############# Download de arquivo #################

        # endpoint para baixar arquivo especifico
        elif caminho.startswith("/files/"):
            nome_arquivo = caminho.split("/files/")[-1]
            caminho_arquivo = os.path.join(PASTA_UPLOADS, nome_arquivo)

            # verifica se o arquivo existe
            if os.path.exists(caminho_arquivo):
                self.send_response(200)

                #indica download de arquivo binário
                self.send_header("Content-Type", "application/octet-stream")

                # sugere o nome do arquivo no download
                self.send_header("Content-Disposition", f'attachment; filename="{nome_arquivo}"')
                self.end_headers() #fim do headers

                #lê arquivo em modo binário e envia para o cliente
                with open(caminho_arquivo, "rb") as f:
                    self.wfile.write(f.read())    
            # se nao existir retorna 404
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Arquivo nao encontrado")
        #qualquer outro caminho retorna 404(nao encontrado)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint nao encontrado")

    # ---------------- POST -----------------

    #pega a URL requisitada e separa o caminho
    def do_POST(self):
        url_parsed = urlparse(self.path)

        #pega só o caminho da URL
        caminho = url_parsed.path

        if caminho == "/upload":
            # Lê os cabeçalhos
            ctype = self.headers.get("Content-Type")

            # Verifica se é um formulario com arquivo
            if not ctype or "multipart/form-data" not in ctype:

                # Se nao for retorna 400(bad request)
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Requisicao invalida: esperado multipart/form-data")
                return

            # Extrai boundary do cabeçalho
            boundary = ctype.split("boundary=")[-1].encode()

            #Lê o tamanho do corpo e lê os bytes do arquivo enviado
            comprimento = int(self.headers.get("Content-Length", 0))
            corpo = self.rfile.read(comprimento)

            # Divide o corpo em partes
            partes = corpo.split(b"--" + boundary)
            for parte in partes:
                # procura a parte que tem o campo "file"
                # separa cabeçalho e conteudo real do arquivo
                if b"Content-Disposition" in parte and b"name=\"file\"" in parte:
                    cabecalho, conteudo = parte.split(b"\r\n\r\n", 1)
                    conteudo = conteudo.rstrip(b"\r\n--")

                    # Pega nome do arquivo
                    for linha in cabecalho.split(b"\r\n"):
                        if b"filename=" in linha:
                            nome_arquivo = linha.split(b"filename=")[1].strip().strip(b"\"").decode()

                            # Cria o caminho completo dentro da pasta de uploads
                            caminho_arquivo = os.path.join(PASTA_UPLOADS, nome_arquivo)

                            #salva o arquivo em modo binario(wb)
                            with open(caminho_arquivo, "wb") as f:
                                f.write(conteudo)
                            
                            #responde 200 OK e uma mensagem de sucesso                           self.send_response(200)
                            self.end_headers()
                            self.wfile.write(f"Arquivo '{nome_arquivo}' enviado com sucesso.".encode("utf-8"))
                            return
                        
            #caso nao encontre arquivo no POST, retorna 400
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Nenhum arquivo enviado")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint nao encontrado")

# ---------------- MAIN -----------------
# Cria o servidor HTTP na porta 8000
def run(server_class=HTTPServer, handler_class=ServidorArquivos, port=8000):

    #aceita requisiçoes de qualquer IP da maquina local
    servidor = server_class(("", port), handler_class)
    print(f"Servidor rodando em http://localhost:{port}")

    # entra em loop infinito esperando requisiçoes
    servidor.serve_forever()

if __name__ == "__main__":
    run()
