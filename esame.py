import re

class ExamException(Exception):
    pass


def compute_avg_monthly_difference(time_series, first_year, last_year):
    
    if time_series == None:
        raise ExamException('La tua time series non esiste')
    
    if not isinstance(time_series, str):
        raise ExamException('Il nome del file deve essere una stringa')

    if not isinstance(first_year, str):
        raise ExamException('Gli anni devono essere passati come stringhe')
     
    if not isinstance(last_year, str):
        raise ExamException('Gli anni devono essere passati come stringhe')

    if int(first_year) < 0 or int(last_year)<0:
        raise ExamException('La variabile anno deve contenere un numero positivo')

    if  int(first_year) > 2022 or int(last_year) > 2022:
        raise ExamException('L\' anno deve essere minore di 2022')

    if int(first_year) >= int(last_year) :
        raise ExamException('Il primo anno non puo essere maggiore dell\' ultimo')


    readable = True
        
    try:
        my_file = open(time_series, 'r')
        my_file.read()
        
    except Exception: readable = False

    if not readable: raise ExamException('File non trovato o illegibile') 


    lista_mensile = []

    data = open(time_series, 'r')


    for i in data: #ciclo su tutti gli elementi del file (riga per riga)

        i = i.split(',')

        if i[0] == 'date' or i[0] =='passangers': continue

        if len(i) < 2 and re.match('\d\d\d\d\-\d\d',i[0]):
            i.append('0') # se non ce una misurazion la setto a 0

            #se ci sono elementi che non sono di tipo data salto la riga
        elif len(i) < 2 and not re.match('\d\d\d\d\-\d\d',i[0]):
            continue
            
        
        while len(i) > 2:
            #se len > 2 ho elementi di troppo
            #print(39)

            #parto dal ultimo elemento: se non e ne in formato data ne un numero lo tolgo dalla lista
            if not re.match('\d\d\d\d\-\d\d',i[len(i)-1]) and not re.match('\d',i[len(i)-1]):
                    i.remove(i[len(i)-1])
                    
            elif not re.match('\d\d\d\d\-\d\d',i[len(i)-2]):
                    i.remove(i[len(i)-1])
            else:
                i.remove(i[0])
        if not re.match('\d\d\d\d\-\d\d',i[0]): #se gli anni non vengono primi e il num dei passegeri secondo cambio l'ordine
            temp = i[0]
            i[0] = i[1]
            i[1] = temp
            

        lista_mensile.append(i) #dopo le eventuali modficazioni aggiungo alla lista i due valori
        
    if len(lista_mensile)<2:
        raise ExamException('Elementi insufficienti per valutare')


    #prendo il primo elemento per verificare se l'anno first_year e contenuto nel file
    anno_mese = lista_mensile[0][0]
    anno_mese = anno_mese.split('-')

    if first_year < anno_mese[0]:
        raise ExamException('Questo file contiene dati a partire dal', anno_mese[0], 'mentre il tuo anno iniziale e',first_year)



    #prendo l'ultimo elemento per verificare se l'anno last_year e contenuto nel file
    anno_mese = lista_mensile[-1][0]
    anno_mese = anno_mese.split('-')

    if last_year > anno_mese[0]:
        raise ExamException('Questo file contiene dati fino', anno_mese[0], 'mentre il tuo anno finale e',last_year)



    lista_risultato = [0 for i in range(12)] # 12 elementi per 12 mesi    

    for i in range (len(lista_mensile)):

        # Verifica del timestamp ordinato #

        #assegno alla variabile il valore del primo elemento della lista
        anno_mese = lista_mensile[i][0] 

        #separo l'anno dal mese
        anno_mese = anno_mese.split('-') 

        #tolgo lo 0 dal mese per poterlo utilizzare come indice della lista
        anno_mese[1] = int(anno_mese[1].lstrip('0'))


        anno_mese_seguente = lista_mensile[i+1][0] #assegno alla variabile il valore dello seguente elemento della lista

        anno_mese_seguente = anno_mese_seguente.split('-') #separo l'anno dal mese
        
        anno_mese_seguente[1] = int(anno_mese_seguente[1].lstrip('0'))


        if anno_mese[1] == 12:
            #se dopo dicembre il mese non e gennaio e l'anno non e di uno maggiore
            if anno_mese_seguente[1] != 1 or int(anno_mese[0])+1 != int(anno_mese_seguente[0]):
                
                  raise ExamException('Timestamp fuori ordine')
                

        elif anno_mese[1] != anno_mese_seguente[1] -1:
            raise ExamException('Timestamp fuori ordine')

        elif anno_mese[0] != anno_mese_seguente[0]:
            raise ExamException('Timestamp fuori ordine')



        #se l'anno e minore di quello iniziale salto l'iterazione
        if first_year > anno_mese[0]: 
            continue
        
        
        # quando supero last_year ritorno la lista ed esco dalla funzione
        elif last_year  ==  anno_mese[0]:
            return lista_risultato



        #prendo il numero con il quale fare la media cioe la differenza tra il primo e l'ultimo anno
        diff_first_last = int(last_year) - int(first_year)

        
        #faccio la coonversione a  int dei primi dodici mesi per non ripeterlo dopo
        if anno_mese[0] == first_year:
            #se riesco a convertirlo in int ok
            try:
                lista_mensile[i][1] = int(lista_mensile[i][1]) 
                
            except ValueError:
                # se no setto il valore a zero
                lista_mensile[i][1] = 0

            if lista_mensile[i][1] < 0:
                #se il numero e negativo non lo prendiamo in considerazione
                lista_mensile[i][1] =0


            
        #time_series[i+12][1].strip() #tolgo la \n dal numero di passegeri
                
        #verifico il valore dello stesso mese dell'anno prossimo
        try:
            #se riesco a convertirlo in int ok
            lista_mensile[i+12][1] = int(lista_mensile[i+12][1]) 
            
        except ValueError:
            #se no setto il valore a zero perche non e possibile cambiarlo a integer
            lista_mensile[i+12][1] = 0

        #se il numero e negativo non lo prendiamo in considerazione
        if lista_mensile[i+12][1] < 0: 
                lista_mensile[i+12][1] =0



        #se i valori sono differenti da 0 aggiungo la loro media alla lista
        if lista_mensile[i+12][1] != 0 and lista_mensile[i][1] != 0: 

            #prendo il valore dei passegeri del seguente anno e lo sottraggo al valore di passegeri di quest'anno facendo subito la media
            lista_risultato[anno_mese[1]-1] += (lista_mensile[i+12][1] - lista_mensile[i][1])/diff_first_last #aggiungo alla lista il num dei passegeri di quel mese


            
class CSVTimeSeriesFile():

    def __init__(self, name):
        
        self.name = name


    def get_data(self):

        incremento_medio = compute_avg_monthly_difference(self.name, first_year, last_year) #chiamata della funzione

        lista_finale = [[ first_year +  '/'  + last_year +  ' - '  + str(i+1), incremento_medio[i]] for i in range(12)]

        return lista_finale
