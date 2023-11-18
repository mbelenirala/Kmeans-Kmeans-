import tkinter as tk
from tkinter import ttk
import ControladorDataset
import ControladorKmeans
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import screeninfo
from PIL import Image, ImageTk
from tkinter import filedialog


global nuevo_dataset_path 

def cerrar_programa():
    root.quit()
    root.destroy()

def graficoKmeans(matriz, centroides_iniciales,centroides, asignaciones, titulo, marco):
    for widget in marco.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(matriz[:, 0], matriz[:, 1], c=asignaciones, marker='o')
    for i, (x, y) in enumerate(zip(centroides[:, 0], centroides[:, 1])):
        ax.scatter(x, y, c='red', marker='x', s=100, label=f'Centroide Final {i + 1}')
        ax.text(x + 0.02, y, f'C{i + 1}({x:.2f}, {y:.2f})', fontsize=10, ha='left', va='center', color='darkred', fontweight='bold')
    for i, (x, y) in enumerate(zip(centroides_iniciales[:, 0], centroides_iniciales[:, 1])):
        ax.scatter(x, y, c='blue', marker='x', s=100, label=f'Centroide Inicial {i + 1}')
        ax.text(x + 0.02, y, f'C{i + 1}({x:.2f}, {y:.2f})', fontsize=10, ha='left', va='center', color='darkblue', fontweight='bold')
    ax.set_title(titulo)
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    
    ax.set_xticks(range(int(matriz[:, 0].min()) - 1, int(matriz[:, 0].max()) + 2, 1))
    ax.set_yticks(range(int(matriz[:, 1].min()) - 1, int(matriz[:, 1].max()) + 2, 1))

    ax.grid(True, alpha=0.5)

    kmeans_canvas = FigureCanvasTkAgg(fig, master=marco)
    kmeans_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def cerrar_programa():
    root.quit()
    root.destroy()

def graficoDataset(dataset):
    for widget in datasetFrame.winfo_children():
        widget.destroy()

    csv = f'./dataset/dataset_{dataset}.csv'
    matriz = ControladorDataset.cargar_dataset(csv)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(matriz[:, 0], matriz[:, 1], c='blue', marker='o')
    ax.set_title(f'Dataset {dataset}')
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')

    ax.set_xticks(range(int(matriz[:, 0].min()) - 1, int(matriz[:, 0].max()) + 2, 1))
    ax.set_yticks(range(int(matriz[:, 1].min()) - 1, int(matriz[:, 1].max()) + 2, 1))

    ax.grid(True, alpha=0.5)

    dataset_canvas = FigureCanvasTkAgg(fig, master=datasetFrame)
    dataset_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Borrar gráfico
    for widget in kmeansFrame.winfo_children():
        widget.destroy()
    for widget in kmeansPlusFrame.winfo_children():
        widget.destroy()

def graficarNuevoDataset(dataset):
    for widget in datasetFrame.winfo_children():
        widget.destroy()

    # Graficar el nuevo dataset
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(dataset[:, 0], dataset[:, 1], c='blue', marker='o')
    ax.set_title(f'Nuevo Dataset')
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')

    ax.set_xticks(range(int(dataset[:, 0].min()) - 1, int(dataset[:, 0].max()) + 2, 1))
    ax.set_yticks(range(int(dataset[:, 1].min()) - 1, int(dataset[:, 1].max()) + 2, 1))

    ax.grid(True, alpha=0.5)

    dataset_canvas = FigureCanvasTkAgg(fig, master=datasetFrame)
    dataset_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Borrar gráfico
    for widget in kmeansFrame.winfo_children():
        widget.destroy()
    for widget in kmeansPlusFrame.winfo_children():
        widget.destroy()

def graficar():
    dataset = nroDataset.get()
    k = k_var.get()
    if dataset != '4':
        csv = f'./dataset/dataset_{dataset}.csv'
    else:
        #aca modificar para que agarre el .csv del nuevo dataset 
        csv =  nuevo_dataset_path
    matriz = ControladorDataset.cargar_dataset(csv)
    

    centroides_iniciales_kmeans,centroides_kmeans, asignaciones_kmeans, pasos_kmeans = ControladorKmeans.k_means(matriz, k, 1)
    centroides_iniciales_kmeansplus,centroides_kmeans_plus, asignaciones_kmeans_plus, pasos_kmeans_plus = ControladorKmeans.k_means(matriz, k, 0)

    texto_area.delete(1.0, tk.END)  # Borra el contenido anterior
    texto_area.insert(tk.END, f'Pasos K-Means:\n{pasos_kmeans}\n')
    texto_area_kmeans_plus.delete(1.0, tk.END)  
    texto_area_kmeans_plus.insert(tk.END, f'Pasos K-Means++:\n{pasos_kmeans_plus}')

    graficoKmeans(matriz, centroides_iniciales_kmeans, centroides_kmeans, asignaciones_kmeans, "Resultados K-Means", kmeansFrame)
    graficoKmeans(matriz, centroides_iniciales_kmeansplus,centroides_kmeans_plus, asignaciones_kmeans_plus, "Resultados K-Means++", kmeansPlusFrame)

