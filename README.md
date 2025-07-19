# M1 - Proyecto 1: Planificador Inteligente de Turnos con CSP

## 📝 Descripción del Proyecto

Este proyecto implementa un **planificador inteligente de turnos para empleados** utilizando técnicas de Inteligencia Artificial, específicamente **Problemas de Satisfacción de Restricciones (CSP)**. El sistema asigna empleados a una lista de turnos de manera automática, asegurando el cumplimiento de un conjunto de reglas y restricciones complejas.

El objetivo principal es encontrar una asignación válida que cumpla con todas las **restricciones duras**, tales como:
- La **disponibilidad** de cada empleado.
- Las **habilidades requeridas** por cada departamento para un turno.
- Un empleado **no puede cubrir dos turnos al mismo tiempo**.
- Se debe garantizar un **descanso mínimo de 8 horas** entre los turnos de un mismo empleado.
- Un empleado solo puede cubrir **un turno por día**.
- Todos los turnos deben ser cubiertos.

## 🛠️ Arquitectura de la Solución

El solucionador está construido en Python y utiliza un enfoque híbrido de dos fases para garantizar eficiencia y correctitud:

1.  **AC-3 (Arc Consistency Algorithm #3)**: Como primer paso, se ejecuta este algoritmo de pre-procesamiento para podar los dominios. Elimina las asignaciones de empleado-turno que son localmente inconsistentes, reduciendo drásticamente el espacio de búsqueda para el siguiente paso. Si AC-3 reduce todos los dominios a un solo valor, el problema se resuelve en esta fase.

2.  **Backtrack Search (Búsqueda con Vuelta Atrás)**: Si AC-3 no encuentra una solución única, se invoca un algoritmo de búsqueda en profundidad (DFS). Este explora sistemáticamente las asignaciones restantes y está optimizado con dos heurísticas clave:
    - **MRV (Minimum Remaining Values)**: Para decidir qué turno asignar a continuación, se elige el que tiene el dominio más pequeño (menos empleados posibles). Esto permite "fallar rápido" y podar ramas más grandes del árbol de búsqueda.
    - **Forward Checking**: Después de asignar un empleado a un turno, esta asignación se propaga a los turnos vecinos no asignados, eliminando al empleado de sus dominios y previniendo futuros conflictos.

## 📂 Estructura del Repositorio

El proyecto está organizado de la siguiente manera para promover la modularidad y la claridad:

├── pruebas/
│ ├── sin_solucion/ # Contiene los 20 casos de prueba en formato .json
│ └── con_solucion/ # Directorio donde se guardan las soluciones encontradas
│
├── src/
│ ├── init.py # Marca 'src' como un paquete de Python
│ ├── models.py # Clases de datos: Empleado, Turno, Departamento, Habilidad
│ ├── solver.py # La clase CSP_Solver con los algoritmos AC-3 y Backtrack
│ └── main.py # Script principal que ejecuta el corredor de pruebas
│
└── README.md # Esta documentación


## 🚀 Instrucciones de Uso

Para ejecutar el planificador y resolver los 20 casos de prueba, sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2.  **Asegúrate de tener Python 3 instalado.** No se requieren librerías externas.

3.  **Ejecuta el script principal desde el directorio raíz del proyecto.** Es importante usar el flag `-m` para que Python reconozca la estructura del paquete:
    ```bash
    python -m src.main
    ```

El programa procesará cada uno de los 20 archivos `.json` ubicados en la carpeta `pruebas/sin_solucion/`. Para cada prueba, imprimirá en la consola si se encontró una solución y con qué método (`AC-3` o `BTS`).

## 📊 Ejemplos de Ejecución

Al ejecutar el comando, verás una salida similar a esta en tu terminal:

--- INICIANDO EJECUCIÓN DE 20 PRUEBAS ---
--- Procesando archivo: test_01.json ---
✅ ¡Solución encontrada con AC-3!
--- Procesando archivo: test_02.json ---
✅ ¡Solución encontrada con BTS!
--- Procesando archivo: test_08.json ---
❌ No se encontró una solución para este problema.
...
--- RESUMEN FINAL ---
Pruebas procesadas: 20
Pruebas resueltas con éxito: 17
Porcentaje de éxito: 85.0%
Las soluciones han sido guardadas en la carpeta 'pruebas/con_solucion/'.


Las soluciones generadas se guardarán como archivos `.json` en la carpeta `pruebas/con_solucion/`, detallando el método utilizado y la asignación final de empleado por turno.

### Captura de Pantalla
_(Opcional pero muy recomendado: Añade aquí una captura de pantalla de la terminal mostrando la ejecución del programa)._



---