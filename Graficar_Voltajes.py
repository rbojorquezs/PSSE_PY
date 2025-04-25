import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.ticker import MultipleLocator

# # Inicializar PSSE V_36
# pssepy_PATH = r"C:\Program Files\PTI\PSSE36\36.1\PSSPY311"
# sys.path.append(pssepy_PATH)
# import psse36  # type: ignore
# import psspy  # type: ignore
# psspy.psseinit()

# # Cargar caso de estudio
# case = r"C:\Users\rbojo\Documents\Ing. Electrica\4to Semestre\Escenarios Tesis\VERANO_MAX.sav"
# ejem = r"C:\Users\rbojo\Documents\PTI\PSSE36\EXAMPLE\savnw.sav"
# psspy.case(case)

# # Obtener información de owners
# ierr, name_owners = psspy.aownerchar(-1, 1, 'OWNERNAME')
# ierr, num_owners = psspy.aownerint(-1, 1, 'NUMBER')

# # Configurar subsistemas por owner
# for i, owner in enumerate(num_owners[0]):
#     ierr = psspy.bsys(i, 1, [115., 230.], 0, [], 0, [], 1, [owner], 0, [])
#     if ierr != 0:
#         print(f"Error en la iteración {i} con owner {owner}")
#     else:
#         print(f"Sistema {i} configurado correctamente para owner {owner}")

# # Diccionario para almacenar los datos por owner
# voltajes_owners = {}

# # Obtener datos para cada owner
# for i in range(len(name_owners[0])):
#     owner = name_owners[0][i]
    
#     ierr, names = psspy.abuschar(i, 2, 'NAME')
#     ierr, voltages = psspy.abusreal(i, 2, 'PU')
    
#     if ierr == 0:
#         nombres_planos = [nombre.strip() for sublist in names for nombre in sublist]
#         voltajes_planos = [voltaje for sublist in voltages for voltaje in sublist]
        
#         voltajes_owners[owner] = {
#             'nombres': nombres_planos,
#             'voltajes': voltajes_planos
#         }
#     else:
#         print(f"Error al obtener datos para el owner {owner}")

# print(voltajes_owners)

voltajes_owners={'LA PAZ      ': {'nombres': ['ASU-115', 'COR-230', 'BLE-115', 'ETR-115', 'LPZ-115', 'OLA-115', 'OLA-230', 'PAA-115', 'PUP-115', 'PUP-115B', 'RCO-115', 'REA-115', 'RFO-115', 'RFO-F01', 'AST-115', 'CAR-115', 'LFI-115', 'EOL-115', 'ERE-115', 'PCH-115'], 'voltajes': [1.008227825164795, 1.0145717859268188, 1.0044522285461426, 0.9849241375923157, 0.9973538517951965, 1.008029818534851, 1.0139319896697998, 1.0008846521377563, 1.0046806335449219, 1.0050020217895508, 1.0053801536560059, 1.0109773874282837, 1.0030803680419922, 1.0115889310836792, 1.0081382989883423, 0.9897531867027283, 1.0102490186691284, 1.0102468729019165, 1.0041170120239258, 1.005561351776123]}, 'LOS CABOS   ': {'nombres': ['ASJ-115', 'CAB-115', 'CAD-115', 'CAS-115', 'CRE-115', 'DES-115', 'DES-F01', 'ELP-115', 'ELP-230', 'ELP-F01', 'PML-115', 'SJC-115', 'SNT-115', 'TCB-115', 'CAF-115', 'MOR-115', 'TCB-230'], 'voltajes': [0.9856927990913391, 0.9934890270233154, 0.9969985485076904, 0.9916285872459412, 0.9963159561157227, 0.999748170375824, 0.9999037384986877, 0.9991272687911987, 1.0111000537872314, 1.0199999809265137, 0.992061197757721, 0.9897936582565308, 0.9790841937065125, 1.0049858093261719, 0.998222827911377, 0.9866102933883667, 1.0096689462661743]}, 'CONSTITUCION': {'nombres': ['DOM-115', 'GAO-115', 'INS-115', 'LAP-115', 'LRO-115', 'PES-115', 'VIO-115', 'SOL-115', 'TOB-115'], 'voltajes': [1.0005711317062378, 1.0162397623062134, 1.0006084442138672, 1.0125869512557983, 0.9692655801773071, 0.9743277430534363, 1.0062583684921265, 1.0006084442138672, 1.0006285905838013]}}
# Renombrar las claves directamente en el mismo diccionario
voltajes_owners['La Paz'] = voltajes_owners.pop('LA PAZ      ')
voltajes_owners['Los Cabos'] = voltajes_owners.pop('LOS CABOS   ')
voltajes_owners['Constitución'] = voltajes_owners.pop('CONSTITUCION')

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