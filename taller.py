
import pulp
 
s = 3
d = 99
 
productos = ['P1', 'P2', 'P3']
materias = ['M1', 'M2']
periodos = [1, 2, 3, 4]
 
alpha = 0.01 + 0.005 * s
precio_base = {'P1': 600000, 'P2': 550000, 'P3': 700000}
precio = {(p, t): precio_base[p] * (1 + alpha) ** (t - 1) for p in productos for t in periodos}
 
capacidad = {t: 180 + ((-1) ** (t - 1)) * d / 100 for t in periodos}
horas_proc = {'P1': 3, 'P2': 4, 'P3': 2}
 
consumo = {
    ('P1', 'M1'): 2, ('P1', 'M2'): 1,
    ('P2', 'M1'): 1, ('P2', 'M2'): 3,
    ('P3', 'M1'): 2, ('P3', 'M2'): 2,
}
 
compra_max = {'M1': 600 - 12 * s, 'M2': 480 + 8 * s}
inv_ini_mp = {'M1': 40, 'M2': 30}
costo_compra = {'M1': 50000, 'M2': 70000}
 
demanda = {
    ('P1', 1): 120, ('P2', 1): 60, ('P3', 1): 72,
    ('P1', 2): 72,  ('P2', 2): 80, ('P3', 2): 60,
    ('P1', 3): 100, ('P2', 3): 130, ('P3', 3): 80,
    ('P1', 4): 60,  ('P2', 4): 62, ('P3', 4): 68,
}
 
inv_ini_pt = {'P1': 20, 'P2': 24, 'P3': 16}
 
costo_alm_pct = s / 100.0
costo_alm_prod = {p: costo_alm_pct * precio_base[p] for p in productos}
costo_alm_mp = {m: costo_alm_pct * costo_compra[m] for m in materias}
 
inv_min_final = 20
lote = {'P1': 5, 'P2': 1, 'P3': 7}
desc_atraso_pct = 0.1 * d / 100.0
 
modelo = pulp.LpProblem("JCR_Planeacion_Produccion", pulp.LpMaximize)
 
Compra = pulp.LpVariable.dicts("Compra", (materias, periodos), lowBound=0)
Lotes = pulp.LpVariable.dicts("Lotes", (productos, periodos), lowBound=0, cat="Integer")
InvMP = pulp.LpVariable.dicts("InvMP", (materias, periodos), lowBound=0)
InvPT = pulp.LpVariable.dicts("InvPT", (productos, periodos), lowBound=0)
VentaTiempo = pulp.LpVariable.dicts("VentaTiempo", (productos, periodos), lowBound=0)
VentaAtrasada = pulp.LpVariable.dicts("VentaAtrasada", (productos, [1, 2, 3]), lowBound=0)
Backlog = pulp.LpVariable.dicts("Backlog", (productos, periodos), lowBound=0)
 
ingresos = pulp.lpSum(
    precio[p, t] * VentaTiempo[p][t] for p in productos for t in periodos
) + pulp.lpSum(
    precio[p, t + 1] * (1 - desc_atraso_pct) * VentaAtrasada[p][t]
    for p in productos for t in [1, 2, 3]
)
 
costos_compra_mp = pulp.lpSum(costo_compra[m] * Compra[m][t] for m in materias for t in periodos)
 
costos_almacenamiento = pulp.lpSum(
    costo_alm_prod[p] * InvPT[p][t] for p in productos for t in periodos
) + pulp.lpSum(
    costo_alm_mp[m] * InvMP[m][t] for m in materias for t in periodos
)
 
modelo += ingresos - costos_compra_mp - costos_almacenamiento, "Utilidad_Total"
 
for t in periodos:
    modelo += (
        pulp.lpSum(horas_proc[p] * lote[p] * Lotes[p][t] for p in productos) <= capacidad[t],
        f"Capacidad_t{t}"
    )
 
    for m in materias:
        modelo += Compra[m][t] <= compra_max[m], f"CompraMax_{m}_t{t}"
 
        entrada_mp = inv_ini_mp[m] if t == 1 else InvMP[m][t - 1]
        consumo_mp = pulp.lpSum(consumo[p, m] * lote[p] * Lotes[p][t] for p in productos)
        modelo += (
            InvMP[m][t] == entrada_mp + Compra[m][t] - consumo_mp,
            f"BalanceMP_{m}_t{t}"
        )
 
    for p in productos:
        entrada_pt = inv_ini_pt[p] if t == 1 else InvPT[p][t - 1]
        produccion_p = lote[p] * Lotes[p][t]
        modelo += (
            InvPT[p][t] == entrada_pt + produccion_p - VentaTiempo[p][t]
            - (VentaAtrasada[p][t - 1] if t > 1 else 0),
            f"BalancePT_{p}_t{t}"
        )
        modelo += VentaTiempo[p][t] + Backlog[p][t] == demanda[p, t], f"Demanda_{p}_t{t}"
 
for p in productos:
    for t in [1, 2, 3]:
        modelo += VentaAtrasada[p][t] <= Backlog[p][t], f"EntregaAtrasada_{p}_t{t}"
    modelo += InvPT[p][4] >= inv_min_final, f"InvMinFinal_{p}"
 
modelo.solve(pulp.PULP_CBC_CMD(msg=0))
 
print("\nEstado de la solucion:", pulp.LpStatus[modelo.status])
 
if pulp.LpStatus[modelo.status] == "Optimal":
    print(f"\nUtilidad total optima: ${pulp.value(modelo.objective):,.2f}")
 
    print("\nPlan de produccion (lotes y unidades):")
    for p in productos:
        for t in periodos:
            lv = Lotes[p][t].varValue
            print(f"  {p} periodo {t}: {lv:.0f} lotes, {lv*lote[p]:.0f} unidades")
 
    print("\nPlan de compra de materias primas:")
    for m in materias:
        for t in periodos:
            print(f"  {m} periodo {t}: {Compra[m][t].varValue:.2f} unidades")
 
    print("\nInventario de producto terminado:")
    for p in productos:
        for t in periodos:
            print(f"  {p} periodo {t}: {InvPT[p][t].varValue:.2f}")
 
    print("\nInventario de materia prima:")
    for m in materias:
        for t in periodos:
            print(f"  {m} periodo {t}: {InvMP[m][t].varValue:.2f}")
 
    print("\nVentas a tiempo y atrasadas:")
    for p in productos:
        for t in periodos:
            va = VentaAtrasada[p][t].varValue if t in [1, 2, 3] else 0
            print(f"  {p} periodo {t}: a tiempo {VentaTiempo[p][t].varValue:.2f}, "
                  f"backlog {Backlog[p][t].varValue:.2f}, atrasada entregada {va if va else 0:.2f}")
else:
    print("No se encontro solucion optima. Revisar factibilidad del modelo.")