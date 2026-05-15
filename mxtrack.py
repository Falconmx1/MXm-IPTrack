#!/bin/bash

# ==============================================
# MXm-IPTrack - El rastreador de IPs con sazón mexicano
# Autor: Falconmx1
# Licencia: MIT
# ==============================================

# Colores chingones
ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[0;33m'
AZUL='\033[0;34m'
MORADO='\033[0;35m'
CYAN='\033[0;36m'
BLANCO='\033[0;37m'
RESET='\033[0m'

# Archivo de salida por defecto
ARCHIVO_SALIDA=""

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

# Función para validar IP
validar_ip() {
    local ip=$1
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        return 0
    else
        return 1
    fi
}

# Función para rastrear IP (estructura completa)
rastrear_ip() {
    local ip=$1
    local modo_bulk=$2  # "true" si estamos en modo batch (no imprime banners por IP)
    
    if [ "$modo_bulk" != "true" ]; then
        echo -e "${VERDE}[+] Rastreando IP: ${BLANCO}$ip${RESET}"
    fi
    
    # Usar ip-api.com (gratis, sin clave, versión JSON)
    local respuesta=$(curl -s "http://ip-api.com/json/$ip?fields=status,message,country,regionName,city,lat,lon,isp,org,as,zip,timezone,currency")
    
    local status=$(echo "$respuesta" | grep -o '"status":"[^"]*"' | cut -d '"' -f4)
    
    if [ "$status" = "success" ]; then
        local pais=$(echo "$respuesta" | grep -o '"country":"[^"]*"' | cut -d '"' -f4)
        local region=$(echo "$respuesta" | grep -o '"regionName":"[^"]*"' | cut -d '"' -f4)
        local ciudad=$(echo "$respuesta" | grep -o '"city":"[^"]*"' | cut -d '"' -f4)
        local lat=$(echo "$respuesta" | grep -o '"lat":[^,]*' | cut -d ':' -f2)
        local lon=$(echo "$respuesta" | grep -o '"lon":[^,]*' | cut -d ':' -f2)
        local isp=$(echo "$respuesta" | grep -o '"isp":"[^"]*"' | cut -d '"' -f4)
        local org=$(echo "$respuesta" | grep -o '"org":"[^"]*"' | cut -d '"' -f4)
        local asn=$(echo "$respuesta" | grep -o '"as":"[^"]*"' | cut -d '"' -f4)
        local zip=$(echo "$respuesta" | grep -o '"zip":"[^"]*"' | cut -d '"' -f4)
        local timezone=$(echo "$respuesta" | grep -o '"timezone":"[^"]*"' | cut -d '"' -f4)
        local currency=$(echo "$respuesta" | grep -o '"currency":"[^"]*"' | cut -d '"' -f4)
        
        # Mostrar resultado bonito
        echo -e "${CYAN}┌────────────────────────────────────────┐${RESET}"
        echo -e "${CYAN}│${RESET} ${AMARILLO}🌍 País:${RESET} $pais"
        echo -e "${CYAN}│${RESET} ${AMARILLO}📍 Región:${RESET} $region"
        echo -e "${CYAN}│${RESET} ${AMARILLO}🏙️ Ciudad:${RESET} $ciudad"
        echo -e "${CYAN}│${RESET} ${AMARILLO}📡 Coordenadas:${RESET} $lat, $lon"
        echo -e "${CYAN}│${RESET} ${AMARILLO}🛜 ISP:${RESET} $isp"
        echo -e "${CYAN}│${RESET} ${AMARILLO}🏢 Organización:${RESET} $org"
        echo -e "${CYAN}│${RESET} ${AMARILLO}🔢 ASN:${RESET} $asn"
        echo -e "${CYAN}│${RESET} ${AMARILLO}📮 Código postal:${RESET} $zip"
        echo -e "${CYAN}│${RESET} ${AMARILLO}⏰ Zona horaria:${RESET} $timezone"
        echo -e "${CYAN}│${RESET} ${AMARILLO}💱 Moneda:${RESET} $currency"
        echo -e "${CYAN}│${RESET} ${AMARILLO}🗺️ Mapa:${RESET} https://maps.google.com/?q=$lat,$lon"
        echo -e "${CYAN}└────────────────────────────────────────┘${RESET}\n"
        
        # Si se especificó archivo de salida, guardar en CSV
        if [ -n "$ARCHIVO_SALIDA" ]; then
            echo "\"$ip\",\"$pais\",\"$region\",\"$ciudad\",\"$lat\",\"$lon\",\"$isp\",\"$org\",\"$asn\",\"$zip\",\"$timezone\",\"$currency\"" >> "$ARCHIVO_SALIDA"
        fi
    else
        local error_msg=$(echo "$respuesta" | grep -o '"message":"[^"]*"' | cut -d '"' -f4)
        echo -e "${ROJO}[!] Error al rastrear $ip: $error_msg${RESET}"
        if [ -n "$ARCHIVO_SALIDA" ]; then
            echo "\"$ip\",\"ERROR: $error_msg\",,,,,,,,,," >> "$ARCHIVO_SALIDA"
        fi
    fi
}

# Función para geolocalización inversa (por ciudad)
geo_inversa() {
    local ciudad=$1
    echo -e "${VERDE}[+] Buscando coordenadas para: ${BLANCO}$ciudad${RESET}"
    
    # Usar OpenStreetMap Nominatim (free, sin clave)
    local respuesta=$(curl -s "https://nominatim.openstreetmap.org/search?q=$ciudad&format=json&limit=1")
    
    local lat=$(echo "$respuesta" | grep -o '"lat":"[^"]*"' | cut -d '"' -f4)
    local lon=$(echo "$respuesta" | grep -o '"lon":"[^"]*"' | cut -d '"' -f4)
    local display=$(echo "$respuesta" | grep -o '"display_name":"[^"]*"' | cut -d '"' -f4 | cut -c1-60)
    
    if [ -n "$lat" ] && [ -n "$lon" ]; then
        echo -e "${CYAN}┌────────────────────────────────────────┐${RESET}"
        echo -e "${CYAN}│${RESET} ${AMARILLO}📍 Ciudad:${RESET} $display..."
        echo -e "${CYAN}│${RESET} ${AMARILLO}📡 Latitud:${RESET} $lat"
        echo -e "${CYAN}│${RESET} ${AMARILLO}📡 Longitud:${RESET} $lon"
        echo -e "${CYAN}│${RESET} ${AMARILLO}🗺️ Mapa:${RESET} https://maps.google.com/?q=$lat,$lon"
        echo -e "${CYAN}└────────────────────────────────────────┘${RESET}\n"
    else
        echo -e "${ROJO}[!] No se encontró la ciudad: $ciudad${RESET}"
    fi
}

# Función para modo batch (archivo con IPs)
batch_rastreo() {
    local archivo=$1
    if [ ! -f "$archivo" ]; then
        echo -e "${ROJO}[!] El archivo $archivo no existe.${RESET}"
        exit 1
    fi
    
    echo -e "${VERDE}[+] Modo batch activado. Leyendo IPs desde $archivo${RESET}"
    if [ -n "$ARCHIVO_SALIDA" ]; then
        echo "IP,País,Región,Ciudad,Latitud,Longitud,ISP,Organización,ASN,Código Postal,Zona Horaria,Moneda" > "$ARCHIVO_SALIDA"
        echo -e "${AMARILLO}[+] Los resultados se guardarán en: $ARCHIVO_SALIDA${RESET}"
    fi
    
    while IFS= read -r ip; do
        # Saltar líneas vacías o comentarios
        if [[ -z "$ip" || "$ip" =~ ^# ]]; then
            continue
        fi
        rastrear_ip "$ip" "true"
        sleep 0.2  # Pequeña pausa para no saturar la API
    done < "$archivo"
    
    echo -e "${VERDE}[+] Batch completado.${RESET}"
}

# Menú principal
banner

# Procesar opciones largas
while [[ $# -gt 0 ]]; do
    case "$1" in
        -m|--myip)
            MODO="myip"
            shift
            ;;
        -t|--track)
            MODO="track"
            IP_TARGET="$2"
            shift 2
            ;;
        -i|--interactive)
            MODO="interactive"
            shift
            ;;
        -b|--batch)
            MODO="batch"
            ARCHIVO_BATCH="$2"
            shift 2
            ;;
        -r|--reverse)
            MODO="reverse"
            CIUDAD_TARGET="$2"
            shift 2
            ;;
        -o|--output)
            ARCHIVO_SALIDA="$2"
            shift 2
            ;;
        *)
            echo -e "${ROJO}[!] Opción desconocida: $1${RESET}"
            exit 1
            ;;
    esac
