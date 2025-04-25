import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.ticker import MultipleLocator

# # Inicializar PSSE V_36
pssepy_PATH = r"C:\Program Files\PTI\PSSE36\36.1\PSSPY311"
sys.path.append(pssepy_PATH)
import psse36  # type: ignore
import psspy  # type: ignore
psspy.psseinit()

# # Cargar caso de estudio
#case = r"C:\Users\rbojo\Documents\Ing. Electrica\4to Semestre\Escenarios Tesis\VERANO_MAX.sav"
ejem = r"C:\Users\rbojo\Documents\PTI\PSSE36\EXAMPLE\savnw.sav"
psspy.case(case)

## Obtener información de owners
ierr, name_owners = psspy.aownerchar(-1, 1, 'OWNERNAME')
ierr, num_owners = psspy.aownerint(-1, 1, 'NUMBER')

## Configurar subsistemas por owner
 for i, owner in enumerate(num_owners[0]):
     ierr = psspy.bsys(i, 1, [115., 230.], 0, [], 0, [], 1, [owner], 0, [])
     if ierr != 0:
         print(f"Error en la iteración {i} con owner {owner}")
     else:
         print(f"Sistema {i} configurado correctamente para owner {owner}")

 # Diccionario para almacenar los datos por owner
 voltajes_owners = {}

# Obtener datos para cada owner
 for i in range(len(name_owners[0])):
     owner = name_owners[0][i]
    
     ierr, names = psspy.abuschar(i, 2, 'NAME')
     ierr, voltages = psspy.abusreal(i, 2, 'PU')
    
     if ierr == 0:
         nombres_planos = [nombre.strip() for sublist in names for nombre in sublist]
         voltajes_planos = [voltaje for sublist in voltages for voltaje in sublist]
        
         voltajes_owners[owner] = {
             'nombres': nombres_planos,
             'voltajes': voltajes_planos
         }
     else:
         print(f"Error al obtener datos para el owner {owner}")



# Crear gráfico
plt.figure(figsize=(6.2, 4.8))
plt.rcParams['font.family'] = 'Cambria'

# Lista de colores para las zonas
colors = ['#0072B2', '#D55E00', '#009E73', '#d62728', '#9467bd']  # Puedes ajustar esta lista de colores

# Linea por zona
lines_zones = []
for i, (zona, datos) in enumerate(voltajes_owners.items()):
    line, = plt.plot(datos['nombres'], datos['voltajes'], marker='o', color=colors[i % len(colors)], label=zona)
    lines_zones.append(line)

# Límites de referencia
lim_inf = plt.axhline(y=0.95, color='#a9a9a9', linestyle='--', label='0.95')
lim_sup = plt.axhline(y=1.05, color='#a9a9a9', linestyle='--', label='1.05')

# Etiquetas y configuración del eje
plt.xlabel('Subestación', fontsize=11)
plt.ylabel('Voltaje (p.u)', fontsize=11)
plt.xticks(rotation=90, fontsize=8)

# Leyenda de zonas
legend_zones = plt.legend(
    handles=lines_zones,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.25),
    ncol=3,
    frameon=True,
    title="Zona",
    title_fontsize=10,
    borderpad=0.5,
)

# Texto que simula la leyenda de límites operativos (ESQUINA SUPERIOR DERECHA DENTRO DEL GRÁFICO)
leyenda_texto = '-- Límite operativo (0.95)\n -- Límite operativo (1.05)'
plt.text(
    0.85, 0.9, leyenda_texto,
    transform=plt.gca().transAxes,
    fontsize=9,
    ha='center',
    va='top',
    bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray')
)


plt.tight_layout()
plt.savefig("voltajes.png", dpi=300, bbox_inches='tight')
plt.show()
