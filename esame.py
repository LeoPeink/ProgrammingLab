# -*- coding: utf-8 -*-

class ExamException(Exception):
        pass


class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name=name
    
    def readCSV(self, path, symbol):
        '''
        Parameters
        ----------
        path : (string)
            system path to the file.
        symbol : (char)
            symbol used to split the CSV..

        Returns
        -------
        outValues : [[int,float]]
            tuple of tuples, basically a CSV "object" with proper casting.

        '''
        outValues = []
        if(isinstance(path, str) == False):
            raise ExamException('Errore: attesa stringa come nome file')
        try:
            input_file=open(path, 'r')
        except Exception:
            raise ExamException('Errore: impossibile aprire il file')
            
            
        for index, line in enumerate(input_file):   #for each index and line in the input stream,
            try:
                elements=line.split(symbol)             #split the data
                values = [round(float(elements[0])),float(elements[1])] #save the values in a tuple  
            except Exception:
                continue
            if(len(outValues)>0):
                if(values[0]<=outValues[-1][0]):
                    raise ExamException('Errore, epoch in disordine e/o valori duplicati')
            outValues.append(values)
        try:
            input_file.close()
        except Exception():
            raise ExamException('Errore: impossibile chiudere il file')
        return outValues
    
    
    def get_data(self):
        dati = []
        dati = self.readCSV(self.name,',')
        return dati
        
        
        #----------------CORPO PROGRAMMA------------------
def hourly_trend_changes(time_series):
    if(isinstance(time_series, list)==False):
        raise ExamException('Errore: attesa lista come parametro di funzione')
    for tupla in time_series:               #salva solo i timestamp divisi per 3600 in una tupla
        tupla[0] = tupla[0]//3600           #tramite divisione intera, salva il n° di ora dei timestamp
        #print(tupla)
        
    if(len(time_series)==0):
        return []
    elif(len(time_series)==1):
        return [0]
        
    out = []                                #inizializzo la tupla di output
    var=-1                                  #numero di variazioni in una determinata ora: iniz. a -1 per il falso positivo durante il primissimo ciclo in cui si controlla la crescenza/decrescenza dei dati.
    var2=0                                  #se tra l'ora analizzata e quella successiva c'è un'inversione, questa diventa 1 e ne viene tenuto conto nel prossimo ciclo (il prossimo ciclo inizia da 1 in tal caso)
    crescente = 1                           #indica se al ciclo precedente la funzione fosse crescente
    decrescente = 1                         #indica se al ciclo precedente la funzione fosse decrescente
    i=0                                     #contatore
    while(len(time_series)>i+1):                                                #cicla tutti i valori
        if(time_series[i][0]==time_series[i+1][0]):                             #se l'ora è la stessa
            if(time_series[i][1]-time_series[i+1][1]>0 and crescente == 1):     #se l'andamento è cambiato
                decrescente = 1                                                 #aggiorna gli stati
                crescente = 0
                var+=1                                                          #aumenta il numero di variazioni
            elif(time_series[i][1]-time_series[i+1][1]<0 and decrescente == 1): #idem a sopra, ma con la crescenza
                crescente = 1
                decrescente = 0
                var+=1
            i+=1
        else:                                                                   #se l'ora è diversa (si passa da un'ora alla successiva)
            if(time_series[i][1]-time_series[i+1][1]>0 and crescente == 1):     #se l'andamento cambia (uguale a sopra)
                decrescente = 1
                crescente = 0
                var2+=1                                                         #aumenta il numero di variazioni della prossima ora
            elif(time_series[i][1]-time_series[i+1][1]<0 and decrescente == 1): #idem a sopra
                crescente = 1
                decrescente = 0
                var2+=1
            i+=1
            if(var==-1):
                var=0
            if(i==1):
                var2=0                                             
            out.append(var)                                                     #infine, salva il numero di variazioni nella tupla di output
            var = var2                                                          #tieni conto della variazione tra l'ora attuale e quella successiva, se presente
            var2 = 0
    if(var==-1):
        var=0                                                                #azzera il numero di variazioni dell'ora successiva
    out.append(var)                                                             #scrivi l'ultimo numero di variazioni nell'output (il ciclo controlla fino a [i-1], è necessario salvare manualmente l'ultimo valore)
    return(out) 
        
        
    
        #--------------------MAIN-------------------------

time_series_file = CSVTimeSeriesFile(name="data.csv") #NB "data.csv"
time_series = time_series_file.get_data()
print(hourly_trend_changes(time_series))


















