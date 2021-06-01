'''
    Elaborato Programmazione di Reti
            A.A.2020/2021
            Pietro Lelli
        Matricola: 0000915624
      Traccia 2: Python Web Server 
'''

#!/bin/env python
import sys, signal
import http.server
import socketserver
#new imports
import threading 

#manage the wait witout busy waiting
waiting_refresh = threading.Event()

# Legge numero della porta da riga di comando, e mette default 8080
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8080

# classe che mantiene le funzioni di SimpleHTTPRequestHandler e implementa
# il metodo get nel caso in cui si voglia fare un refresh
class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        # Scrivo sul file AllRequestsGET le richieste dei client     
        with open("AllRequests.txt", "a") as out:
          info = "GET request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n"
          out.write(str(info))
        if self.path == '/refresh':
            resfresh_contents()
            self.path = '/'
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
# ThreadingTCPServer per gestire più richieste
server = socketserver.ThreadingTCPServer(('127.0.0.1',port), ServerHandler)

# parte iniziale identica per tutte la pagine dei servizi
header_html = """
<html>
    <head>
        <style>
            h1 {
                text-align: center;
                margin: 0;
            }
            td {
                
                text-align: center;
            }
            .topnav {
  		        overflow: hidden;
  		        background-color: #2b8bd9;
  		    }
            .topnav a {
  		        float: left;
  		        color: #f6f6f6;
  		        text-align: center;
  		        padding: 14px 16px;
  		        text-decoration: none;
  		        font-size: 21px;
  		    }        
  		    .topnav a.active {
  		        background-color: #ff0000;
  		        color: white;
  		    }
        </style>
    </head>
    <body>
        <title>Azienda Ospedaliera</title>
"""

# barra di navigazione 
navigation_bar = """
        <br>
        <div class="topnav">
            <a class="active" href="http://127.0.0.1:{port}">Home</a>
            <a href="http://127.0.0.1:{port}/centralino.html">Centralino</a>
            <a href="http://127.0.0.1:{port}/modalitaPrenotazioni.html">Modalita' Prenotazioni</a>
            <a href="http://127.0.0.1:{port}/modalitaDisdetta.html">Modalita' Disdetta</a>
            <a href="http://127.0.0.1:{port}/modalitaPagamento.html">Modalita' Pagamento</a>
            <a href="http://127.0.0.1:{port}/prontoSoccorso.html">Pronto Soccorso</a>
            <a href="http://127.0.0.1:{port}/info.pdf" download="info.pdf" style="float: right">Download info pdf</a>
  		</div>
        <br>
        <table align="center">
""".format(port=port)
  
# creo tutte le pagine per la navigazione
def resfresh_contents():
    print("updating all contents")
    create_page_centralino()
    create_page_modalitaPrenotazioni()
    create_page_modalitaDisdetta()
    create_page_modalitaPagamento()
    create_page_prontoSoccorso()
    create_index_page()
    print("finished update")
        
def create_page_centralino():
        message = header_html + "<h1>Azienda Ospedaliera</h1>" + navigation_bar + "<br><br>" 
        message = message + "<h2>Centralino</h2>"
        message = message + "<h4>Tel. 049 821 1111 </h4>" + "in funzione 24h dal lunedi' alla domenica.<br><br>"
        message = message + "<h4>Tel. 049 821 6500</h4>" + "in funzione presso la sede Ospedale Bufalini dalle 8:00 alle 13:00 dal lunedi' al venerdi'."
        f = open('centralino.html','w', encoding="utf-8")
        f.write(message)
        f.close()  
        
def create_page_modalitaPrenotazioni():   
        message = header_html + "<h1>Azienda Ospedaliera</h1>" + navigation_bar + "<br><br>" 
        message = message + "<h2>Modalita' Prenotazioni</h2>"  
        message = message + "<h3>CUP Centro Unificato di Prenotazione</h3>" + "Solo per le prenotazioni allo sportello: <br>dal lunedi' al venerdi' dalle ore 7.30 alle ore 19.00<br><br>"
        message = message + "<h3>Call Center<br></h3>" + "Solo per prenotazioni telefoniche:<br>da lunedi' a venerdi' dalle 7.30 alle 17.00<br>da rete fissa: 840.000.664 (uno scatto alla risposta)<br>da rete mobile: 049 823 9511 (costi applicati in base al proprio piano tariffario).<br>"
        f = open('modalitaPrenotazioni.html','w', encoding="utf-8")
        f.write(message)
        f.close()

