from gurobipy import Model, GRB
from datetime import datetime, timedelta


def asignar_turnos(guardias, horarios, dias=None):
    # Generar una semana de fechas si no se pasa un valor para 'dias'
    if dias is None:
        dias = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    
    model = Model("asignacion_turnos")
    x = model.addVars(len(guardias), len(horarios), len(dias), vtype=GRB.BINARY, name="x")

    # Restricción: Cada horario debe ser cubierto por al menos un guardia cada día
    for d in range(len(dias)):
        for j in range(len(horarios)):
            model.addConstr(sum(x[i, j, d] for i in range(len(guardias))) >= 1)

    # Restricción: Un guardia no puede tomar más de un turno en el mismo horario
    for i in range(len(guardias)):
        for d in range(len(dias)):
            model.addConstr(sum(x[i, j, d] for j in range(len(horarios))) <= 1)

    # Optimizar (minimizar horas sin cobertura)
    model.setObjective(
        sum(x[i, j, d] for i in range(len(guardias)) for j in range(len(horarios)) for d in range(len(dias))),
        GRB.MINIMIZE
    )

    model.optimize()

    # Obtener resultados
    asignaciones = []
    if model.status == GRB.OPTIMAL:
        for i in range(len(guardias)):
            for j in range(len(horarios)):
                for d in range(len(dias)):
                    if x[i, j, d].x > 0.5:
                        asignaciones.append((guardias[i], f"{dias[d]} {horarios[j]}"))
    return asignaciones
