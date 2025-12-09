import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib

# Configurações de visualização
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("=" * 70)
print("TREINAMENTO DE MODELO - PREVISÃO DE PREÇOS DE CASAS")
print("=" * 70)

# ====================================================
# 1. CARREGAMENTO E TRATAMENTO DOS DADOS
# ====================================================
print("\n" + "=" * 70)
print("1. CARREGAMENTO E PREPARAÇÃO DOS DADOS")
print("=" * 70)

# Carregar dataset
df = pd.read_csv('./houses.csv')
print(f"✓ Dataset carregado: {df.shape[0]} linhas, {df.shape[1]} colunas")

# Converter colunas yes/no para 1/0
colunas_binarias = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 
                    'airconditioning', 'prefarea']

for col in colunas_binarias:
    df[col] = df[col].map({'yes': 1, 'no': 0})
print(f"✓ Convertidas {len(colunas_binarias)} colunas binárias (yes/no → 1/0)")

# Traduzir e codificar furnishingstatus
traducao_mobilia = {
    'unfurnished': 'vazio',
    'semi-furnished': 'semi-mobiliado',
    'furnished': 'mobiliado'
}
df['furnishingstatus'] = df['furnishingstatus'].map(traducao_mobilia)
print("✓ Coluna 'furnishingstatus' traduzida")

# One-hot encoding para furnishingstatus
df_encoded = pd.get_dummies(df, columns=['furnishingstatus'], drop_first=True)
print(f"✓ One-hot encoding aplicado. Shape final: {df_encoded.shape}")

# Verificar valores nulos
if df_encoded.isnull().sum().sum() > 0:
    print("⚠ Valores nulos encontrados! Preenchendo com mediana...")
    df_encoded.fillna(df_encoded.median(), inplace=True)
else:
    print("✓ Nenhum valor nulo encontrado")

# ====================================================
# 2. SEPARAÇÃO DE FEATURES E TARGET
# ====================================================
print("\n" + "=" * 70)
print("2. SEPARAÇÃO DE FEATURES E VARIÁVEL ALVO")
print("=" * 70)

# Separar features (X) e target (y)
X = df_encoded.drop('price', axis=1)
y = df_encoded['price']

print(f"✓ Features (X): {X.shape}")
print(f"✓ Target (y): {y.shape}")
print(f"\nFeatures utilizadas:")
for i, col in enumerate(X.columns, 1):
    print(f"  {i:2d}. {col}")

# ====================================================
# 3. DIVISÃO TREINO/TESTE
# ====================================================
print("\n" + "=" * 70)
print("3. DIVISÃO DOS DADOS (TREINO/TESTE)")
print("=" * 70)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✓ Conjunto de treino: {X_train.shape[0]} amostras ({(X_train.shape[0]/len(X))*100:.1f}%)")
print(f"✓ Conjunto de teste: {X_test.shape[0]} amostras ({(X_test.shape[0]/len(X))*100:.1f}%)")

# ====================================================
# 4. TREINAMENTO DO MODELO RANDOM FOREST
# ====================================================
print("\n" + "=" * 70)
print("4. TREINAMENTO DO MODELO RANDOM FOREST")
print("=" * 70)

# Criar e treinar modelo
rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

print("Treinando modelo Random Forest...")
rf_model.fit(X_train, y_train)
print("✓ Modelo treinado com sucesso!")

# ====================================================
# 5. AVALIAÇÃO DO MODELO
# ====================================================
print("\n" + "=" * 70)
print("5. AVALIAÇÃO DO MODELO")
print("=" * 70)

# Predições
y_train_pred = rf_model.predict(X_train)
y_test_pred = rf_model.predict(X_test)

