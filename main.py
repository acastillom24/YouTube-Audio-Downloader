from script.function import *

import tkinter as tk
from tkinter import messagebox
from threading import Thread


def download_mp3(url):
    try:
        link = "link=" + url

        # Limpiar el cuadro de entrada de URL después de la descarga
        url_entry.delete(0, tk.END)

        response = unlock(link)
        saveMp3(response["link"], "export/" + response["filename"])
        messagebox.showinfo(
            "Descarga completada",
            "El archivo se ha descargado correctamente.",
        )
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante la descarga: {e}")
    finally:
        download_button.config(state=tk.NORMAL)
        cancel_button.config(state=tk.DISABLED)


def on_download():
    url = url_entry.get()
    if url:
        download_button.config(state=tk.DISABLED)
        cancel_button.config(state=tk.NORMAL)
        if messagebox.askyesno(
            "Confirmar descarga", "¿Estás seguro de que quieres descargar el archivo?"
        ):
            Thread(target=download_mp3, args=(url,)).start()


def on_cancel():
    download_button.config(state=tk.NORMAL)
    cancel_button.config(state=tk.DISABLED)


def on_close():
    if messagebox.askokcancel("Salir", "¿Seguro que quieres salir?"):
        root.destroy()


# Crear la ventana principal
root = tk.Tk()
root.title("Descargar MP3")
root.geometry("400x200")

# Etiqueta y campo de entrada para la URL
url_label = tk.Label(root, text="URL del archivo MP3:")
url_label.pack(pady=10)
url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=5)

# Botones
button_frame = tk.Frame(root)
button_frame.pack(pady=20)
download_button = tk.Button(button_frame, text="Descargar", command=on_download)
download_button.pack(side=tk.LEFT, padx=5)
cancel_button = tk.Button(
    button_frame, text="Cancelar", command=on_cancel, state=tk.DISABLED
)
cancel_button.pack(side=tk.LEFT, padx=5)
close_button = tk.Button(root, text="Cerrar", command=on_close)
close_button.pack(pady=10)

# Iniciar la aplicación
root.mainloop()
