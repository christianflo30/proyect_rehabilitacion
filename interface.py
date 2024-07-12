import tkinter as tk
from tkinter import ttk
import subprocess

# Función para iniciar el procesamiento con los parámetros seleccionados
def start_processing():
    
    try:
         angulo_semi_circulo_inter= int(angle_var.get())
         Repeticiones_inter = int(reps_var.get())
         print(f"Ángulo seleccionado: {angulo_semi_circulo_inter}")
         print(f"Número de repeticiones: {Repeticiones_inter}")
        
        # Iniciar el script de procesamiento con los parámetros seleccionados
         subprocess.run(["python", "Lectura_postura_mediapipe.py", str(angulo_semi_circulo_inter), str(Repeticiones_inter)])
    except ValueError:
        print("Please enter valid integers for angle and repetitions.")

# Crear la ventana principal
root = tk.Tk()
root.title("Fisioterapia en casa")

# Variables para los parámetros
angle_var = tk.StringVar()
reps_var = tk.StringVar()

# Crear y organizar los widgets
#tk.Frame.config(width=1200,height=750)
imagen_logo = tk.PhotoImage(file="logo_final.png")
tk.Label(root,image=imagen_logo).pack(pady=5)
tk.Label(root, text="Escoge la semana de terapia:").pack(pady=10)

angles_frame = tk.Frame(root)
angles_frame.pack(pady=5)

for angle in [("Semana 1"),("Semana 2"),("Semana 3"),("Semana 4")]:
    if angle == "Semana 1":
        angle_p = 70
    elif angle == "Semana 2":
        angle_p = 45
    elif angle == "Semana 3":
        angle_p = 25
    elif angle == "Semana 4":
        angle_p = 0


    ttk.Radiobutton(angles_frame, text=f"{angle}", variable=angle_var, value=str(angle_p)).pack(side=tk.LEFT)

tk.Label(root, text="Pon el numero de repeticones").pack(pady=10)
ttk.Entry(root, textvariable=reps_var).pack(pady=5)

ttk.Button(root, text="Start", command=start_processing).pack(pady=20)

# Iniciar el loop de la interfaz
root.mainloop()