# Métricas de treino
train_r2 = r2_score(y_train, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_mae = mean_absolute_error(y_train, y_train_pred)

# Métricas de teste
test_r2 = r2_score(y_test, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_mae = mean_absolute_error(y_test, y_test_pred)

print("\n📊 MÉTRICAS DE PERFORMANCE:")
print("-" * 70)
print(f"{'Métrica':<20} {'Treino':>15} {'Teste':>15}")
print("-" * 70)
print(f"{'R² Score':<20} {train_r2:>15.4f} {test_r2:>15.4f}")
print(f"{'RMSE':<20} {train_rmse:>15.2f} {test_rmse:>15.2f}")
print(f"{'MAE':<20} {train_mae:>15.2f} {test_mae:>15.2f}")
print("-" * 70)

# Interpretação do R²
if test_r2 >= 0.9:
    qualidade = "Excelente"
elif test_r2 >= 0.8:
    qualidade = "Muito Bom"
elif test_r2 >= 0.7:
    qualidade = "Bom"
elif test_r2 >= 0.6:
    qualidade = "Razoável"
else:
    qualidade = "Necessita Melhorias"

print(f"\n✓ Qualidade do Modelo: {qualidade} (R² = {test_r2:.4f})")
print(f"✓ O modelo explica {test_r2*100:.2f}% da variação nos preços")

# ====================================================
# 6. VALIDAÇÃO CRUZADA
# ====================================================
print("\n" + "=" * 70)
print("6. VALIDAÇÃO CRUZADA (5-FOLD)")
print("=" * 70)

cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5, 
                            scoring='r2', n_jobs=-1)

print(f"✓ Scores R² por fold: {cv_scores}")
print(f"✓ Média R²: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

# ====================================================
# 7. IMPORTÂNCIA DAS FEATURES
# ====================================================
print("\n" + "=" * 70)
print("7. IMPORTÂNCIA DAS FEATURES")
print("=" * 70)

# Calcular importância
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n📈 TOP 10 FEATURES MAIS IMPORTANTES:")
print("-" * 70)
for idx, row in feature_importance.head(10).iterrows():
    print(f"{row['feature']:<30} {row['importance']:>10.4f} {'█' * int(row['importance']*100)}")

# Visualizar importância das features
plt.figure(figsize=(10, 6))
top_features = feature_importance.head(10)
plt.barh(top_features['feature'], top_features['importance'])
plt.xlabel('Importância', fontsize=12)
plt.ylabel('Features', fontsize=12)
plt.title('Top 10 Features Mais Importantes', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico de importância salvo como 'feature_importance.png'")

# ====================================================
# 8. VISUALIZAÇÃO DE PREDIÇÕES
# ====================================================
print("\n" + "=" * 70)
print("8. VISUALIZAÇÃO DAS PREDIÇÕES")
print("=" * 70)

# Gráfico: Valores reais vs preditos
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Conjunto de teste
axes[0].scatter(y_test, y_test_pred, alpha=0.6, edgecolors='k', linewidth=0.5)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
             'r--', lw=2, label='Predição Perfeita')
axes[0].set_xlabel('Preço Real', fontsize=12)
axes[0].set_ylabel('Preço Predito', fontsize=12)
axes[0].set_title(f'Conjunto de Teste (R² = {test_r2:.4f})', 
                  fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Distribuição dos erros
residuals = y_test - y_test_pred
axes[1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
axes[1].axvline(x=0, color='r', linestyle='--', linewidth=2)
axes[1].set_xlabel('Erro de Predição (Real - Predito)', fontsize=12)
axes[1].set_ylabel('Frequência', fontsize=12)
axes[1].set_title('Distribuição dos Erros', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('predictions_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico de predições salvo como 'predictions_analysis.png'")

# ====================================================
# 9. EXEMPLO DE PREDIÇÃO
# ====================================================
print("\n" + "=" * 70)
print("9. EXEMPLO DE PREDIÇÃO")
print("=" * 70)

# Pegar primeira amostra do conjunto de teste
exemplo = X_test.iloc[0:1]
preco_real = y_test.iloc[0]
preco_predito = rf_model.predict(exemplo)[0]
erro_percentual = abs(preco_real - preco_predito) / preco_real * 100

print("\n🏠 Características da casa:")
for col in exemplo.columns:
    print(f"  {col:<30} {exemplo[col].values[0]}")

print(f"\n💰 Preço Real: R$ {preco_real:,.2f}")
print(f"💰 Preço Predito: R$ {preco_predito:,.2f}")
print(f"📊 Erro: R$ {abs(preco_real - preco_predito):,.2f} ({erro_percentual:.2f}%)")

# ====================================================
# 10. SALVANDO O MODELO
# ====================================================
print("\n" + "=" * 70)
print("10. SALVANDO O MODELO")
print("=" * 70)

# Salvar modelo
joblib.dump(rf_model, 'random_forest_model.pkl')
print("✓ Modelo salvo como 'random_forest_model.pkl'")

# Salvar informações das features
feature_info = {
    'feature_names': X.columns.tolist(),
    'feature_importance': feature_importance.to_dict('records')
}
joblib.dump(feature_info, 'feature_info.pkl')
print("✓ Informações das features salvas como 'feature_info.pkl'")

# ====================================================
# RESUMO FINAL
# ====================================================
print("\n" + "=" * 70)
print("✅ TREINAMENTO CONCLUÍDO COM SUCESSO!")
print("=" * 70)
print(f"""
📋 RESUMO:
  • Modelo: Random Forest Regressor
  • Amostras de treino: {X_train.shape[0]}
  • Amostras de teste: {X_test.shape[0]}
  • Features utilizadas: {X.shape[1]}
  • R² Score (teste): {test_r2:.4f}
  • RMSE (teste): R$ {test_rmse:,.2f}
  • MAE (teste): R$ {test_mae:,.2f}
  
📁 ARQUIVOS GERADOS:
  • random_forest_model.pkl - Modelo treinado
  • feature_info.pkl - Informações das features
  • feature_importance.png - Gráfico de importância
  • predictions_analysis.png - Análise de predições
""")

print("=" * 70)
