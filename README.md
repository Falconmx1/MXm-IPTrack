# 🇲🇽 MXm-IPTrack  
### *El rastreador de IPs con sazón mexicano*  

![Versión](https://img.shields.io/badge/versión-1.0-red)
![Licencia](https://img.shields.io/badge/licencia-MIT-green)
![Bash](https://img.shields.io/badge/shell-bash-blue)
![Python](https://img.shields.io/badge/python-3.7+-yellow)

**MXm-IPTrack** es una herramienta CLI inspirada en `ip-tracer`, pero con mejoras y un toque bien chingón. Ideal para pentesting, OSINT o simplemente saber quién está detrás de una IP.  

## 🔥 Características  
- Geolocalización completa (país, estado, ciudad, latitud, longitud).  
- ISP y organización propietaria de la IP.  
- Mapa enlace directo a Google Maps.  
- Soporte para **Kali Linux**, **Termux** y cualquier distro con Bash/Python 3.  
- Modo rápido (una línea) o interactivo.  
- Colores y diseño estilo hacker mexa.  

## 📦 Instalación  

```bash
git clone https://github.com/Falconmx1/MXm-IPTrack.git
cd MXm-IPTrack
chmod +x install.sh
./install.sh


🚀 Uso
bash

# Rastrear tu propia IP
mxtrack -m

# Rastrear una IP específica
mxtrack -t 8.8.8.8

# Modo interactivo
mxtrack -i

📸 Captura de ejemplo
text

[+] IP: 187.189.234.12
[+] País: México (MX)
[+] Estado: Jalisco
[+] Ciudad: Guadalajara
[+] Lat/Lon: 20.6597, -103.3496
[+] ISP: Telmex
[+] Mapa: https://maps.google.com/?q=20.6597,-103.3496

1️⃣ Generar reporte HTML bonito:
mxtrack -t 8.8.8.8 -html reporte.html
# Abre reporte.html en tu navegador

2️⃣ Enviar resultado por Telegram:

Primero configura config.cfg con tu token y chat ID.

¿Cómo obtener token y chat ID?

    Token: Habla con @BotFather en Telegram, crea un bot y te dará un token tipo 123456:ABC-DEF...

    Chat ID: Envía un mensaje a tu bot y luego visita https://api.telegram.org/bot<TU_TOKEN>/getUpdates, ahí aparece tu chat_id

Luego:
mxtrack -t 1.1.1.1 -tg

3️⃣ Combinar HTML + Telegram:
bash

mxtrack -m -html mi_ip.html && mxtrack -m -tg

4️⃣ Batch + Telegram (enviar cada resultado):

Modifica el batch si quieres que envíe cada IP a Telegram (avísame y te lo agrego).