done

# Ejecutar según modo
case "$MODO" in
    myip)
        mi_ip=$(curl -s ifconfig.me)
        if validar_ip "$mi_ip"; then
            rastrear_ip "$mi_ip"
        else
            echo -e "${ROJO}[!] No se pudo obtener tu IP pública.${RESET}"
            exit 1
        fi
        ;;
    track)
        if [ -z "$IP_TARGET" ]; then
            echo -e "${ROJO}[!] Usa: $0 -t <IP>${RESET}"
            exit 1
        fi
        if validar_ip "$IP_TARGET"; then
            rastrear_ip "$IP_TARGET"
        else
            echo -e "${ROJO}[!] IP inválida: $IP_TARGET${RESET}"
            exit 1
        fi
        ;;
    interactive)
        echo -ne "${VERDE}[?] Ingresa la IP a rastrear: ${RESET}"
        read ip_usuario
        if validar_ip "$ip_usuario"; then
            rastrear_ip "$ip_usuario"
        else
            echo -e "${ROJO}[!] IP inválida.${RESET}"
            exit 1
        fi
        ;;
    batch)
        if [ -z "$ARCHIVO_BATCH" ]; then
            echo -e "${ROJO}[!] Usa: $0 -b <archivo.txt>${RESET}"
            exit 1
        fi
        batch_rastreo "$ARCHIVO_BATCH"
        ;;
    reverse)
        if [ -z "$CIUDAD_TARGET" ]; then
            echo -e "${ROJO}[!] Usa: $0 -r \"Ciudad, País\"${RESET}"
            exit 1
        fi
        geo_inversa "$CIUDAD_TARGET"
        ;;
    *)
        # Si no hay modo, mostrar ayuda
        echo -e "${AMARILLO}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
        echo -e "${VERDE}🇲🇽 MXm-IPTrack - Modos de uso:${RESET}"
        echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-m, --myip${RESET}         → Rastrear tu propia IP"
        echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-t, --track <IP>${RESET}   → Rastrear una IP específica"
        echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-i, --interactive${RESET}  → Modo interactivo paso a paso"
        echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-b, --batch archivo.txt${RESET} → Rastrear múltiples IPs desde archivo"
        echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-r, --reverse \"Ciudad\"${RESET} → Obtener coordenadas por nombre"
        echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-o archivo.csv${RESET}     → Exportar resultados a CSV (compatible con -t, -b, -m)"
        echo -e "\n${AMARILLO}📌 Ejemplos:${RESET}"
        echo -e "  $0 -t 8.8.8.8 -o resultados.csv"
        echo -e "  $0 -b ips.txt -o reporte.csv"
        echo -e "  $0 -r \"Guadalajara, México\""
        echo -e "  echo -e \"8.8.8.8\\n1.1.1.1\" > ips.txt && $0 -b ips.txt"
        echo -e "${AMARILLO}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
        exit 0
        ;;
esac
