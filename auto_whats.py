import pywhatkit as kit # Biblioteca de automação do WhatsApp
import pandas as pd # Leitura da base de dados
import time # Delay entre mensagens, por conta da internet e para o WhatsApp não bloquear o envio

# Leitura do arquivo csv
faltosos = pd.read_csv("banco_dados\\faltantes.csv", sep=";") 

# Iterando sobre os alunos faltosos
for i in range(len(faltosos)): 
    # Formatando o número para a biblioteca aceitar 
    numero = "+55" + f"{faltosos["TELEFONE"][i]}" 

    # Definir caminho da imagem
    imagem = "banco_dados\\busca_ativa.png" 

    # Retirando o primeiro nome e colocando e formatando em minúsculas
    nome = faltosos["NOME"][i].split()[0].capitalize()

    # Definindo a mensagem.
    mensagem =  f"""Olá🤗 {nome} Tudo bem?

Notei sua ausência na primeira reunião da nossa formação e quero reforçar o quanto sua participação é essencial. O encontro foi um momento importante para alinharmos expectativas e iniciarmos juntos essa Jornada I de 2025 com muito aprendizado.

Se precisar de apoio ou mais informações, estou à disposição para ajudar!

Conto com você nos próximos encontros"""

    

    # Caso queira enviar a mensagem descomente essa linha
    # kit.sendwhats_image(numero, imagem, mensagem)

    # Exibindo mensagem no console
    print(f"A mensagem: {mensagem} \n Foi enviada com sucesso! Enderaçada para {nome} com o número: {numero}")


    # Retirando os alunos que já foi realizado a busca ativa
    faltosos.drop(i)
    faltosos.to_csv("banco_dados\\faltantes\\faltantes.csv", index=False, sep=";")

    # Aplicando delay para carregamento da página e evitar o bloqueio do WhatsApp
    time.sleep(30)
 
