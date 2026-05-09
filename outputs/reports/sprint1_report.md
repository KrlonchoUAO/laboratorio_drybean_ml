# Sprint 1 — Informe: Comprensión y Preparación de Datos

**Proyecto:** Clasificación de variedades de frijol seco — Dry Bean Dataset  
**Metodologías:** CRISP-DM + TDSP + Scrum ML  
**Sprint:** 1 de 3  
**Fecha:** Mayo 2026  
**Equipo:** Carlos Garzón | Jhony Posada

---

## 1. Objetivos del Sprint

| ID | Historia de Usuario | Criterio de Aceptación | Estado |
|----|---------------------|------------------------|--------|
| PB-01 | Como analista, quiero cargar datos reales para analizarlos | El dataframe se carga sin errores | ✅ |
| PB-02 | Como científico de datos, quiero revisar la calidad de los datos | Hay resumen de calidad documentado | ✅ |

---

## 2. Daily Scrum — Registro del Sprint

| Integrante | ¿Qué hice? | ¿Qué haré? | ¿Bloqueos? |
|------------|-----------|-----------|-----------|
| Jhony (Data Engineer) | Configuré el entorno virtual y la estructura TDSP | Cargar y explorar el dataset | Ninguno |
| Jhony (Data Analyst) | Cargué el dataset desde UCI (id=602) | Analizar calidad y distribución | Ninguno |
| Carlos (Scrum Master) | Definí el backlog y los criterios de aceptación | Preparar el split train/test | Ninguno |

---

## 3. CRISP-DM Fases Ejecutadas

### Fase 1: Comprensión del Negocio

- **Problema:** Empresa agrícola necesita automatizar la clasificación de frijoles
- **Objetivo del modelo:** Predecir la variedad (`Class`) a partir de 16 features geométricas
- **Criterio de éxito:** F1-macro ≥ 0.90 en datos de prueba
- **Tipo de problema:** Clasificación multiclase (7 clases)

### Fase 2: Comprensión de los Datos

#### Dataset cargado: Dry Bean Dataset (UCI id=602)

| Característica | Valor |
|---------------|-------|
| Total instancias | 13,611 |
| Features | 16 (numéricas) |
| Variable objetivo | `Class` (string) |
| Clases | 7 variedades |
| Valores nulos | **0** (dataset limpio) |
| Filas duplicadas | **68** |

#### Variables del dataset

| Variable | Tipo | Descripción |
|----------|------|-------------|
| Area | float | Área del grano (píxeles) |
| Perimeter | float | Perímetro del grano |
| MajorAxisLength | float | Longitud del eje mayor |
| MinorAxisLength | float | Longitud del eje menor |
| AspectRatio | float | Relación de aspecto |
| Eccentricity | float | Excentricidad de la elipse |
| ConvexArea | float | Área convexa |
| EquivDiameter | float | Diámetro equivalente |
| Extent | float | Extensión del grano |
| Solidity | float | Solidez |
| Roundness | float | Redondez |
| Compactness | float | Compacidad |
| ShapeFactor1–4 | float | Factores de forma (x4) |
| **Class** | string | **Variable objetivo** |

#### Distribución de clases

| Clase | Instancias | % |
|-------|-----------|---|
| DERMASON | ~3,546 | ~26.2% |
| SIRA | ~2,636 | ~19.5% |
| SEKER | ~2,027 | ~15.0% |
| HOROZ | ~1,860 | ~13.7% |
| CALI | ~1,630 | ~12.0% |
| BARBUNYA | ~1,322 | ~9.8% |
| BOMBAY | ~522 | ~3.9% |


---

### Fase 3: Preparación de Datos (parcial)

#### Decisiones técnicas tomadas

1. **Sin imputación de nulos** — el dataset no tiene valores faltantes.
2. **68 filas duplicadas** — se encontraron 68 filas duplicadas y se eliminaron.
3. **Split estratificado 80/20** con `random_state=42`:
   - Train: ~10,834 instancias
   - Test: ~2,709 instancias
   - `stratify=y` preserva proporciones de clases en ambos conjuntos.

#### Justificación del random_state=42 (TDSP)

El uso de `random_state=42` garantiza **reproducibilidad**: cualquier persona que clone el repositorio y ejecute el notebook obtendrá exactamente la misma partición de datos.

---

## 4. Desbalance de Clases — Análisis

**Hallazgo crítico:** BOMBAY representa solo el 3.9% de las instancias vs DERMASON con 26.2%. Esto es **desbalance 7:1** entre la clase minoritaria y la mayoritaria.

**Implicaciones para el modelado:**
- Usar **F1-macro** como métrica principal (no accuracy)
- En Random Forest: `class_weight='balanced'`
- Evaluar recall por clase en la matriz de confusión

---

## 5. Artefactos Generados

| Artefacto | Ruta | Descripción |
|-----------|------|-------------|
| Dataset train | `data/processed/train_set.csv` | 80% estratificado |
| Dataset test | `data/processed/test_set.csv` | 20% estratificado |
| Gráfica clases | `outputs/reports/distribucion_clases.png` | Distribución de 7 clases |

---

## 6. Sprint Review

**¿Qué se entregó?**
- Dataset cargado y validado (sin nulos ni duplicados)
- Análisis exploratorio completo (EDA)
- Split train/test estratificado y guardado
- Identificación del desbalance de clases como riesgo para el modelado

**Aceptación del Product Owner:** ✅ Los entregables del Sprint 1 están completos. El dataset está listo para modelado.

---

## 7. Retrospectiva Sprint 1

| Pregunta | Respuesta |
|----------|-----------|
| ¿Qué salió bien? | La carga automática via `ucimlrepo` fue inmediata. El dataset está muy bien documentado. |
| ¿Qué fue difícil? | Identificar y cuantificar el desbalance de clases y decidir cómo abordarlo. |
| ¿Qué cambiaríamos? | Agregar análisis de correlación entre features para Sprint 1 futuro. |
| ¿Qué aprendizaje técnico obtuvimos? | El `stratify=y` en `train_test_split` es crítico con clases desbalanceadas. |

---

## 8. Backlog Actualizado para Sprint 2

| ID | Historia | Prioridad | Estado |
|----|----------|-----------|--------|
| PB-01 | Descargar dataset | Alta | ✅ Hecho |
| PB-02 | Analizar calidad | Alta | ✅ Hecho |
| PB-03 | Entrenar Logistic Regression | Alta | 🔲 Pendiente |
| PB-04 | Entrenar Random Forest | Media | 🔲 Pendiente |
| PB-05 | Comparar métricas | Alta | 🔲 Pendiente |
| PB-06 | Crear README profesional | Alta | ✅ Hecho |

---

*Sprint 1 completado — Duración estimada: 1 sesión de laboratorio*
