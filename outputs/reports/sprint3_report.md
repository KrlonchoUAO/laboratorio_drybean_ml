# Sprint 3 — Informe: Despliegue y Documentación

**Proyecto:** Clasificación de variedades de frijol seco — Dry Bean Dataset  
**Sprint:** 3 de 3 (Sprint Final)  
**Fecha:** Mayo 2026  
**Responsable:** Carlos Garzón | Jhony Posada

---

## 1. Objetivos del Sprint

| ID | Historia de Usuario | Criterio de Aceptación | Estado |
|----|---------------------|------------------------|--------|
| PB-07 | Como equipo técnico, quiero reproducibilidad | Modelo se puede cargar y usar | ✅ |
| PB-08 | Como equipo, quiero función de predicción | `predict_bean_class` funcional | ✅ |
| PB-09 | Como PM, quiero documentación completa | README + reportes de sprint | ✅ |

---

## 2. CRISP-DM Fase 6 — Despliegue

### 2.1 Modelo guardado con joblib

```python
joblib.dump(forest_model, 'outputs/models/random_forest_drybean.joblib')
```

**Nota sobre selección del modelo:** En la comparación del Sprint 2, Logistic Regression resultó marginalmente ganadora (F1-macro=0.9306 vs RF 0.9302). Sin embargo, se decidió guardar Random Forest por su mayor interpretabilidad mediante importancia de variables y su robustez ante datos no lineales, criterio relevante para producción.

**Verificación de integridad ejecutada:**
```
=== VERIFICACIÓN DE CARGA ===
Predicción: SEKER
Valor real: SEKER
Correcto:   True
```

**¿Por qué joblib y no pickle?**  
joblib está optimizado para objetos NumPy (como los arrays internos de scikit-learn). Es más rápido y genera archivos más pequeños que pickle para modelos de sklearn.

### 2.2 Función de predicción reutilizable

```python
def predict_bean_class(model, input_data):
    """
    Predice la variedad de frijol dadas sus características geométricas.

    Args:
        model:      modelo entrenado cargado con joblib
        input_data: DataFrame con 16 features geométricas
    Returns:
        str: variedad de frijol predicha
    """
    prediction = model.predict(input_data)
    return prediction[0]
```

Demo ejecutado: `predict_bean_class(loaded_model, sample)` → `SEKER` (clase real: SEKER ✅)

Esta función representa la **versión mínima viable de despliegue**: el modelo ya puede recibir datos nuevos y devolver una predicción. En producción, se envolvería en una API REST (FastAPI/Flask) o un endpoint en la nube.

### 2.3 Archivo de predicciones CSV

```
outputs/reports/predicciones_drybean.csv
```

Resultados reales del conjunto de prueba (2,709 muestras con Random Forest):

| Métrica | Valor |
|---------|-------|
| Total muestras | 2,709 |
| Predicciones correctas | 2,490 |
| Predicciones incorrectas | 219 |
| Tasa de error | 8.08% |

Columnas: todas las features + `real_class` + `predicted_class` + `correct`.  
Permite auditoría de los errores del modelo y trazabilidad de las predicciones.

### 2.4 Validación cruzada (Extensión A)

Se ejecutó cross-validation de 5 folds sobre Random Forest con todo el dataset:

```
F1-macro por fold: [0.3511, 0.7570, 0.8944, 0.7501, 0.3872]
Media: 0.6280 ± 0.2178
```

**Análisis:** Los resultados muestran alta varianza entre folds (σ=0.2178), lo que indica que el modelo es sensible a la partición de datos. La diferencia entre el F1 en test (0.9302) y el promedio CV (0.6280) sugiere que la evaluación hold-out puede estar favorecida por la distribución del split específico. Esto refuerza la recomendación de aplicar GridSearchCV con CV en futuros experimentos para una estimación más robusta del rendimiento real.

---

## 3. Tablero Scrum ML — Estado Final

### Backlog completo

