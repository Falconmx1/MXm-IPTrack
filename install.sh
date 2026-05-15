#!/bin/bash

# ==============================================
# MXm-IPTrack - Instalador automático
# Autor: Falconmx1
# ==============================================

ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[0;33m'
AZUL='\033[0;34m'
RESET='\033[0m'

echo -e "${VERDE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${AMARILLO}  🇲🇽 MXm-IPTrack - Instalador para Linux/Termux${RESET}"
echo -e "${VERDE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

# Detectar si es Termux
if [ -d "/data/data/com.termux" ]; then
    echo -e "${AZUL}[+] Entorno Termux detectado${RESET}"
    PKG_MANAGER="pkg"
    INSTALL_DIR="$PREFIX/bin"
else
    echo -e "${AZUL}[+] Entorno Linux detectado${RESET}"
    PKG_MANAGER="sudo apt"
    INSTALL_DIR="/usr/local/bin"
fi

# Verificar dependencias
echo -e "${VERDE}[+] Verificando dependencias...${RESET}"
DEPS=("curl" "jq" "bc")

for dep in "${DEPS[@]}"; do
    if ! command -v "$dep" &> /dev/null; then
        echo -e "${AMARILLO}[!] $dep no está instalado. Instalando...${RESET}"
        if [ "$PKG_MANAGER" = "pkg" ]; then
            pkg install "$dep" -y
        else
            sudo apt update && sudo apt install "$dep" -y
        fi
    else
        echo -e "${VERDE}[✓] $dep ya está instalado${RESET}"
    fi
done

# Crear directorio de configuración
CONFIG_DIR="$HOME/.config/mxtrack"
mkdir -p "$CONFIG_DIR"

# Copiar archivos
echo -e "${VERDE}[+] Instalando MXm-IPTrack...${RESET}"
chmod +x mxtrack
cp mxtrack "$INSTALL_DIR/"
cp config.cfg "$CONFIG_DIR/"

# Crear archivo vacío para batch si no existe
if [ ! -f "$CONFIG_DIR/ips.txt" ]; then
    touch "$CONFIG_DIR/ips.txt"
    echo "# Agrega una IP por línea aquí" > "$CONFIG_DIR/ips.txt"
fi

echo -e "${VERDE}[+] Instalación completada exitosamente${RESET}"
echo -e "${AMARILLO}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${AZUL}📌 Comandos disponibles:${RESET}"
echo -e "   ${VERDE}mxtrack -m${RESET}         → Rastrear tu IP"
echo -e "   ${VERDE}mxtrack -t 8.8.8.8${RESET} → Rastrear una IP"
echo -e "   ${VERDE}mxtrack -i${RESET}         → Modo interactivo"
echo -e "   ${VERDE}mxtrack -b${RESET}         → Modo batch (usa ~/.config/mxtrack/ips.txt)"
echo -e "   ${VERDE}mxtrack -r \"Ciudad\"${RESET} → Geolocalización inversa"
echo -e "${AMARILLO}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
