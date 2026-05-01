import tkinter as tk
from tkinter import font
import sys

def mostrar_guia_tkinter():
    try:
        root = tk.Tk()
        root.title("🚀 ClaudeMachote - Novedades y Guía")
        root.geometry("600x580")
        root.configure(bg="#1a1a2e")
        root.attributes("-topmost", True)
        
        # Estilos
        bg_color = "#1a1a2e"
        fg_color = "#e0e0e0"
        accent_color = "#e94560"
        title_font = font.Font(family="Segoe UI", size=16, weight="bold")
        h2_font = font.Font(family="Segoe UI", size=12, weight="bold")
        text_font = font.Font(family="Segoe UI", size=10)
        
        # Contenedor principal con padding
        main_frame = tk.Frame(root, bg=bg_color, padx=30, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        tk.Label(main_frame, text="✅ Instalación / Actualización Completa", font=title_font, fg=accent_color, bg=bg_color).pack(anchor="w", pady=(0, 15))
        
        # Sección 1
        tk.Label(main_frame, text="¿QUÉ ES ESTE SISTEMA?", font=h2_font, fg="#4facf7", bg=bg_color).pack(anchor="w", pady=(10, 5))
        desc = "Arquitectura multi-IA (Arquitecto/Dev).\nEl sistema organiza el trabajo en: discusiones -> planes -> código.\nMantiene el estado guardado para que la IA nunca pierda contexto."
        tk.Label(main_frame, text=desc, font=text_font, fg=fg_color, bg=bg_color, justify="left").pack(anchor="w")
        
        # Sección 2
        tk.Label(main_frame, text="🐛 NUEVO: BUG REPORTER (v2.7)", font=h2_font, fg="#4facf7", bg=bg_color).pack(anchor="w", pady=(15, 5))
        bugs = "1. Presiona Alt+R en cualquier momento.\n2. Dibuja rectángulos rojos señalando el error en pantalla.\n3. (NUEVO) Presiona '🎤 Dictar' para describir el error con tu voz.\n4. La IA (Arquitecto) leerá los bugs para planear cómo arreglarlos."
        tk.Label(main_frame, text=bugs, font=text_font, fg=fg_color, bg=bg_color, justify="left").pack(anchor="w")
        
        # Sección 3
        tk.Label(main_frame, text="💡 NUEVO: IDEAS FUTURAS", font=h2_font, fg="#4facf7", bg=bg_color).pack(anchor="w", pady=(15, 5))
        ideas = "Las discusiones ahora tienen una sección de 'Ideas Futuras'.\nLa IA guardará allí ideas que surjan pero que no bloqueen la etapa actual."
        tk.Label(main_frame, text=ideas, font=text_font, fg=fg_color, bg=bg_color, justify="left").pack(anchor="w")

        # Sección 4
        tk.Label(main_frame, text="🔄 SCRIPTS DE EJECUCIÓN", font=h2_font, fg="#4facf7", bg=bg_color).pack(anchor="w", pady=(15, 5))
        scripts = "Usa siempre run.bat o ./run.sh para iniciar tu proyecto.\nEstos scripts arrancan tu app Y lanzan el Bug Reporter en background."
        tk.Label(main_frame, text=scripts, font=text_font, fg=fg_color, bg=bg_color, justify="left").pack(anchor="w")
        
        # Botón cerrar
        btn_frame = tk.Frame(main_frame, bg=bg_color)
        btn_frame.pack(fill="x", pady=(25, 0))
        tk.Button(btn_frame, text="Entendido, ¡A codear!", command=root.destroy, 
                  font=h2_font, bg=accent_color, fg="white", relief="flat", padx=20, pady=8).pack()
        
        # Centrar ventana
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        root.mainloop()
    except Exception as e:
        print(f"\n¡Proceso completo! (Error lanzando interfaz gráfica: {e})")

if __name__ == "__main__":
    mostrar_guia_tkinter()