| ID | Historia | Responsable | Estado |
|----|----------|-------------|--------|
| PB-01 | Descargar dataset Dry Bean | Data Engineer | ✅ Hecho |
| PB-02 | Analizar calidad de datos | Data Analyst | ✅ Hecho |
| PB-03 | Entrenar Logistic Regression | ML Engineer | ✅ Hecho |
| PB-04 | Entrenar Random Forest | ML Engineer | ✅ Hecho |
| PB-05 | Comparar métricas | Todo el equipo | ✅ Hecho |
| PB-06 | Crear README profesional | Scrum Master | ✅ Hecho |
| PB-07 | Guardar modelo con joblib | ML Engineer | ✅ Hecho |
| PB-08 | Función predict_bean_class | ML Engineer | ✅ Hecho |
| PB-09 | Documentación completa | Scrum Master | ✅ Hecho |

### Tablero Kanban Final

| Por hacer | En progreso | Hecho |
|-----------|-------------|-------|
| — | — | PB-01 ✅ |
| — | — | PB-02 ✅ |
| — | — | PB-03 ✅ |
| — | — | PB-04 ✅ |
| — | — | PB-05 ✅ |
| — | — | PB-06 ✅ |
| — | — | PB-07 ✅ |
| — | — | PB-08 ✅ |
| — | — | PB-09 ✅ |

---

## 4. Definition of Done — Verificación Final

| Criterio DoD | Verificado |
|-------------|-----------|
| El notebook corre de inicio a fin sin errores | ✅ |
| El dataset se descarga o carga correctamente | ✅ |
| Se reportan valores nulos y duplicados | ✅ (0 nulos, 68 duplicados eliminados) |
| Se entrena al menos un modelo baseline | ✅ (Logistic Regression — Acc=91.95%, F1=0.9306) |
| Se entrena un modelo alternativo | ✅ (Random Forest 200 árboles — Acc=91.92%, F1=0.9302) |
| Se comparan modelos con accuracy y F1-macro | ✅ (ambos modelos superan F1≥0.90) |
| Se incluye matriz de confusión | ✅ |
| Se guarda el modelo final | ✅ (random_forest_drybean.joblib) |
| Se explica el resultado en lenguaje comprensible | ✅ |
| Se documenta relación con CRISP-DM, TDSP y Scrum ML | ✅ |

---

## 5. Resumen de Artefactos del Proyecto

### Código

| Archivo | Descripción |
|---------|-------------|
| `notebooks/01_laboratorio_drybean.ipynb` | Notebook principal ejecutable |
| `src/laboratorio_drybean.py` | Script Python modular y reutilizable |

### Datos

| Archivo | Descripción |
|---------|-------------|
| `data/raw/` | Dataset original (descargado via ucimlrepo) |
| `data/processed/train_set.csv` | 10,834 muestras de entrenamiento (80%, estratificado) |
| `data/processed/test_set.csv` | 2,709 muestras de prueba (20%, estratificado) |

### Modelos

| Archivo | Descripción |
|---------|-------------|
| `outputs/models/random_forest_drybean.joblib` | Random Forest serializado (200 árboles, class_weight='balanced') |

### Reportes

| Archivo | Descripción |
|---------|-------------|
| `outputs/reports/sprint1_report.md` | EDA, calidad de datos, split |
| `outputs/reports/sprint2_report.md` | Métricas, comparación, análisis |
| `outputs/reports/sprint3_report.md` | Despliegue, documentación final |
| `outputs/reports/distribucion_clases.png` | Visualización de clases |
| `outputs/reports/matrices_confusion.png` | Matrices de confusión |
| `outputs/reports/feature_importance.png` | Top 10 variables |
| `outputs/reports/predicciones_drybean.csv` | 2,709 predicciones auditables (219 errores) |

---

## 6. Reflexiones Finales del Proyecto

### Preguntas de reflexión del laboratorio

**1. ¿Qué fase de CRISP-DM fue más importante?**  
La **Comprensión de los Datos** (Fase 2). Detectar el desbalance de clases (BOMBAY 3.9% vs DERMASON 26.2%) fue la decisión que determinó toda la estrategia: usar F1-macro como métrica, `class_weight='balanced'` en RF, y el enfoque de análisis por clase en la evaluación.

