## Projeto: Microservidor 
Objetivo do servidor é ter as seguintes funcionalidades: 
* Permitir que um arquivo seja enviado pelo cliente e amazenado em uma pasta no servidor.
* Permitir que o cliente faça download de arquivos previamente armazenados.
* Retornar uma lista dos arquivos disponiveis para download.
O trabalho foi implementado integralmente em python, utilizando bibliotecas HTTPServer, urlparse aprendendo assim as funções que compõem. Uso de HTTP Status code e tratamentos de erros. Assim, explorndo conceitos de Sistema distribuídos, protocolos de comunicação e arquitetura cliente-servidor.

---

### Estrutura do projeto
.
└── microservidor/
    ├── uploads/
    ├── servidor.py
    └── Readme.md

--- 

### Como executar
Primeiro, execute para clonar o projeto: 
```
git clone <url do projeto>
```
Certifique-se de ter o **Python 3** instalado.

Estando no terminal, na pasta do projeto, Execute o servidor
```
python server.py
```
Funcionalidades do servidor:

1. Enviar um arquivo para o servidor.(Upload)
```
curl -X POST -F "file=@/caminho/do/arquivo.tipoArquivo" http://localhost:8000/upload

```

2. Listar arquivos disponíveis
```
curl http://localhost:8000/files
```

3. Baixar um arquivo(Download)
```
curl -O http://localhost:8000/files/nomeArquivo.tipoArquivo
```









