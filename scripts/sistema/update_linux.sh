#!/bin/bash

cd $DEVOPSAPP_HOME

if ! sudo apt update; then
    echo "problemi download pacchetti"
else
    echo "nuovi pacchetti scaricati"
fi

if ! sudo apt upgrade -y; then
    echo "problemi di aggiornamento sistema operativo"
else
    echo "sistema operativo aggiornato"
fi

if ! sudo apt autoremove -y; then
    echo "problemi rimozione pacchetti obsoleti"
else
    echo "rimossi pacchetti obsoleti"
fi

if ! sudo apt autoclean -y; then
    echo "problemi rimozione pacchetti inutili"
else
    echo "rimossi pacchetti inutili"
fi

if ! sudo apt clean; then
    echo "problemi pulizia cache pacchetti"
else
    echo "pulita cache pacchetti"
fi