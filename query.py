import requests
from bs4 import BeautifulSoup
import pandas as pd

## https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteo.asp
#https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteoPost.asp?CodParam=AFMERAIWID&CodTema=REGIONE&IdEstraz=DE&Frequenza=GG&TipoOutput=HTML&Separatore=TAB&IdRichiesta=28988914564617&IdRichiestaCarto=&DataIniz=05/08/2024&InizOra=00:00&DataFine=06/08/2024&FineOra=23:59
#MONTE ROCCHETTA (La Spezia)    "ME00083">

variableOrario = [
## Orario ##
    "TEMPTRMWC0", #>TEMPERATURA - Temperatura Media Dell'Aria
    "TEMPTRMWC2", #>TEMPERATURA - Temperatura Massima Dell'Aria
    "TEMPTRMWC5", #>TEMPERATURA - Temperatura Minima Dell'Aria
    "UMREIGRWCO", #>UMIDITA RELATIVA - Umidità Relativa Media Dell'Aria
    "DIRVWAN", #>VENTO - Direzione Di Provenienza Del Vento Prevalente
    "VV00TACWAN", #>VENTO - Intensità Massima Del Vento
    "VVMDTACWAN", #>VENTO - Intensità Media Del Vento
#    "PRECPBIWC1", # SELECTED>PRECIPITAZIONE - Precipitazione Cumulata
    "ALIGWCL", #>PRESSIONE ATMOSFERICA - Altezza Media Del Livello Di Geopotenziale Di Riferimento
    "PATMBRMWC1", #>PRESSIONE ATMOSFERICA - Pressione Atmosferica Media Al Livello Del Mare 
    "PATMBRMWCL", #>PRESSIONE ATMOSFERICA - Pressione Atmosferica Media Alla Stazione 
    "RSTORDTWC1", #>RADIAZIONE SOLARE - Radiazione Solare Media (Potenza)
]

variableGiornaliero = [
## Giornaliero ##
    "PORTIDRI11", #SELECTED>PORTATA - Portata Massima Del Torrente
    "PORTIDRWI9", #>PORTATA - Portata Media Del Torrente
    "PORTIDRI10", #>PORTATA - Portata Minima Del Torrente
    "PRECPBIWC1", #>PRECIPITAZIONE - Precipitazione Cumulata
    "ALIGMAXWCL", #>PRESSIONE ATMOSFERICA - Altezza Massima Del Livello Di Geopotenziale Di Riferimento
    "ALIGMINWCL", #>PRESSIONE ATMOSFERICA - Altezza Minima Del Livello Di Geopotenziale Di Riferimento
    "ALIGMDWCL", #>PRESSIONE ATMOSFERICA - Altezza Media Del Livello Di Geopotenziale Di Riferimento
    "PATMMBRWCL", #>PRESSIONE ATMOSFERICA - Pressione Atmosferica Media Al Livello Del Mare 

## Giornaliero ##
    "PAMXBRMWCL", #>PRESSIONE ATMOSFERICA - Pressione Atmosferica Massima Al Livello Del Mare 
    "PAMNBRMWCL", #>PRESSIONE ATMOSFERICA - Pressione Atmosferica Minima Al Livello Del Mare
    "RSTORDTWCL", #>RADIAZIONE SOLARE - Radiazione Solare Giornaliera
    "ESTEWCL", #>TEMPERATURA - Escursione Termica
    "TEMPTRMWC4", #>TEMPERATURA - Temperatura Massima Assoluta Dell'Aria
    "TEMPTRMWC1", #>TEMPERATURA - Temperatura Media Dell'Aria
    "TEMPTRMWC7", #>TEMPERATURA - Temperatura Minima Assoluta Dell'Aria
    "UMMXIGRWCL", #>UMIDITA RELATIVA - Umidità Relativa Massima Dell'Aria
    "UMREIGRWCL", #>UMIDITA RELATIVA - Umidità Relativa Media Dell'Aria
    "UMMNIGRWCL", #>UMIDITA RELATIVA - Umidità Relativa Minima Dell'Aria
    "DIRVGONWAN", #>VENTO - Direzione Di Provenienza Del Vento Massimo
    "DISCOCPWAN", #>VENTO - Distribuzione Di Frequenza Congiunta Della Direzione Ed Intensità Vento (1 + 5 Classi Intensità X 16 Settori In Direzioni)
    "VVMXTACWAN", #>VENTO - Intensità Massima Del Vento
    "VVMDTAOWAN", #>VENTO - Intensità Media Del Vento

    "HWMDMARWIM", #MARE - Altezza D'Onda
    "PONDMARWIM", #MARE - Periodo D'Onda
    "TEMPTRMWIM", #MARE - Temperatura Superficiale Del Mare
    "LIVAIDRWID", #PORTATA - Livello Medio Del Torrente
    "SNOWNIVWCL", #PRECIPITAZIONE - Altezza Del Manto Nevoso
    "PRECPBIWC1", #PRECIPITAZIONE - Precipitazione Cumulata
    "ALIGWCL", #PRESSIONE ATMOSFERICA - Altezza Media Del Livello Di Geopotenziale Di Riferimento


]



