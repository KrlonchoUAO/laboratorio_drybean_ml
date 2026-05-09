# Sprint 3 — Informe: Despliegue y Documentación

**Proyecto:** Clasificación de variedades de frijol seco — Dry Bean Dataset  
**Sprint:** 3 de 3 (Sprint Final)  
**Fecha:** Mayo 2026  
**Responsable:** Carlos García — todos los roles

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

**Verificación de integridad:**
```python
loaded_model = joblib.load('outputs/models/random_forest_drybean.joblib')
prediction = loaded_model.predict(X_test.iloc[[0]])
# → Predicción correcta verificada
```

**¿Por qué joblib y no pickle?**  
joblib está optimizado para objetos NumPy (como los arrays internos de scikit-learn). Es más rápido y genera archivos más pequeños que pickle para modelos de sklearn.

### 2.2 Función de predicción reutilizable

```python
def predict_bean_class(model, input_data):
    """
    Predice variedad de frijol a partir de sus características geométricas.
    
    Args:
        model:      modelo cargado con joblib
        input_data: DataFrame con 16 features geométricas
    Returns:
        str: variedad predicha (ej: 'SIRA', 'DERMASON', 'BOMBAY', ...)
    """
    prediction = model.predict(input_data)
    return prediction[0]
```

Esta función representa la **versión mínima viable de despliegue**: el modelo ya puede recibir datos nuevos y devolver una predicción. En producción, se envolvería en una API REST (FastAPI/Flask) o un endpoint en la nube.

### 2.3 Archivo de predicciones CSV

```
outputs/reports/predicciones_drybean.csv
```

Columnas: todas las features + `real_class` + `predicted_class` + `correct`.  
Permite auditoría de los errores del modelo y trazabilidad de las predicciones.

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
| Se reportan valores nulos y duplicados | ✅ (0 nulos, 0 duplicados) |
| Se entrena al menos un modelo baseline | ✅ (Logistic Regression) |
| Se entrena un modelo alternativo | ✅ (Random Forest) |
| Se comparan modelos con accuracy y F1-macro | ✅ |
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
| `data/processed/train_set.csv` | 80% del dataset (estratificado) |
| `data/processed/test_set.csv` | 20% del dataset (estratificado) |

### Modelos

| Archivo | Descripción |
|---------|-------------|
| `outputs/models/random_forest_drybean.joblib` | Modelo final serializado |

### Reportes

| Archivo | Descripción |
|---------|-------------|
| `outputs/reports/sprint1_report.md` | EDA, calidad de datos, split |
| `outputs/reports/sprint2_report.md` | Métricas, comparación, análisis |
| `outputs/reports/sprint3_report.md` | Despliegue, documentación final |
| `outputs/reports/distribucion_clases.png` | Visualización de clases |
| `outputs/reports/matrices_confusion.png` | Matrices de confusión |
| `outputs/reports/feature_importance.png` | Top 10 variables |
| `outputs/reports/predicciones_drybean.csv` | Predicciones auditables |

---

## 6. Reflexiones Finales del Proyecto

### Preguntas de reflexión del laboratorio

**1. ¿Qué fase de CRISP-DM fue más importante?**  
La **Comprensión de los Datos** (Fase 2). Detectar el desbalance de clases (BOMBAY 3.8% vs DERMASON 26%) fue la decisión que determinó toda la estrategia: usar F1-macro como métrica, `class_weight='balanced'` en RF, y el enfoque de análisis por clase en la evaluación.

**2. ¿Qué ventaja ofrece TDSP?**  
Estructura reproducible y versionable. Cualquier persona puede clonar el repo, instalar `requirements.txt` y reproducir exactamente los mismos resultados gracias a `random_state=42`. Sin TDSP, los archivos serían un conjunto de notebooks sin estructura, sin separación de datos procesados, y sin modelo guardado.

**3. ¿Cómo ayuda Scrum ML cuando el resultado es incierto?**  
Permite iterar en sprints cortos. Si el baseline (Sprint 2) ya hubiera alcanzado F1 ≥ 0.90, el Sprint 3 de modelado complejo no habría sido necesario. Scrum ML evita over-engineering al entregar valor en cada sprint.

**4. ¿Por qué se usa un modelo baseline?**  
Sin baseline, no hay referencia objetiva. Si Random Forest da F1=0.926, no se puede saber si eso es bueno o malo sin compararlo con algo. El baseline de Logistic Regression con ~91.5% establece que el problema es "relativamente fácil" y que RF agrega ~1-2% de mejora real.

**5. ¿Qué métrica para el mejor modelo?**  
F1-macro. El negocio necesita clasificar correctamente *todas* las variedades, no solo la más frecuente. Accuracy ignora el rendimiento en clases minoritarias como BOMBAY.

**6. ¿Qué hacer si una clase tiene muchos errores?**  
Protocolo sugerido: (1) verificar si hay suficientes datos de esa clase para el modelo; (2) aplicar SMOTE u oversampling; (3) explorar features más discriminativas para esa clase; (4) ajustar el threshold de clasificación para esa clase específica; (5) como último recurso, entrenar un modelo binario especializado (one-vs-rest).

**7. ¿Qué se necesita antes de producción?**  
Validación con datos frescos (data drift check), definición de SLA de latencia (¿cuánto puede tardar una predicción?), monitoreo continuo del F1 en producción, pipeline de reentrenamiento automático, y validación formal del Product Owner con el cliente final (empresa agrícola).

---

## 7. Retrospectiva Final del Proyecto

| Pregunta | Respuesta |
|----------|-----------|
| ¿Qué salió bien? | La integración CRISP-DM + TDSP + Scrum ML fue natural. El dataset es limpio y bien documentado. El Random Forest funcionó bien sin tuning extenso. |
| ¿Qué fue difícil? | Interpretar los errores entre SIRA y DERMASON. El desbalance de clases requirió decisiones conscientes en cada fase. |
| ¿Qué cambiaríamos? | Agregar análisis de correlación en Sprint 1. Incluir GridSearchCV en Sprint 2. Explorar XGBoost como tercera opción. Agregar cross-validation en el Sprint 2. |
| ¿Qué aprendizaje técnico obtuvimos? | La estructura TDSP hace que el código sea profesional desde el inicio. `stratify=y` y `class_weight='balanced'` son no negociables con clases desbalanceadas. F1-macro es la métrica correcta para multiclase desbalanceado. |

---

## 8. Próximos Pasos Sugeridos (Extensiones)

| Extensión | Prioridad | Descripción |
|-----------|-----------|-------------|
| GridSearchCV | Media | Optimizar `n_estimators`, `max_depth` en RF |
| XGBoost | Media | Comparar contra RF como tercer modelo |
| API REST | Alta | Envolver `predict_bean_class` en FastAPI |
| Data Drift Monitor | Alta | Detectar cambios en distribución de features en producción |
| SHAP Values | Baja | Explicabilidad a nivel de instancia individual |

---

*Sprint 3 completado — Proyecto Lab 1 finalizado | Mayo 2026*  
*UAO — Maestría en IA y Ciencia de Datos*
