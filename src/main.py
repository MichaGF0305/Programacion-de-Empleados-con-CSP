# src/main.py

import json
import os
import sys

# Añadir la ruta del directorio 'src' al path de Python para asegurar que las importaciones funcionen
# al ejecutar desde la raíz del proyecto.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import Habilidad, Departamento, Empleado, Turno
from src.solver import CSP_Solver

def ejecutar_pruebas():
    # Rutas relativas a la raíz del proyecto
    carpeta_raiz = 'pruebas'
    carpeta_sin_solucion = os.path.join(carpeta_raiz, 'sin_solucion')
    carpeta_con_solucion = os.path.join(carpeta_raiz, 'con_solucion')

    if not os.path.exists(carpeta_sin_solucion):
        print(f"Error: La carpeta de pruebas '{carpeta_sin_solucion}' no existe.")
        print("Asegúrate de ejecutar este script desde la raíz del proyecto.")
        return
        
    if not os.path.exists(carpeta_con_solucion):
        os.makedirs(carpeta_con_solucion)

    archivos_de_prueba = sorted([f for f in os.listdir(carpeta_sin_solucion) if f.endswith('.json')])
    total_pruebas, pruebas_resueltas = len(archivos_de_prueba), 0

    print(f"--- INICIANDO EJECUCIÓN DE {total_pruebas} PRUEBAS ---")

    for nombre_archivo in archivos_de_prueba:
        print(f"\n--- Procesando archivo: {nombre_archivo} ---")
        ruta_archivo = os.path.join(carpeta_sin_solucion, nombre_archivo)

        with open(ruta_archivo, 'r') as f:
            datos = json.load(f)

        habilidades = {nombre: Habilidad(nombre) for nombre in datos['habilidades']}
        departamentos = {d['nombre']: Departamento(d['nombre'], [habilidades[h] for h in d['habilidades_requeridas']]) for d in datos['departamentos']}
        empleados = [Empleado(e['nombre'], [habilidades[h] for h in e['habilidades']], e.get('disponibilidad', None)) for e in datos['empleados']]
        turnos = [Turno(t['id'], t['dia'], t['hora_inicio'], t['hora_fin'], departamentos[t['departamento']]) for t in datos['turnos']]

        solver = CSP_Solver(turnos, empleados)
        solver.inicializar_csp()
        
        solucion_final, metodo_usado = None, ""
        if solver.ac3():
            if all(len(d) == 1 for d in solver.dominios.values()):
                solucion_final = {t.id: solver.dominios[t.id][0] for t in solver.variables}
                metodo_usado = "AC-3"
            else:
                solucion_bts = solver.backtrack({})
                if solucion_bts:
                    solucion_final = solucion_bts
                    metodo_usado = "BTS"
        
        if solucion_final:
            pruebas_resueltas += 1
            print(f"✅ ¡Solución encontrada con {metodo_usado}!")
            resultado_json = {
                "archivo_problema": nombre_archivo,
                "metodo_solucion": metodo_usado,
                "asignacion": [{"turno_id": tid, "empleado_asignado": emp.nombre} for tid, emp in sorted(solucion_final.items())]
            }
            ruta_solucion = os.path.join(carpeta_con_solucion, nombre_archivo)
            with open(ruta_solucion, 'w') as f:
                json.dump(resultado_json, f, indent=2)
        else:
            print("❌ No se encontró una solución para este problema.")

    print(f"\n--- RESUMEN FINAL ---")
    print(f"Pruebas procesadas: {total_pruebas}")
    print(f"Pruebas resueltas con éxito: {pruebas_resueltas}")
    print(f"Porcentaje de éxito: {pruebas_resueltas / total_pruebas:.1%}" if total_pruebas > 0 else "N/A")
    print("Las soluciones han sido guardadas en la carpeta 'pruebas/con_solucion/'.")

if __name__ == "__main__":
    ejecutar_pruebas()