#variables = variableOrario + variableGiornaliero
variables = variableGiornaliero

def getIdRichiesta():
    urlIdRichiesta = "https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteo12.asp"
    response = requests.get(urlIdRichiesta)
    return response.text.split("NAME=IdRichiesta VALUE=")[1].split(">")[0]

#idRichiesta = getIdRichiesta()
idRichiesta = "28988914564688"
idRichiesta = "28988914565546" ##L'ID Richiesta contiene la stazione

#stazione = "MROCC"
stazione = "FABIA"
stazione = "SPZIA"

for variable in variables:
    #variable = "TEMPTRMWC1"
    #variable = "TEMPTRMWC0"
    #frequenza = "HH"
    
    if variable in variableOrario: frequenza = "HH"
    else: frequenza = "GG"
    
    # Specifica l'URL del file da scaricare https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteoPost.asp?CodParam=TEMPTRMWC0&CodTema=STAZIONE&IdEstraz=DE&Frequenza=HH&TipoOutput=HTML&Separatore=TAB&IdRichiesta=27667458855479&IdRichiestaCarto=&DataIniz=20/07/2023&InizOra=00:00&DataFine=21/07/2023&FineOra=23:59
    url = "https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteoPost.asp?CodParam=%s&CodTema=STAZIONE&IdEstraz=DE&Frequenza=%s&TipoOutput=HTML&Separatore=TAB&IdRichiesta=%s&IdRichiestaCarto=&DataIniz=01/12/2000&InizOra=00:00&DataFine=26/12/2024&FineOra=23:59"%(variable, frequenza, idRichiesta)
    print(url)

    # Effettua la richiesta HTTP per scaricare il file
    response = requests.get(url)

    print(response.status_code)

    # Verifica che la richiesta sia andata a buon fine
    if response.status_code == 200:
        # Salva il contenuto del file in una stringa
        data = response.text

        # Crea un oggetto BeautifulSoup a partire dal contenuto del file HTML
        soup = BeautifulSoup(data, 'html.parser')

        # Seleziona la tabella dal file HTML
        tables = soup.find_all('table')
        if len(tables)<3: continue
        table = tables[3]
#        print(table) 
        localita = str(table).split("<")[4].split(": ")[1]
        valore = str(table).split("<")[10].split(": ")[1]

        # Inizializza una lista per i nomi delle colonne
        columns = []

        # Inizializza una lista per i dati delle righe
        rows_data = []

#        print("HELLO", table)
        # Per ogni riga della tabella
        for row in table.find_all('tr'):
            # Inizializza una lista per i dati della riga corrente
            row_data = []
            
            # Per ogni colonna della riga
            for col in row.find_all('td'):
              # Aggiungi il contenuto della colonna alla lista dei dati della riga
              row_data.append(col.text)
#            print(row_data)
            if len(row_data)!=5: continue
            # Se si tratta della prima riga (intestazione)
            if columns == []:
              # Salva i nomi delle colonne
              columns = row_data
              for i, column in enumerate(columns):
                  if columns[i][0] == " ": columns[i] = columns[i][1:]
                  if columns[i][-1] == " ": columns[i] = columns[i][:-1]
            else:
              # Altrimenti, salva i dati della riga
              rows_data.append(row_data)
        
        # Crea un DataFrame di Pandas con i dati delle righe e delle colonne
        df = pd.DataFrame(rows_data, columns=columns)
        

        if not "Valore" in columns: continue
        # Converti la colonna ' Valore ' in numeri
        df['Valore'] = pd.to_numeric(df['Valore'], errors='coerce')
        
        #df['Valore'] = df['Valore'].apply(lambda x: x / 3600 * 10000/24)
        
        import re
        
        localita = re.sub(r'[^\w\s]', '', localita)
        valore = re.sub(r'[^\w\s]', '', valore)
        localita = localita.replace(" ", "_")
        valore = valore.replace(" ", "_")
        valore = valore.replace("\n", "_")
        valore = valore.replace("\r", "_")
        
        # Write the DataFrame to a CSV file
        df = df.rename(columns={'Valore': valore})
        
        df.to_csv('%s_%s.csv'%(localita, valore), index=False)
        
        print("DONE")
        print(df)

    else:
        # Se la richiesta non è andata a buon fine, stampa un messaggio di errore
        print("Errore nello scaricamento del file: status code", response.status_code)

        ## Filtra il DataFrame per selezionare solo le righe con la data 07/10/2022
        #df_filtered = df[df[' Inizio rilevazione '] == '20/12/2022']

        ## Seleziona la colonna 'Radiazione solare'
        #radiazione_solare = df_filtered[' Valore ']

        ## Stampa il valore della radiazione solare
        #print(radiazione_solare)


import matplotlib.pyplot as plt

# Crea il grafico
df.plot(x='Inizio rilevazione', y=valore)

# Mostra il grafico
plt.show()



        # 53182088046022

