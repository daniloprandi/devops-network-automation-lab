# Flusso reale richiesta VM3 -> VM1


## 1) Utente su VM3

Esegue:

curl http://192.168.200.128/processi-api/processes


Cosa succede:

viene avviato il programma curl.

Linux crea un processo:

nome: curl
PID: xxxx



## 2) Processo curl

curl analizza l'URL:

protocollo:
http

server:
192.168.200.128

risorsa richiesta:
/processi-api/processes


curl costruisce il messaggio HTTP:

GET /processi-api/processes HTTP/1.1
Host: 192.168.200.128



## 3) curl chiede al sistema operativo di spedire

curl non parla direttamente con la scheda rete.

Chiama il kernel tramite syscall:

socket()
connect()
send()



## 4) Kernel VM3 crea una socket

Nasce un endpoint di comunicazione:

192.168.200.131:porta_random

esempio:

192.168.200.131:45678



## 5) TCP crea il segmento

Il kernel aggiunge:

porta sorgente: 45678
porta destinazione: 80


crea:

TCP SEGMENT



## 6) IP crea il pacchetto

Il livello IP aggiunge:

IP sorgente:
192.168.200.131

IP destinazione:
192.168.200.128


crea:

IP PACKET



## 7) Ethernet crea il frame

Vengono aggiunti:

MAC sorgente VM3

MAC destinazione VM1


crea:

ETHERNET FRAME



## 8) VM1 riceve il frame

Il kernel smonta:

FRAME
 ↓
IP PACKET
 ↓
TCP SEGMENT
 ↓
HTTP REQUEST


vede:

porta destinazione 80



## 9) Kernel VM1 consegna a nginx

La porta 80 appartiene al processo:

nginx

PID xxxx


La richiesta entra nel container nginx.



## 10) nginx legge la richiesta

Riceve:

GET /processi-api/processes


apre:

nginx/default.conf



## 11) nginx controlla le regole

Trova:

location /processi-api/


decide:

questa richiesta deve andare a processi-api



## 12) nginx crea una nuova richiesta interna

Destinazione:

http://processi-api:3140


Docker DNS traduce:

processi-api

in

IP container



## 13) Gunicorn riceve

Nel container processi-api gira:

gunicorn


Il worker prende la richiesta.



## 14) Gunicorn chiama Flask

Carica:

app.py


passa la richiesta all'app Flask.



## 15) Flask cerca la route

Trova:

@app.route("/processes")


quindi esegue la funzione collegata.



## 16) La funzione Python parte

Il codice chiama:

os.listdir("/proc")


per chiedere:

quali processi esistono?



## 17) Linux legge /proc

/proc è creato dal kernel.


Dentro trova:

/proc/1
/proc/25
/proc/40



## 18) Python costruisce gli oggetti

Crea strutture:

dictionary

{
 pid: 1,
 name: nginx
}



## 19) Flask crea JSON

Trasforma i dati:

Python dict

↓

JSON HTTP response



## 20) Risposta torna indietro

JSON

↓
Gunicorn

↓
nginx

↓
TCP/IP

↓
curl VM3



## 21) Fine

curl riceve il JSON.

lo stampa.

il processo curl termina.