**2. ¿Qué ventaja ofrece TDSP?**  
Estructura reproducible y versionable. Cualquier persona puede clonar el repo, instalar `requirements.txt` y reproducir exactamente los mismos resultados gracias a `random_state=42`. Sin TDSP, los archivos serían un conjunto de notebooks sin estructura, sin separación de datos procesados, y sin modelo guardado.

**3. ¿Cómo ayuda Scrum ML cuando el resultado es incierto?**  
Permite iterar en sprints cortos y detener cuando se cumple el criterio de éxito. En este proyecto, el baseline (Logistic Regression) ya alcanzó F1=0.9306 > 0.90 en Sprint 2, superando el umbral definido. Scrum ML permitió reconocer ese resultado y destinar el Sprint 3 exclusivamente al despliegue y documentación, evitando modelado adicional innecesario.

**4. ¿Por qué se usa un modelo baseline?**  
Sin baseline, no hay referencia objetiva. El baseline de Logistic Regression con F1=0.9306 estableció que el problema es "relativamente fácil" para modelos lineales bien configurados. Random Forest con F1=0.9302 resultó marginalmente inferior, lo que confirma que la complejidad adicional no siempre agrega valor. La diferencia de 0.0004 en F1 no justifica por sí sola el cambio de modelo en producción.

**5. ¿Qué métrica para el mejor modelo?**  
F1-macro. El negocio necesita clasificar correctamente *todas* las variedades, no solo la más frecuente. Accuracy ignora el rendimiento en clases minoritarias como BOMBAY. Con accuracy ambos modelos marcan ~91.9%, pero F1-macro revela diferencias por clase que accuracy oculta.

**6. ¿Qué hacer si una clase tiene muchos errores?**  
Protocolo sugerido: (1) verificar si hay suficientes datos de esa clase para el modelo; (2) aplicar SMOTE u oversampling; (3) explorar features más discriminativas para esa clase; (4) ajustar el threshold de clasificación para esa clase específica; (5) como último recurso, entrenar un modelo binario especializado (one-vs-rest).

**7. ¿Qué se necesita antes de producción?**  
Validación con datos frescos (data drift check), definición de SLA de latencia (¿cuánto puede tardar una predicción?), monitoreo continuo del F1 en producción, pipeline de reentrenamiento automático, y validación formal del Product Owner con el cliente final (empresa agrícola). Adicionalmente, la alta varianza observada en cross-validation (F1 0.6280 ± 0.2178) exige validación más exhaustiva antes de despliegue real.

---

## 7. Retrospectiva Final del Proyecto

| Pregunta | Respuesta |
|----------|-----------|
| ¿Qué salió bien? | La integración CRISP-DM + TDSP + Scrum ML fue natural. El dataset es limpio y bien documentado. Ambos modelos superaron el criterio de éxito (F1≥0.90) sin hiperparametrización. |
| ¿Qué fue difícil? | Interpretar los errores entre SIRA y DERMASON. El desbalance de clases requirió decisiones conscientes en cada fase. Los resultados inconsistentes de cross-validation generaron incertidumbre sobre la robustez real del modelo. |
| ¿Qué cambiaríamos? | Agregar análisis de correlación en Sprint 1. Incluir GridSearchCV con CV en Sprint 2 para estimación más robusta. Explorar XGBoost como tercera opción. Investigar la causa de la alta varianza en cross-validation. |
| ¿Qué aprendizaje técnico obtuvimos? | La estructura TDSP hace que el código sea profesional desde el inicio. `stratify=y` y `class_weight='balanced'` son no negociables con clases desbalanceadas. F1-macro es la métrica correcta para multiclase desbalanceado. Un modelo más complejo (RF) no siempre supera al baseline. |

---

*Sprint 3 completado — Proyecto Lab 1 finalizado | Mayo 2026*  
*UAO — Maestría en IA y Ciencia de Datos*
