#!/bin/bash

# ==============================================
# MXm-IPTrack - El rastreador de IPs con sazón mexicano
# Autor: Falconmx1
# Licencia: MIT
# Versión: 2.0 (HTML + Telegram)
# ==============================================

# Cargar configuración
CONFIG_DIR="$HOME/.config/mxtrack"
CONFIG_FILE="$CONFIG_DIR/config.cfg"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    # Valores por defecto
    API_URL="http://ip-api.com/json"
    GEO_API_URL="https://nominatim.openstreetmap.org/search"
    BATCH_DELAY=0.3
    MAX_RETRIES=2
    OUTPUT_FORMAT="pretty"
    AUTO_MAP="false"
    COLOR_MODE="true"
    TELEGRAM_BOT_TOKEN=""
    TELEGRAM_CHAT_ID=""
fi

# Colores chingones (si no están desactivados)
if [ "$COLOR_MODE" = "false" ]; then
    ROJO=''; VERDE=''; AMARILLO=''; AZUL=''; MORADO=''; CYAN=''; BLANCO=''; RESET=''
else
    ROJO='\033[0;31m'
    VERDE='\033[0;32m'
    AMARILLO='\033[0;33m'
    AZUL='\033[0;34m'
    MORADO='\033[0;35m'
    CYAN='\033[0;36m'
    BLANCO='\033[0;37m'
    RESET='\033[0m'
fi

# Variables globales
ARCHIVO_SALIDA=""
REPORTE_HTML=""
TIPO_SALIDA="normal"  # normal, html, tg
DATOS_IP=""

# ===================== FUNCIONES =====================

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
    echo -e "${AZUL}     Versión 2.0 | HTML + Telegram | Uso educativo${RESET}\n"
}

validar_ip() {
    local ip=$1
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        return 0
    else
        return 1
    fi
}

# Nueva: Obtener datos de IP y guardarlos en variable global
obtener_datos_ip() {
    local ip=$1
    local intento=1
    
    while [ $intento -le $MAX_RETRIES ]; do
        local respuesta=$(curl -s "$API_URL/$ip?fields=status,message,country,regionName,city,lat,lon,isp,org,as,zip,timezone,currency")
        local status=$(echo "$respuesta" | grep -o '"status":"[^"]*"' | cut -d '"' -f4)
        
        if [ "$status" = "success" ]; then
            # Limpiar variables anteriores
            unset pais region ciudad lat lon isp org asn zip timezone currency
            
            pais=$(echo "$respuesta" | grep -o '"country":"[^"]*"' | cut -d '"' -f4)
            region=$(echo "$respuesta" | grep -o '"regionName":"[^"]*"' | cut -d '"' -f4)
            ciudad=$(echo "$respuesta" | grep -o '"city":"[^"]*"' | cut -d '"' -f4)
            lat=$(echo "$respuesta" | grep -o '"lat":[^,]*' | cut -d ':' -f2)
            lon=$(echo "$respuesta" | grep -o '"lon":[^,]*' | cut -d ':' -f2)
            isp=$(echo "$respuesta" | grep -o '"isp":"[^"]*"' | cut -d '"' -f4)
            org=$(echo "$respuesta" | grep -o '"org":"[^"]*"' | cut -d '"' -f4)
            asn=$(echo "$respuesta" | grep -o '"as":"[^"]*"' | cut -d '"' -f4)
            zip=$(echo "$respuesta" | grep -o '"zip":"[^"]*"' | cut -d '"' -f4)
            timezone=$(echo "$respuesta" | grep -o '"timezone":"[^"]*"' | cut -d '"' -f4)
            currency=$(echo "$respuesta" | grep -o '"currency":"[^"]*"' | cut -d '"' -f4)
            
            DATOS_IP="IP: $ip
País: $pais
Región: $region
Ciudad: $ciudad
Coordenadas: $lat, $lon
ISP: $isp
Organización: $org
ASN: $asn
Código Postal: $zip
Zona Horaria: $timezone
Moneda: $currency
Mapa: https://maps.google.com/?q=$lat,$lon"
            return 0
        else
            local error_msg=$(echo "$respuesta" | grep -o '"message":"[^"]*"' | cut -d '"' -f4)
            if [ $intento -eq $MAX_RETRIES ]; then
                DATOS_IP="Error al rastrear $ip: $error_msg"
                return 1
            fi
            sleep 1
            ((intento++))
        fi
    done
}

mostrar_resultado_pretty() {
    local ip=$1
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
}

