import yt_dlp
import subprocess
import os
from colorama import Fore, Style, init

init(autoreset=True)

# ───────── UI ─────────
def banner():
    os.system("clear")
    print(Fore.CYAN + "=" * 65)
    print(Fore.YELLOW + "🎮 YOUTUBE DOWNLOADER PRO — SOLO TERMUX - DANJAH")
    print(Fore.GREEN + " MP4 ANDROID ✔ | MP3 ✔ | WHATSAPP ✔")
    print(Fore.CYAN + "=" * 65)

def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '')
        s = d.get('_speed_str', '')
        e = d.get('_eta_str', '')
        print(Fore.GREEN + f"\r⬇ {p} | ⚡ {s} | ⏳ {e}", end='')
    elif d['status'] == 'finished':
        print(Fore.CYAN + "\n✔ Descarga completa. Procesando...")

# ───────── UTIL ─────────
def check_ffmpeg():
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except:
        print(Fore.RED + "\n❌ FFmpeg no instalado. Ejecuta:")
        print(Fore.YELLOW + "pkg install ffmpeg -y")
        exit(1)

# ───────── MP4 ANDROID SEGURO ─────────
def download_mp4(url):
    os.makedirs("Videos", exist_ok=True)

    ydl_opts = {
        # descargamos lo mejor disponible, luego convertimos
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'Videos/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        input_file = ydl.prepare_filename(info)

    output_file = input_file.replace(".mp4", "_android.mp4")

    # Conversión FINAL segura (clave de todo)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_file,
        "-c:v", "libx264",
        "-profile:v", "baseline",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-c:a", "aac",
        "-b:a", "128k",
        output_file
    ], check=True)

    os.remove(input_file)

    print(Fore.GREEN + "\n📱 Video optimizado para Android y WhatsApp")
    print(Fore.CYAN + f"📂 Guardado en: {output_file}")

# ───────── MP3 ESTABLE ─────────
def download_mp3(url):
    os.makedirs("Audios", exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'Audios/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(Fore.GREEN + "\n🎧 MP3 creado correctamente")

# ───────── MENU ─────────
def menu():
    check_ffmpeg()

    while True:
        banner()
        print(Fore.RED + "[1] Descargar VIDEO MP4 (Android)")
        print(Fore.RED + "[2] Descargar AUDIO MP3")
        print(Fore.RED + "[3] Salir")

        op = input(Fore.YELLOW + "\n👉 Opción: ").strip()

        if op == "3":
            break

        url = input(Fore.YELLOW + "🔗Ingresa la URL: ").strip()

        try:
            if op == "1":
                download_mp4(url)
            elif op == "2":
                download_mp3(url)
            else:
                print(Fore.RED + "❌ Opción inválida")
        except Exception as e:
            print(Fore.RED + f"\n❌ Error controlado: {e}")

        input(Fore.YELLOW + "\nPresiona ENTER para continuar...")

# ───────── START ─────────
if __name__ == "__main__":
    menu()