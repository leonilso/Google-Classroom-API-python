# Google-Classroom-API-python
Repositório para conectar com o google classroom via API, enviando mensagens em lote, gerenciar alunos e reuniões e integrar com o googke meet, whatsapp e email.

O  arquivo "credential.json" deve ser criado através do site: https://developers.google.com/classroom/guides/auth?hl=pt-br

Para o script funcionar o OAuth 2.0 deve estar configurado e o ambiente no Google Cloud aberto.

Para configurar o ambiente assista esse vídeo, ele está em inglês, mas está bem explicado.
https://www.youtube.com/watch?v=1WwLPcVaYxY

O arquivo "token.json" é gerado assim que o código roda pela primeira vez, ou seja não é preciso baixá-lo de nenhum lugar como o "credential.json", entretanto caso seja necessário trocar de conta ou alterar os SCOPES o arquivo "token.json" deverá ser apagado.

Os arquivos .csv só contem informações públicas, tudo que era pessoal eu apaguei, portanto deve se montar as tabelas manualmente (AINDA) pode se usar o Excel para isso, mas o formato deve ser o CSV com separador de ";" e com capacidade para caractéres utf-8
