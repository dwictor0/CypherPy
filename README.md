# CypherPy
> Este projeto utiliza criptografia simétrica baseada na biblioteca cryptography.

## Derivação de chave
A chave é derivada da senha do usuário utilizando:
- Algoritmo: Scrypt
- Parâmetros:
- n = n = 2^14
- r = 8
- p = 1
- lenght = 32 bytes

## Salt (Aleatoriedade)
- Um salt aleatório de 16 bytes é gerado automaticamente
- Armazenado no arquivo salt.salt
- Usado na derivação da chave

## Criptografia dos Dados
Os arquivos são criptografados usando:
- Algoritmo: Fernet
O Fernet internamente utiliza (AES - Advanced Encryption Standard) em modo CBC , HMAC para autenticação (integridade dos dados)

Como usar o projeto:
1. Clonar o repositorio:
```bash
git clone https://github.com/seu-usuario/CypherPy.git
cd CypherPy
```
2. Criar ambiente virtual (venv)
Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
Windows:
```bash
python3 -m venv venv
venv\Scripts\activate
```
3. Instalar dependencias:
```bash
pip install -r requirements.txt
```
4. Criptografar arquivo:
Na primeira execução, você deve gerar o salt manualmente usando -s:
```bash
python3 index.py file -e -s 16
```
5. Descriptografar arquivo:
```bash
python3 index.py file -d
```
6. Criptografar diretorio:
```bash
python3 index.py /folder -e
```
7. Descriptografar diretorio:
```bash
python3 index.py /folder -d
```
