""" 
Sriopt to generate graph for renewable integration level in a determined .sav file
This script retrieves data from the machine information:
-Gets MW rating of each generator
-Gets the type of generation: Renewable or Conventional
-Calculates the renewable integration level
-Generates a pie chart to visualize the renewable integration level 
 """

# Obtener el numero de generadores en el sistema
# Ciclo para obtener la potencia MW a la que esta operando cada generador y si es renovable o convencional
# Calcular el nivel de integracion renovable 
# Generar un grafico de pastel para visualizar el nivel de integracion renovable
# Dar un pequeño reporte de los resultados obtenidos en la consola

import matplotlib.pyplot as plt

conv = []   
nconv = []  

ierr, gen_id = psspy.amachchar(-1,1,'ID')
ierr, gen_bus = psspy.amachint(-1,1,'NUMBER')
ierr, gen_mw = psspy.amachreal(-1, 1, 'PGEN')

for mid, ibus, pgen in zip(gen_id[0], gen_bus[0], gen_mw[0]):
    ierr, wmod = psspy.macint(ibus, mid, 'WMOD')
    if wmod == 0:
        conv.append((ibus, mid, pgen, wmod))
    elif 1 <= wmod <= 3:
        nconv.append((ibus, mid, pgen, wmod))

conv_mw  = sum(p for _, _, p, _ in conv)
nconv_mw = sum(p for _, _, p, _ in nconv)

print(f"Conventional generation: {conv_mw:.2f}  MW")
print(f"Renewable generation: {nconv_mw:.2f} MW")

# Gráfica de pastel
labels = ['Conventional', 'Renewable']
sizes  = [conv_mw, nconv_mw]

fig, ax = plt.subplots(figsize=(5,5))
ax.pie(sizes, labels=labels, autopct=lambda pct: f'{pct:.1f}%', startangle=90)
ax.axis('equal')
ax.set_title('Renewable Integration Level', fontsize=14)
plt.show()