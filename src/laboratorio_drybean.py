"""
laboratorio_drybean.py
======================
Script Python reutilizable — Clasificación de variedades de frijol seco
Dry Bean Dataset | UCI ML Repository | id=602

Metodologías: CRISP-DM + TDSP + Scrum ML
Autor: Carlos Garzón | Jhony Posada (UAO — Maestría IA y CD)
Fecha: Mayo 2026

Uso:
    python src/laboratorio_drybean.py
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from ucimlrepo import fetch_ucirepo

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, classification_report,
    ConfusionMatrixDisplay
)
import joblib

# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────
RANDOM_STATE = 42   # Semilla de reproducibilidad (TDSP best practice)
TEST_SIZE    = 0.20 # 80/20 split
N_ESTIMATORS = 200  # Árboles en Random Forest

# Rutas (relativas al root del proyecto)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED = os.path.join(ROOT, 'data', 'processed')
MODELS_DIR     = os.path.join(ROOT, 'outputs', 'models')
REPORTS_DIR    = os.path.join(ROOT, 'outputs', 'reports')

for d in [DATA_PROCESSED, MODELS_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# FASE 1 & 2 CRISP-DM: Comprensión negocio + datos
# ─────────────────────────────────────────────────────────────
def load_dataset():
    """Carga el Dry Bean Dataset desde UCI ML Repository."""
    print("[1/7] Cargando dataset desde UCI (id=602)...")
    dry_bean = fetch_ucirepo(id=602)
    X = dry_bean.data.features
    y = dry_bean.data.targets
    df = pd.concat([X, y], axis=1)
    print(f"      ✅ Dataset cargado: {df.shape[0]:,} filas × {df.shape[1]} columnas")
    return df, X, y


def quality_report(df):
    """Genera reporte de calidad de datos (CRISP-DM Fase 2)."""
    print("\n[2/7] Análisis de calidad de datos...")
    print(f"      Nulos:        {df.isna().sum().sum()}")
    print(f"      Duplicados:   {df.duplicated().sum()}")
    print(f"      Clases únicas: {df['Class'].nunique()}")
    print(f"\n      Distribución de clases:")
    print(df['Class'].value_counts().to_string())
    return df.drop_duplicates()


def plot_class_distribution(df):
    """Gráfica de distribución de clases."""
    counts = df['Class'].value_counts()
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ['#c0392b', '#e67e22', '#f1c40f', '#27ae60',
              '#2980b9', '#8e44ad', '#2c3e50']
    counts.plot(kind='bar', ax=ax, color=colors, edgecolor='white')
    ax.set_title('Distribución de clases — Dry Bean Dataset', fontweight='bold')
    ax.set_xlabel('Variedad')
    ax.set_ylabel('Cantidad')
    plt.xticks(rotation=45)
    plt.tight_layout()
    out = os.path.join(REPORTS_DIR, 'distribucion_clases.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"      📊 Gráfica guardada: {out}")


# ─────────────────────────────────────────────────────────────
# FASE 3 CRISP-DM: Preparación de datos
# ─────────────────────────────────────────────────────────────
def prepare_data(df):
    """Split estratificado train/test."""
    print("\n[3/7] Preparando datos (split 80/20 estratificado)...")
    X = df.drop(columns='Class')
    y = df['Class']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )
    print(f"      Train: {X_train.shape[0]:,} | Test: {X_test.shape[0]:,}")

    # Guardar datos procesados (TDSP: versionado de datos)
    X_train.join(y_train).to_csv(os.path.join(DATA_PROCESSED, 'train_set.csv'), index=False)
    X_test.join(y_test).to_csv(os.path.join(DATA_PROCESSED, 'test_set.csv'), index=False)
    print("      💾 Datos guardados en data/processed/")
    return X_train, X_test, y_train, y_test


# ─────────────────────────────────────────────────────────────
# FASE 4 CRISP-DM: Modelado
# ─────────────────────────────────────────────────────────────
def train_baseline(X_train, y_train):
    """Logistic Regression como modelo baseline."""
    print("\n[4/7] Entrenando modelo baseline (Logistic Regression)...")
    model = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))
    ])
    model.fit(X_train, y_train)
    print("      ✅ Baseline entrenado")
    return model


def train_improved(X_train, y_train):
    """Random Forest como modelo mejorado."""
    print("\n[5/7] Entrenando modelo mejorado (Random Forest)...")
    model = RandomForestClassifier(
        n_estimators=N_ESTIMATORS,
        random_state=RANDOM_STATE,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)
    print(f"      ✅ Random Forest entrenado ({N_ESTIMATORS} árboles)")
    return model


# ─────────────────────────────────────────────────────────────
# FASE 5 CRISP-DM: Evaluación
# ─────────────────────────────────────────────────────────────
def evaluate_models(baseline, forest, X_test, y_test):
    """Evalúa ambos modelos y genera comparación."""
    print("\n[6/7] Evaluando modelos...")

    y_pred_base   = baseline.predict(X_test)
    y_pred_forest = forest.predict(X_test)

    acc_base   = accuracy_score(y_test, y_pred_base)
    f1_base    = f1_score(y_test, y_pred_base, average='macro')
    acc_forest = accuracy_score(y_test, y_pred_forest)
    f1_forest  = f1_score(y_test, y_pred_forest, average='macro')

    print(f"\n      Logistic Regression → Accuracy: {acc_base:.4f} | F1-macro: {f1_base:.4f}")
    print(f"      Random Forest       → Accuracy: {acc_forest:.4f} | F1-macro: {f1_forest:.4f}")

    mejor = 'Random Forest' if f1_forest >= f1_base else 'Logistic Regression'
    print(f"\n      🏆 Modelo seleccionado: {mejor}")
    print(f"\n{classification_report(y_test, y_pred_forest)}")

    # Matrices de confusión
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred_base,
        xticks_rotation=45, ax=axes[0], colorbar=False)
    axes[0].set_title(f'Logistic Regression\nAcc={acc_base:.3f} | F1={f1_base:.3f}',
                      fontweight='bold')
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred_forest,
        xticks_rotation=45, ax=axes[1], colorbar=False)
    axes[1].set_title(f'Random Forest\nAcc={acc_forest:.3f} | F1={f1_forest:.3f}',
                      fontweight='bold')
    plt.suptitle('Matrices de Confusión', fontsize=13)
    plt.tight_layout()
    out_cm = os.path.join(REPORTS_DIR, 'matrices_confusion.png')
    plt.savefig(out_cm, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"      📊 Matriz guardada: {out_cm}")

    # Importancia de variables
    fi = pd.DataFrame({
        'feature':    X_test.columns,
        'importance': forest.feature_importances_
    }).sort_values('importance', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    top10 = fi.head(10)
    ax.bar(range(10), top10['importance'], color='#2980b9', edgecolor='white')
    ax.set_xticks(range(10))
    ax.set_xticklabels(top10['feature'], rotation=45, ha='right')
    ax.set_title('Top 10 variables más importantes — Random Forest', fontweight='bold')
    plt.tight_layout()
    out_fi = os.path.join(REPORTS_DIR, 'feature_importance.png')
    plt.savefig(out_fi, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"      📊 Feature importance guardado: {out_fi}")

    # Predicciones CSV
    pred_df = X_test.copy()
    pred_df['real_class']      = y_test.values
    pred_df['predicted_class'] = y_pred_forest
    pred_df['correct']         = pred_df['real_class'] == pred_df['predicted_class']
    out_csv = os.path.join(REPORTS_DIR, 'predicciones_drybean.csv')
    pred_df.to_csv(out_csv, index=False)
    print(f"      💾 Predicciones guardadas: {out_csv}")

    return y_pred_forest, acc_base, f1_base, acc_forest, f1_forest


# ─────────────────────────────────────────────────────────────
# FASE 6 CRISP-DM: Despliegue
# ─────────────────────────────────────────────────────────────
def save_model(model):
    """Guarda el modelo final para uso en producción (TDSP)."""
    path = os.path.join(MODELS_DIR, 'random_forest_drybean.joblib')
    joblib.dump(model, path)
    print(f"\n[7/7] Modelo guardado: {path}")
    return path


def predict_bean_class(model, input_data):
    """
    Función de despliegue: predice variedad de frijol.

    Args:
        model: modelo cargado con joblib
        input_data: DataFrame con 16 features geométricas
    Returns:
        str: variedad predicha
    """
    return model.predict(input_data)[0]


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("  LAB ML — Dry Bean Dataset | CRISP-DM + TDSP + Scrum ML")
    print("=" * 60)

    # Sprint 1
    df, X_raw, y_raw = load_dataset()
    df = quality_report(df)
    plot_class_distribution(df)
    X_train, X_test, y_train, y_test = prepare_data(df)

    # Sprint 2
    baseline = train_baseline(X_train, y_train)
    forest   = train_improved(X_train, y_train)
    y_pred, acc_b, f1_b, acc_f, f1_f = evaluate_models(
        baseline, forest, X_test, y_test
    )

    # Sprint 3
    model_path = save_model(forest)

    # Demo de predicción
    loaded = joblib.load(model_path)
    sample = X_test.iloc[[0]]
    pred   = predict_bean_class(loaded, sample)
    real   = y_test.iloc[0]
    print(f"\n🫘 Demo predicción:")
    print(f"   Predicción: {pred} | Real: {real} | Correcto: {pred == real}")

    print("\n" + "=" * 60)
    print("  ✅ DEFINITION OF DONE COMPLETADA")
    print(f"  Logistic Regression: Acc={acc_b:.4f} | F1={f1_b:.4f}")
    print(f"  Random Forest:       Acc={acc_f:.4f} | F1={f1_f:.4f}")
    print("=" * 60)