root = tk.Tk()
root.title("K-Means")
root.protocol("WM_DELETE_WINDOW", cerrar_programa)

screen = screeninfo.get_monitors()[0]
width, height = screen.width, screen.height

root.geometry(f"{width}x{height}")
root.state("zoomed")
# Crear un Canvas para agregar barras de desplazamiento
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear barras de desplazamiento
y_scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
y_scrollbar.pack(side=tk.RIGHT, fill="y")
canvas.configure(yscrollcommand=y_scrollbar.set)

# Crear una barra de desplazamiento horizontal en la parte superior
x_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
x_scrollbar.pack(side=tk.TOP, fill="x")
canvas.configure(xscrollcommand=x_scrollbar.set)

# Crear un nuevo frame dentro del canvas
mainFrame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=mainFrame, anchor="nw")

# Permitir desplazamiento con el mouse
def _on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas.bind("<Configure>", _on_canvas_configure)

datasetFrame = tk.LabelFrame(mainFrame, text="Dataset", font=("Arial", 14))
datasetFrame.grid(row=0, column=0)

kmeansFrame = tk.LabelFrame(mainFrame, text="Resultados K-Means", font=("Arial", 14))
kmeansFrame.grid(row=0, column=1)

kmeansPlusFrame = tk.LabelFrame(mainFrame, text="Resultados K-Means++", font=("Arial", 14))
kmeansPlusFrame.grid(row=0, column=2)

referenciasFrame = tk.LabelFrame(mainFrame, text="Referencias Gráficas", font=("Arial", 14))
referenciasFrame.grid(row=1, column=0)

controlesFrame = tk.LabelFrame(mainFrame)
controlesFrame.grid(row=2, column=0, columnspan=3, rowspan=2)

nroDataset = tk.StringVar()
nroDataset.set("1")  # Por defecto se grafica el dataset1

# Seleccionar dataset 
def seleccionarDataset():
    seleccion = nroDataset.get()
    if (seleccion != '4'):
       cargar_nuevo_dataset_button["state"] =  tk.DISABLED
       graficoDataset(seleccion)
    else:
        if (seleccion == '4'):
            cargar_nuevo_dataset_button["state"] = tk.NORMAL 
    

refDataset_label = tk.Label(referenciasFrame, text="Dato del dataset:", font=("Arial", 10))
refDataset_label.grid(row=0, column=0)
#REF IMG Dataset
imgRefDataset = ImageTk.PhotoImage(Image.open("img/imgRefDataset.png"))
imgRefDataset_label = tk.Label(referenciasFrame, image=imgRefDataset)
imgRefDataset_label.grid(row=0, column=1)

refKmeans_label = tk.Label(referenciasFrame, text="Dato de un cluster:", font=("Arial", 10))
refKmeans_label.grid(row=0, column=2)
#REF IMG Cluster 1
imgRefCluster1 = ImageTk.PhotoImage(Image.open("img/imgRefCluster1.png"))
imgRefCluster1_label = tk.Label(referenciasFrame, image=imgRefCluster1)
imgRefCluster1_label.grid(row=0, column=3)
#REF IMG Cluster 2
imgRefCluster2 = ImageTk.PhotoImage(Image.open("img/imgRefCluster2.png"))
imgRefCluster2_label = tk.Label(referenciasFrame, image=imgRefCluster2)
imgRefCluster2_label.grid(row=0, column=4)
#REF IMG Cluster 3
imgRefCluster3 = ImageTk.PhotoImage(Image.open("img/imgRefCluster3.png"))
imgRefCluster3_label = tk.Label(referenciasFrame, image=imgRefCluster3)
imgRefCluster3_label.grid(row=0, column=5)
#REF IMG Cluster 4
imgRefCluster4 = ImageTk.PhotoImage(Image.open("img/imgRefCluster4.png"))
imgRefCluster4_label = tk.Label(referenciasFrame, image=imgRefCluster4)
imgRefCluster4_label.grid(row=0, column=6)
#REF IMG Cluster 5
imgRefCluster5 = ImageTk.PhotoImage(Image.open("img/imgRefCluster5.png"))
imgRefCluster5_label = tk.Label(referenciasFrame, image=imgRefCluster5)
imgRefCluster5_label.grid(row=0, column=7)

