import sys
import yt_dlp

from pathlib import Path

from decorators import handle_errors, print_styled

OUTPUT_DIR = Path("output")

@handle_errors("Error al descargar el audio en MP3")
def download_mp3(url: str, filename: str) -> Path:
    """Descarga el audio del vídeo en formato MP3 a 192kbps."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    ydl_opts: dict = {
        "format": "bestaudio/best",
        "outtmpl": str(OUTPUT_DIR / f"{filename}.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return OUTPUT_DIR / f"{filename}.mp3"

@handle_errors("Error al descargar el vídeo en MP4")
def download_mp4(url: str, filename: str) -> Path:
    """Descarga el vídeo en formato MP4 con la mejor calidad disponible."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    ydl_opts: dict = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": str(OUTPUT_DIR / f"{filename}.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return OUTPUT_DIR / f"{filename}.mp4"

@handle_errors("Error al descargar el vídeo de YouTube")
def download_video(url: str, filename: str) -> None:
    """Descarga un vídeo de YouTube en formatos MP3 y MP4."""

    saved_filepath_mp3: Path = download_mp3(url=url, filename=filename)
    print_styled(
        message=f"✓ Audio descargado: {saved_filepath_mp3}\n",
        color="green"
    )

    saved_filepath_mp4: Path = download_mp4(url=url, filename=filename)
    print_styled(
        message=f"✓ Vídeo descargado: {saved_filepath_mp4}\n",
        color="green"
    )

def main():
    """Función principal que maneja la ejecución del script."""
    if len(sys.argv) != 3:
        print_styled(
            message="Número de argumentos inválido\n",
            error_type="ValueError",
            color="red"
        )
        print_styled(
            message="📖 Uso: python main.py <url> <filename>",
            color="cyan"
        )
        print_styled(
            message="📝 Ejemplo: python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ my_video",
            color="cyan"
        )
        sys.exit(1)

    url: str = sys.argv[1]
    filename: str = sys.argv[2]
    download_video(url=url, filename=filename)

if __name__ == "__main__":
    main()
