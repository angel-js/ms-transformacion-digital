from gurobipy import Model, GRB

def asignar_turnos(guardias, horarios):

    model = Model("asignacion_turnos")
    x = model.addVars(len(guardias), len(horarios), vtype=GRB.BINARY, name="x")
    # Restricción: Cada horario debe ser cubierto por al menos un guardia
    for j in range(len(horarios)):
        model.addConstr(sum(x[i, j] for i in range(len(guardias))) >= 1)

    # Restricción: Un guardia no puede tomar más de un turno al mismo tiempo
    for i in range(len(guardias)):
        model.addConstr(sum(x[i, j] for j in range(len(horarios))) <= 1)

    # Optimizar (minimizar cantidad de horas sin cobertura)
    model.setObjective(sum(x[i, j] for i in range(len(guardias)) for j in range(len(horarios))), GRB.MINIMIZE)

    model.optimize()

    # Obtener resultados
    asignaciones = []
    if model.status == GRB.OPTIMAL:
        for i in range(len(guardias)):
            for j in range(len(horarios)):
                if x[i, j].x > 0.5:
                    asignaciones.append((guardias[i], horarios[j]))
    return asignaciones