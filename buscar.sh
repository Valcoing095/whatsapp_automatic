#!/bin/bash

echo -n "¿Qué deseas buscar? "
read -r busqueda

if [ -n "$busqueda" ]; then
    open "https://www.google.com/search?q=$(echo "$busqueda" | jq -sRr @uri)"
else
    echo "No proporcionaste ninguna búsqueda."
fi