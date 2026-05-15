#!/bin/bash

# Colores chingones
ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[0;33m'
AZUL='\033[0;34m'
MORADO='\033[0;35m'
CYAN='\033[0;36m'
BLANCO='\033[0;37m'
RESET='\033[0m'

# Función para mostrar banner
banner() {
    echo -e "${ROJO}"
    echo "  ╔═══╗╔═══╗╔╗─╔╗╔═══╗╔══╗╔═══╗╔═══╗╔═══╗"
    echo "  ║╔═╗║║╔══╝║║─║║║╔══╝║╔╗║║╔═╗║║╔═╗║║╔══╝"
    echo "  ║╚═╝║║╚══╗║╚═╝║║╚══╗║╚╝║║╚═╝║║╚═╝║║╚══╗"
    echo "  ║╔╗╔╝║╔══╝║╔╗╔╝║╔══╝║╔╗║║╔╗╔╝║╔╗╔╝║╔══╝"
    echo "  ║║║╚╗║╚══╗║║║╚╗║╚══╗║║║║║║║╚╗║║║╚╗║╚══╗"
    echo "  ╚╝╚═╝╚═══╝╚╝╚═╝╚═══╝╚╝╚╝╚╝╚═╝╚╝╚═╝╚═══╝"
    echo -e "${RESET}"
    echo -e "${AMARILLO}     MXm-IPTrack - Rastreador de IPs con sazón mexicano${RESET}"
    echo -e "${AZUL}     Creado por Falconmx1 | Uso educativo siempre${RESET}\n"
}

# Función para rastrear IP
rastrear_ip() {
    local ip=$1
    echo -e "${VERDE}[+] Rastreando IP: ${BLANCO}$ip${RESET}"
    
    # Usar ip-api.com (gratis, sin clave)
    local respuesta=$(curl -s "http://ip-api.com/json/$ip")
    
    # Extraer datos con grep/sed (o se puede usar jq si está instalado)
    local status=$(echo "$respuesta" | grep -o '"status":"[^"]*"' | cut -d '"' -f4)
    
    if [ "$status" = "success" ]; then
        local pais=$(echo "$respuesta" | grep -o '"country":"[^"]*"' | cut -d '"' -f4)
        local region=$(echo "$respuesta" | grep -o '"regionName":"[^"]*"' | cut -d '"' -f4)
        local ciudad=$(echo "$respuesta" | grep -o '"city":"[^"]*"' | cut -d '"' -f4)
        local lat=$(echo "$respuesta" | grep -o '"lat":[^,]*' | cut -d ':' -f2)
        local lon=$(echo "$respuesta" | grep -o '"lon":[^,]*' | cut -d ':' -f2)
        local isp=$(echo "$respuesta" | grep -o '"isp":"[^"]*"' | cut -d '"' -f4)
        
        echo -e "${CYAN}┌────────────────────────────────────────┐${RESET}"
        echo -e "${CYAN}│${RESET} ${AMARILLO}🌍 País:${RESET} $pais"
        echo -e "${CYAN}│${RESET} ${AMARILLO}📍 Región:${RESET} $region"
        echo -e "${CYAN}│${RESET} ${AMARILLO}🏙️ Ciudad:${RESET} $ciudad"
        echo -e "${CYAN}│${RESET} ${AMARILLO}📡 Coordenadas:${RESET} $lat, $lon"
        echo -e "${CYAN}│${RESET} ${AMARILLO}🛜 ISP:${RESET} $isp"
        echo -e "${CYAN}│${RESET} ${AMARILLO}🗺️ Mapa:${RESET} https://maps.google.com/?q=$lat,$lon"
        echo -e "${CYAN}└────────────────────────────────────────┘${RESET}\n"
    else
        echo -e "${ROJO}[!] Error: No se pudo rastrear la IP o es inválida.${RESET}"
    fi
}

# Menú principal
banner

case "$1" in
    -m|--myip)
        mi_ip=$(curl -s ifconfig.me)
        rastrear_ip "$mi_ip"
        ;;
    -t|--track)
        if [ -z "$2" ]; then
            echo -e "${ROJO}[!] Usa: $0 -t <IP>${RESET}"
            exit 1
        fi
        rastrear_ip "$2"
        ;;
    -i|--interactive)
        echo -ne "${VERDE}[?] Ingresa la IP a rastrear: ${RESET}"
        read ip_usuario
        rastrear_ip "$ip_usuario"
        ;;
    *)
        echo -e "${AMARILLO}Uso:${RESET}"
        echo "  $0 -m, --myip        Rastrear tu propia IP"
        echo "  $0 -t, --track <IP>  Rastrear una IP específica"
        echo "  $0 -i, --interactive Modo interactivo"
        echo -e "\n${ROJO}Ejemplo: $0 -t 8.8.8.8${RESET}"
        exit 1
        ;;
esac