refCentroide_label = tk.Label(referenciasFrame, text="Centroide final:", font=("Arial", 10))
refCentroide_label.grid(row=0, column=8)
#REF IMG Centroide
imgRefCentroide = ImageTk.PhotoImage(Image.open("img/imgRefCentroide.png"))
imgRefCentroide_label = tk.Label(referenciasFrame, image=imgRefCentroide)
imgRefCentroide_label.grid(row=0, column=9)

refCentroideIni_label = tk.Label(referenciasFrame, text="Centroide Inicial:", font=("Arial", 10))
refCentroideIni_label.grid(row=0, column=10)
#REF IMG Centroide
imgRefCentroideIni = ImageTk.PhotoImage(Image.open("img/imgRefCentroideIni.png"))
imgRefCentroideIni_label = tk.Label(referenciasFrame, image=imgRefCentroideIni)
imgRefCentroideIni_label.grid(row=0, column=111)

dataset1_button = ttk.Radiobutton(controlesFrame, text="Dataset 1", variable=nroDataset, value="1", command=seleccionarDataset)
dataset1_button.grid(row=0, column=1)

dataset2_button = ttk.Radiobutton(controlesFrame, text="Dataset 2", variable=nroDataset, value="2", command=seleccionarDataset)
dataset2_button.grid(row=0, column=2)

dataset3_button = ttk.Radiobutton(controlesFrame, text="Dataset 3", variable=nroDataset, value="3", command=seleccionarDataset)
dataset3_button.grid(row=0, column=3)

dataset4_button = ttk.Radiobutton(controlesFrame, text="Otro ", variable=nroDataset, value="4", command=seleccionarDataset)
dataset4_button.grid(row=0, column=4)


def cargarNuevoDataset():
    global nuevo_dataset_path
    try:
        nuevo_dataset_path = filedialog.askopenfilename(title="Seleccionar Dataset", filetypes=[("Archivos CSV", "*.csv")])

        if nuevo_dataset_path:
            nuevo_dataset = ControladorDataset.cargar_dataset(nuevo_dataset_path)

            # Realiza las operaciones necesarias con el nuevo dataset, por ejemplo, graficarlo
            graficarNuevoDataset(nuevo_dataset)
    except Exception as e:
        tk.messagebox.showerror("Error", f"Ocurrió un error al cargar el nuevo dataset: {str(e)}")


cargar_nuevo_dataset_button = ttk.Button(controlesFrame, text="Cargar Nuevo Dataset", command=cargarNuevoDataset, style="TButton", state=tk.DISABLED)
cargar_nuevo_dataset_button.grid(row=0, column=6, columnspan=2)

k_label = tk.Label(controlesFrame, text="Valor de K:", font=("Arial", 14))
k_label.grid(row=1, column=0)
k_var = tk.IntVar()
k_dropdown = ttk.Combobox(controlesFrame, textvariable=k_var, values=[2, 3, 4, 5], state="readonly")
k_dropdown.grid(row=1, column=1)
k_dropdown.set(2)

botonGraficar = ttk.Button(controlesFrame, text="Graficar Resultados", command=graficar, style="TButton")
botonGraficar.grid(row=3, column=0, columnspan=2)

ttk.Style().configure("TButton", font=("Arial", 12), padding=(10, 5))
ttk.Style().map("TButton", foreground=[("active", "blue")], background=[("active", "lightgray")])

pasoskmeans = tk.Label(controlesFrame, text="Paso a paso K-means", font=("Arial", 14))
pasoskmeans.grid(row=4, column=0)
texto_area = tk.Text(controlesFrame, height=10, width=40)
texto_area.grid(row=5, column=0, padx=5)

pasoskmeanspp = tk.Label(controlesFrame, text="Paso a paso K-means++", font=("Arial", 14))
pasoskmeanspp.grid(row=4, column=2)
texto_area_kmeans_plus = tk.Text(controlesFrame, height=10, width=40)
texto_area_kmeans_plus.grid(row=5, column=2, padx=5)

graficoDataset("1")

root.mainloop()