# Nueva: Generar reporte HTML
generar_html() {
    local archivo=$1
    local ip=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    cat > "$archivo" << EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MXm-IPTrack - Reporte de $ip</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #0f0;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(0,0,0,0.8);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0,255,0,0.3);
        }
        h1 {
            text-align: center;
            color: #ff4444;
            text-shadow: 0 0 10px #ff0000;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #0f0;
            margin-bottom: 20px;
        }
        .data-row {
            margin: 10px 0;
            padding: 10px;
            background: #111;
            border-left: 3px solid #0f0;
        }
        .label {
            color: #ffaa00;
            font-weight: bold;
            display: inline-block;
            width: 150px;
        }
        .value {
            color: #0f0;
        }
        .map-link {
            color: #00aaff;
            text-decoration: none;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #666;
        }
        .badge {
            display: inline-block;
            background: #ff4444;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🇲🇽 MXm-IPTrack Report</h1>
            <p>Generado el: $timestamp</p>
        </div>
        <div class="data-row">
            <span class="label">🌍 IP Rastreada:</span>
            <span class="value">$ip</span>
        </div>
        <div class="data-row">
            <span class="label">📍 País:</span>
            <span class="value">$pais</span>
        </div>
        <div class="data-row">
            <span class="label">🏙️ Región:</span>
            <span class="value">$region</span>
        </div>
        <div class="data-row">
            <span class="label">🏙️ Ciudad:</span>
            <span class="value">$ciudad</span>
        </div>
        <div class="data-row">
            <span class="label">📡 Coordenadas:</span>
            <span class="value">$lat, $lon</span>
        </div>
        <div class="data-row">
            <span class="label">🛜 ISP:</span>
            <span class="value">$isp</span>
        </div>
        <div class="data-row">
            <span class="label">🏢 Organización:</span>
            <span class="value">$org</span>
        </div>
        <div class="data-row">
            <span class="label">🔢 ASN:</span>
            <span class="value">$asn</span>
        </div>
        <div class="data-row">
            <span class="label">📮 Código Postal:</span>
            <span class="value">$zip</span>
        </div>
        <div class="data-row">
            <span class="label">⏰ Zona Horaria:</span>
            <span class="value">$timezone</span>
        </div>
        <div class="data-row">
            <span class="label">💱 Moneda:</span>
            <span class="value">$currency</span>
        </div>
        <div class="data-row">
            <span class="label">🗺️ Mapa:</span>
            <span class="value"><a href="https://maps.google.com/?q=$lat,$lon" class="map-link" target="_blank">Ver en Google Maps</a></span>
        </div>
        <div class="footer">
            <span class="badge">MXm-IPTrack</span> - Herramienta de OSINT con sazón mexicano
        </div>
    </div>
</body>
</html>
EOF
    echo -e "${VERDE}[✓] Reporte HTML guardado en: $archivo${RESET}"
}

# Nueva: Enviar por Telegram
enviar_telegram() {
    if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
        echo -e "${ROJO}[!] Error: Configura TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en ~/.config/mxtrack/config.cfg${RESET}"
        return 1
    fi
    
    local mensaje="$1"
    local url="https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage"
    
    # Escapar caracteres especiales para Telegram Markdown
    mensaje=$(echo "$mensaje" | sed 's/_/\\_/g; s/*/\\*/g; s/\[/\\[/g; s/\]/\\]/g; s/(/\\(/g; s/)/\\)/g; s/~/\\~/g; s/`/\\`/g; s/>/\\>/g; s/#/\\#/g; s/+/\\+/g; s/-/\\-/g; s/=/\\=/g; s/|/\\|/g; s/{/\\{/g; s/}/\\}/g; s/\./\\./g; s/!/\\!/g')
    
    local respuesta=$(curl -s -X POST "$url" -d "chat_id=$TELEGRAM_CHAT_ID" -d "text=$mensaje" -d "parse_mode=MarkdownV2")
    
    if echo "$respuesta" | grep -q '"ok":true'; then
        echo -e "${VERDE}[✓] Mensaje enviado a Telegram correctamente${RESET}"
    else
        echo -e "${ROJO}[!] Error al enviar a Telegram: $respuesta${RESET}"
    fi
}

rastrear_ip() {
    local ip=$1
    local modo=$2  # normal, html, tg
    
    obtener_datos_ip "$ip"
    if [ $? -eq 0 ]; then
        case "$modo" in
            html)
                generar_html "$REPORTE_HTML" "$ip"
                ;;
            tg)
                enviar_telegram "📡 *MXm-IPTrack Reporte* 📡\n\`\`\`\n$DATOS_IP\n\`\`\`"
                ;;
            *)
                mostrar_resultado_pretty "$ip"
                if [ -n "$ARCHIVO_SALIDA" ]; then
                    echo "\"$ip\",\"$pais\",\"$region\",\"$ciudad\",\"$lat\",\"$lon\",\"$isp\",\"$org\",\"$asn\",\"$zip\",\"$timezone\",\"$currency\"" >> "$ARCHIVO_SALIDA"
                fi
                ;;
        esac
    else
        echo -e "${ROJO}$DATOS_IP${RESET}"
        if [ -n "$ARCHIVO_SALIDA" ] && [ "$modo" != "html" ] && [ "$modo" != "tg" ]; then
            echo "\"$ip\",\"ERROR\",,,,,,,,,," >> "$ARCHIVO_SALIDA"
        fi
    fi
}

