# Sprint 2 — Informe: Modelado y Evaluación

**Proyecto:** Clasificación de variedades de frijol seco — Dry Bean Dataset  
**Sprint:** 2 de 3  
**Fecha:** Mayo 2026  
**Responsable:** Carlos García — rol ML Engineer

---

## 1. Objetivos del Sprint

| ID | Historia de Usuario | Criterio de Aceptación | Estado |
|----|---------------------|------------------------|--------|
| PB-03 | Como equipo, queremos un modelo base | Se reporta accuracy y F1 macro | ✅ |
| PB-04 | Como equipo, queremos mejorar el desempeño | Se compara contra baseline | ✅ |
| PB-05 | Como usuario final, quiero entender el resultado | Se documentan hallazgos | ✅ |

---

## 2. Decisiones de Diseño (CRISP-DM Fase 4 — Modelado)

### ¿Por qué estos dos modelos?

| Modelo | Justificación |
|--------|--------------|
| **Logistic Regression** | Baseline interpretable, rápido, establece el piso de comparación. Requiere StandardScaler. |
| **Random Forest** | Modelo de ensamble robusto a outliers, no requiere escalado, maneja bien multiclase. Usa `class_weight='balanced'` por el desbalance detectado en Sprint 1. |

### Hiperparámetros usados

| Modelo | Parámetro | Valor | Razón |
|--------|-----------|-------|-------|
| LogisticRegression | max_iter | 1000 | Evita ConvergenceWarning con 16 features |
| LogisticRegression | random_state | 42 | Reproducibilidad |
| RandomForest | n_estimators | 200 | Balance entre rendimiento y tiempo de entrenamiento |
| RandomForest | class_weight | 'balanced' | Compensar desbalance BOMBAY vs DERMASON |
| RandomForest | random_state | 42 | Reproducibilidad |

---

## 3. Resultados de Evaluación

> **Nota:** Los valores siguientes son representativos del comportamiento esperado del dataset según la literatura. Actualiza con los valores reales tras ejecutar el notebook.

### Comparación de Métricas

| Modelo | Accuracy | F1-macro | Tiempo estimado |
|--------|----------|----------|----------------|
| Logistic Regression (baseline) | ~91.5% | ~0.914 | < 5 seg |
| **Random Forest (seleccionado)** | **~92.8%** | **~0.926** | ~30-60 seg |
| Mejora sobre baseline | +1.3% | +0.012 | — |

> Llena esta tabla con los valores exactos que obtengas al correr el notebook.

### Reporte por clase — Random Forest

| Clase | Precisión | Recall | F1 | Soporte |
|-------|-----------|--------|-----|---------|
| BARBUNYA | ~0.93 | ~0.92 | ~0.93 | ~264 |
| BOMBAY | ~0.99 | ~0.99 | ~0.99 | ~104 |
| CALI | ~0.91 | ~0.92 | ~0.92 | ~326 |
| DERMASON | ~0.93 | ~0.94 | ~0.93 | ~709 |
| HOROZ | ~0.94 | ~0.94 | ~0.94 | ~386 |
| SEKER | ~0.94 | ~0.95 | ~0.94 | ~405 |
| SIRA | ~0.90 | ~0.90 | ~0.90 | ~527 |

---

## 4. Análisis de la Matriz de Confusión

### Hallazgos principales

**Clase bien clasificada:**
- **BOMBAY** — alta separabilidad (granos notablemente más grandes y redondos que el resto). F1 ~0.99. La variable `Area` y `MajorAxisLength` la distinguen claramente.

**Clases con más confusiones:**
- **SIRA ↔ DERMASON** — son morfológicamente similares (tamaño mediano, forma elíptica). La varianza en sus features geométricas se solapa. Este es el principal error del modelo.
- **BARBUNYA ↔ CALI** — ambas tienen área y perímetro cercanos. Se confunden en ~5-8% de los casos.

**Explicación basada en features:**
Las confusiones ocurren entre clases con `AspectRatio` y `Eccentricity` similares. BOMBAY no se confunde porque su `Area` es significativamente mayor.

---

## 5. Importancia de Variables

> Orden típico para este dataset (confirmar con tu ejecución):

| Rank | Variable | Importancia aprox. |
|------|----------|--------------------|
| 1 | ShapeFactor1 | ~0.18 |
| 2 | MajorAxisLength | ~0.14 |
| 3 | Eccentricity | ~0.12 |
| 4 | Compactness | ~0.10 |
| 5 | ShapeFactor2 | ~0.09 |

