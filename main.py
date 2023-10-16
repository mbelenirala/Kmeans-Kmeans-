import tkinter as tk
from tkinter import ttk
import ControladorDataset
import ControladorKmeans
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def cerrar_programa():
    root.quit()
    root.destroy()

def graficar():
    dataset = nroDataset.get()
    k = k_var.get()
    criterioParada = int(nroCritero.get())
    csv = f'./dataset/dataset_{dataset}.csv'
    matriz = ControladorDataset.cargar_dataset(csv)
    centroides, asignaciones, pasos = ControladorKmeans.k_means(matriz, k, criterioParada, 0)
    
    # Muestra los pasos en el área de texto
    texto_area.delete(1.0, tk.END)  # Borra el contenido anterior
    texto_area.insert(tk.END, pasos)

    graficoKmeans(matriz, centroides, asignaciones)

def graficoDataset(dataset):
    for widget in datasetFrame.winfo_children():
        widget.destroy()

    # Grafica el dataset seleccionado
    csv = f'./dataset/dataset_{dataset}.csv'
    matriz = ControladorDataset.cargar_dataset(csv)
    plt.figure(figsize=(5, 5))
    plt.scatter(matriz[:, 0], matriz[:, 1], c='blue', marker='o')
    plt.title(f'Dataset {dataset}')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    dataset_canvas = FigureCanvasTkAgg(plt.gcf(), master=datasetFrame)
    dataset_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Borrar gráfico
    for widget in kmeansFrame.winfo_children():
        widget.destroy()

def graficoKmeans(matriz, centroides, asignaciones):
    # Borrar gráfico
    for widget in kmeansFrame.winfo_children():
        widget.destroy()

    # Grafica los resultados del K-Means
    plt.figure(figsize=(5, 5))
    plt.scatter(matriz[:, 0], matriz[:, 1], c=asignaciones, marker='o')
    plt.scatter(centroides[:, 0], centroides[:, 1], c='red', marker='x', s=100, label='Centroides')
    plt.title('Resultados K-Means')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    kmeans_canvas = FigureCanvasTkAgg(plt.gcf(), master=kmeansFrame)
    kmeans_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("K-Means Visualizer")
root.protocol("WM_DELETE_WINDOW", cerrar_programa)

mainFrame = ttk.Frame(root)
mainFrame.pack(padx=20, pady=20)

datasetFrame = tk.LabelFrame(mainFrame, text="Dataset",font=("Arial", 14))
datasetFrame.grid(row=0, column=0)

kmeansFrame = tk.LabelFrame(mainFrame, text="Resultados K-Means",font=("Arial", 14))
kmeansFrame.grid(row=0, column=1)

controlesFrame = tk.LabelFrame(mainFrame)
controlesFrame.grid(row=1, column=0, columnspan=2)

dataset_label = tk.Label(controlesFrame, text="Seleccionar Dataset:",font=("Arial", 14))
dataset_label.grid(row=0, column=0)

nroDataset = tk.StringVar()
nroDataset.set("1")  # Por defecto, se grafica el 1

# Seleccionar dataset 
def seleccionarDataset():
    seleccion = nroDataset.get()
    graficoDataset(seleccion)  

dataset1_button = ttk.Radiobutton(controlesFrame, text="Dataset 1", variable=nroDataset, value="1", command=seleccionarDataset)
dataset1_button.grid(row=0, column=1)

dataset2_button = ttk.Radiobutton(controlesFrame, text="Dataset 2", variable=nroDataset, value="2", command=seleccionarDataset)
dataset2_button.grid(row=0, column=2)

dataset3_button = ttk.Radiobutton(controlesFrame, text="Dataset 3", variable=nroDataset, value="3", command=seleccionarDataset)
dataset3_button.grid(row=0, column=3)

k_label = tk.Label(controlesFrame, text="Valor de K:",font=("Arial", 14))
k_label.grid(row=1, column=0)
k_var = tk.IntVar()
k_dropdown = ttk.Combobox(controlesFrame, textvariable=k_var, values=[2, 3, 4, 5], state="readonly")
k_dropdown.grid(row=1, column=1)
k_dropdown.set(2)

criterio_label = tk.Label(controlesFrame, text="Criterio de Parada:",font=("Arial", 14))
criterio_label.grid(row=2, column=0)
nroCritero = tk.StringVar()
nroCritero.set("1")  

criterioOpcion1 = ttk.Radiobutton(controlesFrame, text="No haya más asignaciones", variable=nroCritero, value="1")
criterioOpcion1.grid(row=2, column=1)

criterioOpcion2 = ttk.Radiobutton(controlesFrame, text="No haya más cambios en los centroides", variable=nroCritero, value="2")
criterioOpcion2.grid(row=2, column=2)

botonGraficar = ttk.Button(controlesFrame, text="Graficar Resultados", command=graficar, style="TButton")
botonGraficar.grid(row=3, column=0, columnspan=2)

# Configurar el estilo del botón directamente
ttk.Style().configure("TButton", font=("Arial", 12), padding=(10, 5))
ttk.Style().map("TButton", foreground=[("active", "blue")], background=[("active", "lightgray")])

# Agregar un área de texto para mostrar los pasos
texto_area = tk.Text(controlesFrame, height=10, width=40)
texto_area.grid(row=4, column=0, columnspan=3)

graficoDataset("1")

root.mainloop()
