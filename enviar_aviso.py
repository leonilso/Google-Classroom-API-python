
# Importando bibiotecas

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd
from datetime import datetime, timedelta


# Se modificar esses escopos, exclua o arquivo token.json.
SCOPES = ["https://www.googleapis.com/auth/classroom.announcements"]


def main():
  """Shows basic usage of the Classroom API.
  Prints the names of the first 10 courses the user has access to.
  """
  creds = None
# O arquivo token.json armazena os tokens de acesso e atualização do usuário e é
  # criado automaticamente quando o fluxo de autorização é concluído pela primeira vez
  # tempo.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # Se não houver credenciais (válidas) disponíveis, deixe o usuário fazer login.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    #Salve as credenciais para a próxima execução
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("classroom", "v1", credentials=creds)

    # Lendo arquivos
    dir = "banco_dados\\"
    if not os.path.exists(dir + "announcement.csv"):
        df_announcement = pd.DataFrame(columns=['ID', 'turma', 'reuniao'])
    else:
       df_announcement = pd.read_csv(dir + "announcement.csv", sep=';')

    classes = pd.read_csv(dir + "turmas.csv", sep=';')
    meetings = pd.read_csv(dir + "reunioes.csv", sep=';')
    slides = pd.read_csv(dir + "slides.csv", sep=';')
    recoordings = pd.read_csv(dir + "gravacoes.csv", sep=';')

    # Iniciando variáveis
    day_post = False
    today = datetime.today().date()

    # Calculando dia
    for i in range(len(meetings['SEMANA'])):
        day_meet_list = datetime.strptime(meetings['SEMANA'][i], "%d/%m/%Y")
        day_meet_list = day_meet_list.date()
        if day_meet_list == today:
            day_post = True
            day_meet = day_meet_list
            day_meet = day_meet.strftime("%d/%m/%Y")

    if(day_post):
        classes_id = classes['ID'].to_list()

        for i in classes_id:
            # Coletando informações do banco de dados ( arquivos csv)
            classe = classes.loc[classes["ID"] == i, "NOME"].values[0]
            n_meet = meetings.loc[meetings["SEMANA"] == day_meet, "ID"].values[0]
            meet_name = meetings.loc[meetings["SEMANA"] == day_meet, "NOME"].values[0]
            day_of_week = f"{classes.loc[classes["ID"] == i, "DIA_SEMANA"].values[0]} feira"
            day_diff = int(classes.loc[classes["ID"] == i, "DIA_MES"].values[0])
            data_meet = datetime.strptime(day_meet, "%d/%m/%Y") + timedelta(days=day_diff)
            data_meet = data_meet.strftime("%d/%m/%Y")
            schedules_init = f"{classes.loc[classes["ID"] == i, "HORARIO_INICIO"].values[0]}"
            schedules_end = f"{classes.loc[classes["ID"] == i, "HORARIO_TERMINO"].values[0]}"
            link_slides = f"{slides.loc[slides["ID"] == n_meet, classe].values[0]}"
            link_meet = f"{classes.loc[classes["ID"] == i, "LINK_REUNIAO"].values[0]}"
            link_recording = f"{recoordings.loc[recoordings["ID"] == n_meet, classe].values[0]}"

          # Criando recado, infelizmente o announcement não tem a opção de agendar a publicação, então deve ser usado o estado PUBLISHED,
          #  a lógica de publicação deve ser feita com o python, ainda não fiz por falta de tempo.
            announcement = {
                "text": f'''
                {n_meet}º Encontro
                🤩 Pauta: {meet_name}
                📆 Data: {day_of_week}, {data_meet}
                ⏰ Horário: {schedules_init}h às {schedules_end}h

                🖥️ Slides: {link_slides}
                📲 Link da Reunião: {link_meet}
                🎞️ Link da gravação: {link_recording}
                        ''',
                "state": "PUBLISHED",
            }

            # Postagem 
            response = service.courses().announcements().create(
                courseId=i, body=announcement
            ).execute()


            # O id da postagem deve ser salvo para a posterior atualização com o link da gravação
            new_line = pd.DataFrame([{
                'ID': response['id'],
                'turma': classe,
                'reuniao': n_meet
            }])
            df_announcement = pd.concat([df_announcement, new_line], ignore_index=True)

            print(f"Aviso criado com ID: {response['id']} ")
        # Salva em um csv o id das postagens
        df_announcement.to_csv( dir + 'announcement.csv', index=False, sep=';')
  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
