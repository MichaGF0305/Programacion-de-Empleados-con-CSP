# src/models.py

from typing import List, Dict, Optional

# Constante para los días de la semana
DIAS_SEMANA = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

class Habilidad:
    """Representa una habilidad única que un empleado puede poseer."""
    def __init__(self, nombre: str):
        self.nombre = nombre

    def __repr__(self) -> str:
        return f"Habilidad({self.nombre})"

    def __eq__(self, other):
        return isinstance(other, Habilidad) and self.nombre == other.nombre
    
    def __hash__(self):
        return hash(self.nombre)


class Departamento:
    """Representa un departamento que tiene turnos y requiere habilidades específicas."""
    def __init__(self, nombre: str, habilidades_requeridas: List[Habilidad]):
        self.nombre = nombre
        self.habilidades_requeridas = habilidades_requeridas

    def __repr__(self) -> str:
        return f"Departamento({self.nombre})"


class Empleado:
    """Representa a un empleado con sus habilidades y su disponibilidad."""
    def __init__(self, nombre: str, habilidades: List[Habilidad], disponibilidad: Optional[Dict[str, bool]] = None):
        self.nombre = nombre
        self.habilidades = set(habilidades)

        if disponibilidad is None:
            self.disponibilidad = {dia: True for dia in DIAS_SEMANA}
        else:
            self.disponibilidad = disponibilidad

    def tiene_habilidad(self, habilidad_requerida: Habilidad) -> bool:
        return habilidad_requerida in self.habilidades

    def tiene_todas_las_habilidades(self, habilidades_requeridas: List[Habilidad]) -> bool:
        return all(self.tiene_habilidad(h) for h in habilidades_requeridas)

    def puede_trabajar(self, dia: str) -> bool:
        return self.disponibilidad.get(dia, False)

    def __repr__(self) -> str:
        return f"Empleado({self.nombre})"


class Turno:
    """Representa un turno de trabajo. Esta es la VARIABLE en nuestro modelo CSP."""
    def __init__(self, id: str, dia: str, hora_inicio: int, hora_fin: int, departamento: Departamento):
        self.id = id
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.departamento = departamento
        self.empleado_asignado: Optional[Empleado] = None

    def __repr__(self) -> str:
        return (f"Turno('{self.id}', {self.dia}, {self.hora_inicio:02d}:00-{self.hora_fin:02d}:00, "
                f"Dept: {self.departamento.nombre})")
    
    def __eq__(self, other):
        return isinstance(other, Turno) and self.id == other.id

    def __hash__(self):
        return hash(self.id)