def create_page_modalitaDisdetta():
        message = header_html + "<h1>Azienda Ospedaliera</h1>" + navigation_bar + "<br><br>" 
        message = message + "<h2>Modalita' Disdetta</h2>" + "Nel caso di impossibilita' a presentarsi all appuntamento prenotato, la disdetta deve avvenire almeno tre giorni lavorativi prima dell appuntamento e cinque giorni lavorativi per gli esami strumentali. <br>La mancata presentazione ad una visita prenotata causa un danno rilevante alla collettivita' e in particolare a quei cittadini che sono in attesa di una prestazione medica; per questo motivo.<br>La mancata disdetta comporta il pagamento dell intera tariffa della prestazione prevista dal vigente Nomenclatore Tariffario, anche se il paziente e' esente dalla partecipazione alla spesa sanitaria. (Legge Regionale 30/2016 - art. 38, comma 12).<br>" 
        message = message + "<h3>Disdetta tramite FAX</h3>" + "Inviando un fax al N. 049 821 6330 segnalando i propri dati personali e il numero della prenotazione che si intende disdire.<br>Ricordiamo che il numero di prenotazione si trova in alto a sinistra del foglio di prenotazione;<br>Ad esempio: Prenotazione N. 2008 12345 (e' necessario indicare il numero completo anche delle quattro cifre dell anno cosi' come scritto sopra).<br>"
        message = message + "<h3>Disdetta Telefonica<br></h3>" + "Chiamando il numero di Disdetta Vocale: 840 140 301 (un solo scatto alla risposta)<br>Rispondera' un operatorice virtuale.<br>Si ricorda di tenere a portata di mano il foglio della prenotazione e seguire le indicazioni fornite dalla voce.<br>Vi ricordiamo che il numero di prenotazione si trova in alto a sinistra del foglio di prenotazione;<br>ad esempio: Prenotazione N. 2008 12345 e che dovete dettare il numero completo anche delle quattro cifre dell'anno cosi' come scritto sopra, una cifra per volta: due zero zero otto uno due tre quattro cinque.<br>Alla fine vi verra' dettato il codice dell operazione di disdetta: annotatelo direttamente sul foglio della prenotazione.<br>Se non avete il numero della prenotazione (ad esempio perché avete smarrito il foglio di prenotazione) e' possibile disdire lo stesso la prenotazione comunicando la data dell appuntamento e rispondendo alle ulteriori domande dell operatore virtuale.<br>"
        message = message + "<h3>Disdetta allo Sportello</h3>" + "Presentandosi personalmente presso l accettazione ambulatori e presso gli sportelli CUP<br>"
        f = open('modalitaDisdetta.html','w', encoding="utf-8")
        f.write(message)
        f.close()

def create_page_modalitaPagamento():
        message = header_html + "<h1>Azienda Ospedaliera</h1>" + navigation_bar + "<br><br>" 
        message = message + "<h2>Modalita' Pagamento</h2>" + "Il pagamento va effettuato prima dell erogazione della prestazione in una delle seguenti modalita':<br><br>1) alle riscuotitrici automatiche utilizzando il Bancomat o la Carta di Credito;<br><br>2) agli sportelli cassa ubicati<br><br>3) mediante i servizi online con Carta di Credito;<br><br>4) presso le filiali della banca Antonveneta-Monte dei Paschi di Siena presentando il foglio di prenotazione.<br>" 
        message = message + "<h3>ESTREMI PER I PAGAMENTI A FAVORE DELL AZIENDA OSPEDALIERA DI CESENA</h3>" + "Per i pagamenti a mezzo bonifico bancario dovranno essere utilizzate le seguenti coordinate, Banca Intesa San Paolo<br><br>IT34W0306913298100000300064<br><br>In tutti i casi e' obbligatorio indicare la causale del versamento inserendo il numero della prestazione.<br><br>Attenzione: Il mancato ritiro dei referti entro 30gg dalla disponibilita' degli stessi, comporta l addebito all assistito dell intero costo della prestazione usufruita, anche se esente (Legge n. 412/91, Legge Finanziaria 2007)<br>"
        f = open('modalitaPagamento.html','w', encoding="utf-8")
        f.write(message)
        f.close() 

