# src/solver.py

import copy
import datetime
from collections import deque
from typing import List, Dict, Optional

# La importación relativa (.) funciona porque ambos archivos están en el paquete 'src'
from .models import Turno, Empleado, DIAS_SEMANA

class CSP_Solver:
    """
    Clase que encapsula toda la lógica para resolver el problema de asignación de turnos
    mediante técnicas de Satisfacción de Restricciones (CSP), incluyendo AC-3 y Backtracking.
    """
    def __init__(self, turnos: List[Turno], empleados: List[Empleado]):
        self.variables: List[Turno] = turnos
        self.empleados: List[Empleado] = empleados
        self.dominios: Dict[str, List[Empleado]] = {}
        self.vecinos: Dict[str, List[Turno]] = {}

    def inicializar_csp(self):
        self._inicializar_dominios()
        self._construir_vecinos()

    def _inicializar_dominios(self):
        for turno in self.variables:
            self.dominios[turno.id] = [
                emp for emp in self.empleados
                if emp.puede_trabajar(turno.dia) and
                   emp.tiene_todas_las_habilidades(turno.departamento.habilidades_requeridas)
            ]

    def _construir_vecinos(self):
        for turno in self.variables: self.vecinos[turno.id] = []
        dias_map = {dia: idx for idx, dia in enumerate(DIAS_SEMANA)}
        minutos_descanso = 8 * 60
        for i in range(len(self.variables)):
            for j in range(i + 1, len(self.variables)):
                t1, t2 = self.variables[i], self.variables[j]
                if t1.dia == t2.dia:
                    self.vecinos[t1.id].append(t2)
                    self.vecinos[t2.id].append(t1)
                    continue
                fin_t1_min = (dias_map[t1.dia]*24*60) + (t1.hora_fin*60)
                if t1.hora_fin < t1.hora_inicio: fin_t1_min += 24*60
                inicio_t2_min = (dias_map[t2.dia]*24*60) + (t2.hora_inicio*60)
                fin_t2_min = (dias_map[t2.dia]*24*60) + (t2.hora_fin*60)
                if t2.hora_fin < t2.hora_inicio: fin_t2_min += 24*60
                inicio_t1_min = (dias_map[t1.dia]*24*60) + (t1.hora_inicio*60)
                if abs(inicio_t2_min - fin_t1_min) < minutos_descanso or abs(inicio_t1_min - fin_t2_min) < minutos_descanso:
                    self.vecinos[t1.id].append(t2)
                    self.vecinos[t2.id].append(t1)

    def revise(self, turno_i: Turno, turno_j: Turno) -> bool:
        revisado = False
        for empleado_x in list(self.dominios[turno_i.id]):
            if len(self.dominios[turno_j.id]) == 1 and self.dominios[turno_j.id][0] == empleado_x:
                self.dominios[turno_i.id].remove(empleado_x)
                revisado = True
        return revisado

    def ac3(self) -> bool:
        cola = deque([(t_i, t_j) for t_i in self.variables for t_j in self.vecinos[t_i.id]])
        while cola:
            turno_i, turno_j = cola.popleft()
            if self.revise(turno_i, turno_j):
                if not self.dominios[turno_i.id]: return False
                for turno_k in self.vecinos[turno_i.id]:
                    if turno_k != turno_j: cola.append((turno_k, turno_i))
        return True

    def backtrack(self, asignacion: Dict[str, Empleado]) -> Optional[Dict[str, Empleado]]:
        if len(asignacion) == len(self.variables): return asignacion
        turno_a_asignar = self.seleccionar_variable_mrv(asignacion)
        for empleado_valor in self.dominios[turno_a_asignar.id]:
            dominios_originales = copy.deepcopy(self.dominios)
            asignacion[turno_a_asignar.id] = empleado_valor
            if self.forward_checking(turno_a_asignar, empleado_valor, asignacion):
                resultado = self.backtrack(asignacion)
                if resultado is not None: return resultado
            del asignacion[turno_a_asignar.id]
            self.dominios = dominios_originales
        return None

    def seleccionar_variable_mrv(self, asignacion: Dict[str, Empleado]) -> Turno:
        variables_no_asignadas = [v for v in self.variables if v.id not in asignacion]
        return min(variables_no_asignadas, key=lambda v: len(self.dominios[v.id]))

    def forward_checking(self, turno_actual: Turno, valor_asignado: Empleado, asignacion: Dict[str, Empleado]) -> bool:
        for vecino in self.vecinos[turno_actual.id]:
            if vecino.id not in asignacion and valor_asignado in self.dominios[vecino.id]:
                self.dominios[vecino.id].remove(valor_asignado)
                if not self.dominios[vecino.id]: return False
        return True