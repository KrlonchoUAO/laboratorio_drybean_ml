# Laboratorio Práctico de Machine Learning — Dry Bean Dataset
**CRISP-DM + TDSP + Scrum ML**  
*UAO — Maestría en IA y Ciencia de Datos*

---

## Equipo Scrum ML

| Rol | Responsable | Responsabilidades |
|-----|-------------|-------------------|
| **Product Owner** | Carlos Garzon | Define el valor del modelo, valida que el clasificador cumpla el objetivo de negocio |
| **Scrum Master** | Carlos Garzon | Coordina sprints, elimina bloqueos, gestiona el tablero |
| **Data Engineer / Analyst** | Jhony Posada | Descarga, limpia y explora el dataset; prepara pipelines de datos |
| **ML Engineer** | Jhony Posada | Entrena, evalúa y compara modelos; guarda artefactos |


---

## Problema de Negocio

Una empresa agrícola desea **automatizar la clasificación de granos de frijol seco** para mejorar el control de calidad. El modelo debe predecir la variedad de frijol (`Class`) a partir de 16 características geométricas extraídas mediante visión por computador.

**Dataset:** [Dry Bean Dataset — UCI ML Repository](https://archive.ics.uci.edu/dataset/602/dry+bean+dataset)  
- 13,611 instancias | 16 features | 7 clases  
- Variables: forma, tamaño y estructura del grano

---

## Metodologías Aplicadas

| Metodología | Rol en el proyecto |
|-------------|-------------------|
| **CRISP-DM** | Marco de ciclo de vida del proyecto (6 fases) |
| **TDSP** | Estructura del repositorio, versionado, reproducibilidad |
| **Scrum ML** | Gestión ágil: backlog, sprints, DoD, retrospectivas |

---

## Estructura del Repositorio (TDSP)

```
laboratorio_drybean_ml/
├── data/
│   ├── raw/          # Dataset original sin modificar
│   └── processed/    # Dataset limpio post-EDA
├── notebooks/
│   └── 01_laboratorio_drybean.ipynb   # Notebook principal
├── outputs/
│   ├── models/       # Modelos serializados (.joblib)
│   └── reports/      # Reportes de sprint en Markdown
├── src/
│   └── laboratorio_drybean.py         # Script Python reutilizable
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Sprints

| Sprint | Objetivo | Estado |
|--------|----------|--------|
| Sprint 1 | Comprensión y preparación de datos | ✅ Completado |
| Sprint 2 | Modelado y evaluación | ✅ Completado |
| Sprint 3 | Despliegue y documentación | ✅ Completado |

---

## Configuración del Entorno

```powershell
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

```powershell
# Abrir notebook
jupyter notebook notebooks/01_laboratorio_drybean.ipynb

# O ejecutar script directamente
python src/laboratorio_drybean.py
```

---

## Definition of Done

- [x] Notebook ejecuta de inicio a fin sin errores
- [x] Dataset descargado y cargado correctamente
- [x] Nulos y duplicados reportados
- [x] Modelo baseline (Logistic Regression) entrenado
- [x] Modelo alternativo (Random Forest) entrenado
- [x] Comparación con accuracy y F1-macro
- [x] Matriz de confusión incluida
- [x] Modelo final guardado con joblib
- [x] Resultados explicados en lenguaje comprensible
- [x] Relación con CRISP-DM, TDSP y Scrum ML documentada

---

## Reportes de Sprint

- [Sprint 1 — Comprensión y Preparación](outputs/reports/sprint1_report.md)
- [Sprint 2 — Modelado y Evaluación](outputs/reports/sprint2_report.md)
- [Sprint 3 — Despliegue y Documentación](outputs/reports/sprint3_report.md)

---

*Creado con CRISP-DM + TDSP + Scrum ML | Mayo 2026*