geo_inversa() {
    local ciudad=$1
    echo -e "${VERDE}[+] Buscando coordenadas para: ${BLANCO}$ciudad${RESET}"
    
    local respuesta=$(curl -s "$GEO_API_URL?q=$ciudad&format=json&limit=1")
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
        if [[ -z "$ip" || "$ip" =~ ^# ]]; then
            continue
        fi
        obtener_datos_ip "$ip"
        if [ $? -eq 0 ]; then
            mostrar_resultado_pretty "$ip"
            if [ -n "$ARCHIVO_SALIDA" ]; then
                echo "\"$ip\",\"$pais\",\"$region\",\"$ciudad\",\"$lat\",\"$lon\",\"$isp\",\"$org\",\"$asn\",\"$zip\",\"$timezone\",\"$currency\"" >> "$ARCHIVO_SALIDA"
            fi
        else
            echo -e "${ROJO}$DATOS_IP${RESET}"
        fi
        sleep "$BATCH_DELAY"
    done < "$archivo"
    
    echo -e "${VERDE}[+] Batch completado.${RESET}"
}

# ===================== MENÚ PRINCIPAL =====================

banner

# Procesar opciones largas
while [[ $# -gt 0 ]]; do
    case "$1" in
        -m|--myip) MODO="myip"; shift ;;
        -t|--track) MODO="track"; IP_TARGET="$2"; shift 2 ;;
        -i|--interactive) MODO="interactive"; shift ;;
        -b|--batch) MODO="batch"; ARCHIVO_BATCH="$2"; shift 2 ;;
        -r|--reverse) MODO="reverse"; CIUDAD_TARGET="$2"; shift 2 ;;
        -o|--output) ARCHIVO_SALIDA="$2"; shift 2 ;;
        -html|--html) TIPO_SALIDA="html"; REPORTE_HTML="$2"; shift 2 ;;
        -tg|--telegram) TIPO_SALIDA="tg"; shift ;;
        *) echo -e "${ROJO}[!] Opción desconocida: $1${RESET}"; exit 1 ;;
    esac
done

# Si no hay modo, mostrar ayuda
if [ -z "$MODO" ]; then
    echo -e "${AMARILLO}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${VERDE}🇲🇽 MXm-IPTrack v2.0 - Modos de uso:${RESET}"
    echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-m, --myip${RESET}              → Rastrear tu propia IP"
    echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-t, --track <IP>${RESET}        → Rastrear una IP específica"
    echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-i, --interactive${RESET}       → Modo interactivo"
    echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-b, --batch archivo.txt${RESET} → Rastrear múltiples IPs"
    echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-r, --reverse \"Ciudad\"${RESET} → Geolocalización inversa"
    echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-o archivo.csv${RESET}          → Exportar a CSV"
    echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-html reporte.html${RESET}      → Generar reporte HTML"
    echo -e "  ${CYAN}•${RESET} $0 ${VERDE}-t 8.8.8.8 -tg${RESET}          → Enviar resultado a Telegram"
    echo -e "\n${AMARILLO}📌 Ejemplos avanzados:${RESET}"
    echo -e "  $0 -t 8.8.8.8 -html resultado.html"
    echo -e "  $0 -t 1.1.1.1 -tg"
    echo -e "  $0 -m -html mi_ip.html && $0 -m -tg"
    echo -e "${AMARILLO}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    exit 0
fi

# Ejecutar según modo y tipo de salida
case "$MODO" in
    myip)
        mi_ip=$(curl -s ifconfig.me)
        if validar_ip "$mi_ip"; then
            if [ "$TIPO_SALIDA" = "html" ]; then
                rastrear_ip "$mi_ip" "html"
            elif [ "$TIPO_SALIDA" = "tg" ]; then
                rastrear_ip "$mi_ip" "tg"
            else
                rastrear_ip "$mi_ip" "normal"
            fi
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
            if [ "$TIPO_SALIDA" = "html" ]; then
                rastrear_ip "$IP_TARGET" "html"
            elif [ "$TIPO_SALIDA" = "tg" ]; then
                rastrear_ip "$IP_TARGET" "tg"
            else
                rastrear_ip "$IP_TARGET" "normal"
            fi
        else
            echo -e "${ROJO}[!] IP inválida: $IP_TARGET${RESET}"
            exit 1
        fi
        ;;
    interactive)
        echo -ne "${VERDE}[?] Ingresa la IP a rastrear: ${RESET}"
        read ip_usuario
        if validar_ip "$ip_usuario"; then
            if [ "$TIPO_SALIDA" = "html" ]; then
                rastrear_ip "$ip_usuario" "html"
            elif [ "$TIPO_SALIDA" = "tg" ]; then
                rastrear_ip "$ip_usuario" "tg"
            else
                rastrear_ip "$ip_usuario" "normal"
            fi
        else
            echo -e "${ROJO}[!] IP inválida.${RESET}"
            exit 1
        fi
        ;;
    batch)
        if [ -z "$ARCHIVO_BATCH" ]; then
            ARCHIVO_BATCH="$CONFIG_DIR/ips.txt"
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
esac
