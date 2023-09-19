import numpy as np
import csv
import matplotlib.pyplot as plt

#convertir CSV to Array text
csv_filename = './dataset/dataset_1.csv'
with open(csv_filename,newline='', encoding='utf-8') as f:
    reader = csv.reader(f,delimiter=';') 
    next(reader) #omite el encabezado
    array_csv_lista = list(reader)
    array_text_lista = np.array(array_csv_lista) #convierte lista en array
   
   #convertir x,y elemento a float
    x = array_text_lista[0][0]
    x_float = float(x.replace(',', '.'))
    y = array_text_lista[0][1]
    y_float = float(y.replace(',', '.'))

#graficar el bendito punto
plt.plot(x_float,y_float,marker ="o")
plt.show()