def create_page_prontoSoccorso():
        message = header_html + "<h1>Azienda Ospedaliera</h1>" + navigation_bar + "<br><br>" 
        message = message + "<h2>Pronto Soccorso</h2>"
        message = message + "<h3>Note utili per un corretto utilizzo del Pronto Soccorso</h3><br>"
        message = message + "Il Pronto Soccorso e' un Servizio finalizzato alla diagnosi e alla cura rapida delle urgenze ed emergenze mediche e traumatologiche. Si rivolge prevalentemente a pazienti colpiti acutamente da malattie e lesioni che costituiscono un pericolo per l integrita' psico-fisica o per la vita stessa. L eccessivo e inappropriato uso del Pronto Soccorso ha come diretta conseguenza un progressivo allungamento medio dei tempi d' attesa. Pertanto, ogni qualvolta la sintomatologia accusata e' compatibile con una visita medica preliminare e' opportuno rivolgersi al Medico Curante o al Medico di Continuita' Assistenziale evitando il Pronto Soccorso. L utilizzazione del Pronto Soccorso per motivi non urgenti e' assolutamente da evitare. L ordine di accesso agli Ambulatori del Pronto Soccorso e' stabilito sulla base della gravita' della condizione clinica e non per ordine di arrivo. Le prestazioni eseguite dal Pronto Soccorso, che non hanno carattere di urgenza, sono soggette al pagamento del ticket.<br><br>"
        message = message + "<h4>I colori e le aree</h4>" + "Attraverso questa attivita' i pazienti al loro arrivo, sono suddivisi in 4 gruppi identificati da un codice/colore: <br><br> Cod. ROSSO: pazienti con un alterazione in atto delle funzioni vitali <br><br>Cod. GIALLO: pazienti con potenziale rischio di vita o di invalidita' <br><br>Cod. VERDE: Pazienti con grave stato di sofferenza <br><br>Cod. BIANCO: paziente non a rischio e con stato di sofferenza sopportabile. <br><br>"
        f = open('prontoSoccorso.html','w', encoding="utf-8")
        f.write(message)
        f.close() 
    
# creazione della pagina iniziale index.html
def create_index_page():
    f = open('index.html','w', encoding="utf-8")
    try:
        message = header_html + "<h1>Azienda Ospedaliera</h1>" + navigation_bar
        message = message + '<tr><th colspan="2"><h2>I Nostri Servizi:</h2></th>'
        message = message + '<th><ul><li>Centralino</li><li>Modalita Prenotazioni</li><li>Modalita Disdetta</li><li>Modalita Pagamento</li><li>Pronto Soccorso</li><li>Download File pdf</li></ul></th>'
        message = message + "<i> by Pietro Lelli </i>"
    except:
        pass
    f.write(message)
    f.close()

# definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if(server):
        server.server_close()
    finally:
      # fermo il thread del refresh senza busy waiting
      waiting_refresh.set()
      sys.exit(0)
      
# metodo che viene chiamato al lancio del server
def main():
    resfresh_contents()
    #Assicura che da tastiera usando la combinazione
    #di tasti Ctrl-C termini in modo pulito tutti i thread generati
    server.daemon_threads = True 
    #il Server acconsente al riutilizzo del socket anche se ancora non e' stato
    #rilasciato quello precedente, andandolo a sovrascrivere
    server.allow_reuse_address = True  
    #interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
    signal.signal(signal.SIGINT, signal_handler)
    # cancella i dati get ogni volta che il server viene attivato
    f = open('AllRequests.txt','w', encoding="utf-8")
    f.close()
    # loop infinito
    try:
      while True:
        server.serve_forever()
    except KeyboardInterrupt:
      pass
    server.server_close()

if __name__ == "__main__":
    main()