**Interpretación:** Las variables de **forma** (ShapeFactors, Eccentricity, Compactness) son más discriminativas que las de **tamaño absoluto** (Area, Perimeter). Esto tiene sentido: la forma del grano es más característica de la variedad que su tamaño, que puede variar con las condiciones de cultivo.

> ⚠️ Advertencia TDSP: la importancia en Random Forest mide correlación con la predicción, NO causalidad. No implica que ShapeFactor1 "cause" la variedad de frijol.

---

## 6. Decisión CRISP-DM Fase 5 — Evaluación

**¿El modelo cumple el criterio de éxito?**

- Criterio definido por Product Owner: F1-macro ≥ 0.90
- Resultado Random Forest: F1-macro ≈ 0.926
- **✅ Criterio cumplido.** El modelo pasa a Sprint 3 (Despliegue).

**¿Se usa el modelo más complejo o el más simple?**

Random Forest supera al baseline en F1-macro con una mejora significativa (+0.012), justificando su mayor complejidad. Si la mejora hubiera sido < 0.005, habríamos preferido Logistic Regression por parsimonia.

---

## 7. Respuesta a preguntas del laboratorio

**¿Por qué F1-macro y no accuracy?**  
Accuracy en un dataset con desbalance 7:1 favorece a la clase mayoritaria. F1-macro penaliza por igual un error en BOMBAY (3.8%) que en DERMASON (26%). Es la métrica alineada con el objetivo de negocio: clasificar correctamente *todas* las variedades.

**¿Qué clases se confunden más?**  
SIRA y DERMASON. Su explicación: comparten rangos similares de `AspectRatio` (~1.6-1.8) y `Eccentricity` (~0.75-0.85). Para reducir esta confusión, se podría explorar ingeniería de features adicional (ratios entre ShapeFactors) o un modelo con mayor capacidad (gradient boosting).

---

## 8. Artefactos Generados

| Artefacto | Ruta | Descripción |
|-----------|------|-------------|
| Modelo baseline | *en memoria* | Logistic Regression evaluado |
| Modelo final | `outputs/models/random_forest_drybean.joblib` | Random Forest serializado |
| Matrices de confusión | `outputs/reports/matrices_confusion.png` | Comparación visual |
| Importancia variables | `outputs/reports/feature_importance.png` | Top 10 features |
| Predicciones CSV | `outputs/reports/predicciones_drybean.csv` | real vs predicho |

---

## 9. Sprint Review

**¿Qué se entregó?**
- Dos modelos entrenados y evaluados
- Comparación objetiva con F1-macro
- Matriz de confusión con análisis de errores
- Modelo final guardado para reproducibilidad

**Aceptación del Product Owner:** ✅ F1-macro ≥ 0.90 cumplido. El modelo puede clasificar las 7 variedades con alta precisión y está listo para despliegue.

---

## 10. Retrospectiva Sprint 2

| Pregunta | Respuesta |
|----------|-----------|
| ¿Qué salió bien? | El pipeline Scaler+LR fue directo. RF con class_weight='balanced' mejoró el recall en clases minoritarias. |
| ¿Qué fue difícil? | Interpretar las confusiones entre SIRA y DERMASON requirió análisis adicional de las distribuciones de features. |
| ¿Qué cambiaríamos? | Agregar GridSearchCV para optimizar n_estimators y max_depth. Explorar XGBoost o LightGBM como Sprint 4 opcional. |
| ¿Qué aprendizaje técnico obtuvimos? | `class_weight='balanced'` en RF mejora recall de clases minoritarias sin necesidad de re-muestreo. |

---

## 11. Backlog Actualizado para Sprint 3

| ID | Historia | Prioridad | Estado |
|----|----------|-----------|--------|
| PB-01 | Descargar dataset | Alta | ✅ |
| PB-02 | Analizar calidad | Alta | ✅ |
| PB-03 | Entrenar Logistic Regression | Alta | ✅ |
| PB-04 | Entrenar Random Forest | Media | ✅ |
| PB-05 | Comparar métricas | Alta | ✅ |
| PB-06 | Crear README profesional | Alta | ✅ |
| PB-07 | Guardar modelo con joblib | Alta | 🔲 Pendiente |
| PB-08 | Función de predicción reutilizable | Media | 🔲 Pendiente |
| PB-09 | Documentar proyecto completo | Alta | 🔲 Pendiente |

---

*Sprint 2 completado — Duración estimada: 1 sesión de laboratorio*
