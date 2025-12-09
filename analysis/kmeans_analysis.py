import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import warnings
warnings.filterwarnings('ignore')

# Configurações de visualização
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("=" * 70)
print("ANÁLISE DE CLUSTERING K-MEANS - DATASET HOUSES")
print("=" * 70)

# ====================================================
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS
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

# Codificar furnishingstatus
furnishing_map = {'unfurnished': 0, 'semi-furnished': 1, 'furnished': 2}
df['furnishingstatus_encoded'] = df['furnishingstatus'].map(furnishing_map)

# Selecionar features numéricas para clustering
features_clustering = ['price', 'area', 'bedrooms', 'bathrooms', 'stories', 
                       'mainroad', 'guestroom', 'basement', 'hotwaterheating',
                       'airconditioning', 'parking', 'prefarea', 'furnishingstatus_encoded']

X = df[features_clustering].copy()
print(f"✓ Features selecionadas: {len(features_clustering)}")
print(f"✓ Shape dos dados: {X.shape}")

# ====================================================
# 2. NORMALIZAÇÃO DOS DADOS
# ====================================================
print("\n" + "=" * 70)
print("2. NORMALIZAÇÃO DOS DADOS (STANDARDSCALER)")
print("=" * 70)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("✓ Dados normalizados (média=0, desvio padrão=1)")
print(f"✓ Shape dos dados normalizados: {X_scaled.shape}")

# ====================================================
# 3. MÉTODO DO COTOVELO (ELBOW METHOD)
# ====================================================
print("\n" + "=" * 70)
print("3. DETERMINAÇÃO DO NÚMERO IDEAL DE CLUSTERS")
print("=" * 70)

print("\n📊 Calculando Método do Cotovelo...")
K_range = range(2, 11)
inertias = []
silhouette_scores = []
davies_bouldin_scores = []
calinski_harabasz_scores = []

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
    davies_bouldin_scores.append(davies_bouldin_score(X_scaled, kmeans.labels_))
    calinski_harabasz_scores.append(calinski_harabasz_score(X_scaled, kmeans.labels_))

# Criar figura com múltiplos gráficos
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Gráfico 1: Método do Cotovelo
axes[0, 0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
axes[0, 0].set_xlabel('Número de Clusters (k)', fontsize=12)
axes[0, 0].set_ylabel('Inércia (WCSS)', fontsize=12)
axes[0, 0].set_title('Método do Cotovelo', fontsize=14, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

# Gráfico 2: Silhouette Score
axes[0, 1].plot(K_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
axes[0, 1].set_xlabel('Número de Clusters (k)', fontsize=12)
axes[0, 1].set_ylabel('Silhouette Score', fontsize=12)
axes[0, 1].set_title('Coeficiente de Silhueta (maior é melhor)', fontsize=14, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].axhline(y=0.5, color='r', linestyle='--', label='Threshold 0.5')
axes[0, 1].legend()

# Gráfico 3: Davies-Bouldin Score
axes[1, 0].plot(K_range, davies_bouldin_scores, 'ro-', linewidth=2, markersize=8)
axes[1, 0].set_xlabel('Número de Clusters (k)', fontsize=12)
axes[1, 0].set_ylabel('Davies-Bouldin Score', fontsize=12)
axes[1, 0].set_title('Davies-Bouldin Index (menor é melhor)', fontsize=14, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# Gráfico 4: Calinski-Harabasz Score
axes[1, 1].plot(K_range, calinski_harabasz_scores, 'mo-', linewidth=2, markersize=8)
axes[1, 1].set_xlabel('Número de Clusters (k)', fontsize=12)
axes[1, 1].set_ylabel('Calinski-Harabasz Score', fontsize=12)
axes[1, 1].set_title('Calinski-Harabasz Index (maior é melhor)', fontsize=14, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('kmeans_elbow_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 'kmeans_elbow_analysis.png'")

# Mostrar métricas
print("\n📈 MÉTRICAS POR NÚMERO DE CLUSTERS:")
print("-" * 70)
print(f"{'K':>3} {'Inércia':>15} {'Silhouette':>12} {'Davies-Bouldin':>16} {'Calinski-Harabasz':>18}")
print("-" * 70)
for i, k in enumerate(K_range):
    print(f"{k:>3} {inertias[i]:>15.2f} {silhouette_scores[i]:>12.4f} "
          f"{davies_bouldin_scores[i]:>16.4f} {calinski_harabasz_scores[i]:>18.2f}")

# Determinar k ideal baseado em silhouette score
k_ideal = K_range[silhouette_scores.index(max(silhouette_scores))]
print(f"\n✓ K ideal (baseado em Silhouette Score): {k_ideal}")

# ====================================================
# 4. TREINAMENTO DO MODELO K-MEANS
# ====================================================
print("\n" + "=" * 70)
print(f"4. TREINAMENTO DO MODELO K-MEANS (K={k_ideal})")
print("=" * 70)

kmeans_final = KMeans(n_clusters=k_ideal, random_state=42, n_init=10)
df['cluster'] = kmeans_final.fit_predict(X_scaled)

print(f"✓ Modelo treinado com {k_ideal} clusters")
print(f"✓ Silhouette Score: {silhouette_score(X_scaled, df['cluster']):.4f}")
print(f"✓ Davies-Bouldin Score: {davies_bouldin_score(X_scaled, df['cluster']):.4f}")
print(f"✓ Calinski-Harabasz Score: {calinski_harabasz_score(X_scaled, df['cluster']):.2f}")

# Distribuição dos clusters
print("\n📊 DISTRIBUIÇÃO DOS CLUSTERS:")
print("-" * 70)
cluster_counts = df['cluster'].value_counts().sort_index()
for cluster, count in cluster_counts.items():
    percentage = (count / len(df)) * 100
    print(f"Cluster {cluster}: {count} casas ({percentage:.2f}%)")

# ====================================================
# 5. ANÁLISE DOS CLUSTERS
# ====================================================
print("\n" + "=" * 70)
print("5. CARACTERÍSTICAS DOS CLUSTERS")
print("=" * 70)

# Estatísticas por cluster
cluster_stats = df.groupby('cluster')[['price', 'area', 'bedrooms', 'bathrooms', 
                                        'stories', 'parking']].mean()

print("\n📋 MÉDIAS POR CLUSTER:")
print("-" * 70)
print(cluster_stats.to_string())

# Criar tabela de perfil dos clusters
cluster_profiles = []
for cluster in range(k_ideal):
    cluster_data = df[df['cluster'] == cluster]
    profile = {
        'Cluster': cluster,
        'Tamanho': len(cluster_data),
        '% Total': f"{(len(cluster_data)/len(df)*100):.1f}%",
        'Preço Médio': f"R$ {cluster_data['price'].mean():,.2f}",
        'Área Média': f"{cluster_data['area'].mean():.0f} ft²",
        'Quartos Médio': f"{cluster_data['bedrooms'].mean():.1f}",
        'Banheiros Médio': f"{cluster_data['bathrooms'].mean():.1f}",
        'Ar-Cond. %': f"{(cluster_data['airconditioning'].mean()*100):.0f}%",
        'Garagem Média': f"{cluster_data['parking'].mean():.1f}"
    }
    cluster_profiles.append(profile)

df_profiles = pd.DataFrame(cluster_profiles)
print("\n" + "=" * 70)
print("📊 PERFIL DETALHADO DOS CLUSTERS:")
print("=" * 70)
print(df_profiles.to_string(index=False))

# Salvar perfis em CSV
df_profiles.to_csv('cluster_profiles.csv', index=False, encoding='utf-8-sig')
print("\n✓ Perfis salvos em 'cluster_profiles.csv'")

# ====================================================
# 6. VISUALIZAÇÃO DOS CLUSTERS (PCA)
# ====================================================
print("\n" + "=" * 70)
print("6. VISUALIZAÇÃO DOS CLUSTERS (REDUÇÃO DIMENSIONAL PCA)")
print("=" * 70)

# Aplicar PCA para reduzir a 2 dimensões
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"✓ PCA aplicado: {X_scaled.shape[1]}D → 2D")
print(f"✓ Variância explicada PC1: {pca.explained_variance_ratio_[0]*100:.2f}%")
print(f"✓ Variância explicada PC2: {pca.explained_variance_ratio_[1]*100:.2f}%")
print(f"✓ Variância total explicada: {sum(pca.explained_variance_ratio_)*100:.2f}%")

# Criar visualização
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# Gráfico 1: Scatter plot dos clusters
scatter = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], 
                         c=df['cluster'], 
                         cmap='viridis', 
                         s=50, 
                         alpha=0.6,
                         edgecolors='k',
                         linewidth=0.5)

# Plotar centroides
centroids_pca = pca.transform(kmeans_final.cluster_centers_)
axes[0].scatter(centroids_pca[:, 0], centroids_pca[:, 1], 
               c='red', 
               marker='X', 
               s=300, 
               edgecolors='black',
               linewidth=2,
               label='Centroides')

axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontsize=12)
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontsize=12)
axes[0].set_title('Visualização dos Clusters (PCA)', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
plt.colorbar(scatter, ax=axes[0], label='Cluster')

# Gráfico 2: Boxplot de preços por cluster
df_plot = df[['cluster', 'price']].copy()
df_plot['cluster'] = df_plot['cluster'].astype(str)
sns.boxplot(data=df_plot, x='cluster', y='price', ax=axes[1], palette='viridis')
axes[1].set_xlabel('Cluster', fontsize=12)
axes[1].set_ylabel('Preço (R$)', fontsize=12)
axes[1].set_title('Distribuição de Preços por Cluster', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('kmeans_clusters_visualization.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualização salva: 'kmeans_clusters_visualization.png'")

# ====================================================
# 7. HEATMAP DE CARACTERÍSTICAS DOS CLUSTERS
# ====================================================
print("\n" + "=" * 70)
print("7. HEATMAP DE CARACTERÍSTICAS")
print("=" * 70)

# Normalizar características para o heatmap
cluster_stats_normalized = df.groupby('cluster')[features_clustering].mean()

fig, ax = plt.subplots(figsize=(14, 8))
sns.heatmap(cluster_stats_normalized.T, 
            annot=True, 
            fmt='.2f', 
            cmap='RdYlGn',
            center=0,
            cbar_kws={'label': 'Valor Normalizado'},
            linewidths=0.5,
            ax=ax)

ax.set_xlabel('Cluster', fontsize=12)
ax.set_ylabel('Features', fontsize=12)
ax.set_title('Heatmap de Características Médias por Cluster', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('kmeans_features_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Heatmap salvo: 'kmeans_features_heatmap.png'")

# ====================================================
# 8. INTERPRETAÇÃO DOS CLUSTERS
# ====================================================
print("\n" + "=" * 70)
print("8. INTERPRETAÇÃO DOS CLUSTERS")
print("=" * 70)

# Análise automática de perfis
interpretations = []
for cluster in range(k_ideal):
    cluster_data = df[df['cluster'] == cluster]
    
    avg_price = cluster_data['price'].mean()
    avg_area = cluster_data['area'].mean()
    avg_bedrooms = cluster_data['bedrooms'].mean()
    aircon_pct = cluster_data['airconditioning'].mean() * 100
    
    # Determinar perfil
    if avg_price < df['price'].quantile(0.33):
        price_level = "Econômicas"
    elif avg_price < df['price'].quantile(0.67):
        price_level = "Médias"
    else:
        price_level = "Luxo"
    
    if avg_area < df['area'].quantile(0.33):
        size_level = "Compactas"
    elif avg_area < df['area'].quantile(0.67):
        size_level = "Padrão"
    else:
        size_level = "Espaçosas"
    
    interpretation = {
        'Cluster': cluster,
        'Classificação': f"{price_level} / {size_level}",
        'Descrição': f"Casas {price_level.lower()}, {size_level.lower()}, ~{avg_bedrooms:.0f} quartos",
        'Características': f"Ar-cond: {aircon_pct:.0f}%, Área: {avg_area:.0f}ft²"
    }
    interpretations.append(interpretation)

df_interpretations = pd.DataFrame(interpretations)
print("\n🏠 PERFIL E INTERPRETAÇÃO:")
print("-" * 70)
print(df_interpretations.to_string(index=False))

# ====================================================
# 9. SALVAR DATASET COM CLUSTERS
# ====================================================
print("\n" + "=" * 70)
print("9. SALVANDO RESULTADOS")
print("=" * 70)

df_output = df.copy()
df_output.to_csv('houses_with_clusters.csv', index=False, encoding='utf-8-sig')
print("✓ Dataset com clusters salvo: 'houses_with_clusters.csv'")

# Salvar interpretações
df_interpretations.to_csv('cluster_interpretations.csv', index=False, encoding='utf-8-sig')
print("✓ Interpretações salvas: 'cluster_interpretations.csv'")

# ====================================================
# RESUMO FINAL
# ====================================================
print("\n" + "=" * 70)
print("✅ ANÁLISE K-MEANS CONCLUÍDA!")
print("=" * 70)

print(f"""
📊 RESUMO:
  • Número de clusters: {k_ideal}
  • Silhouette Score: {silhouette_score(X_scaled, df['cluster']):.4f}
  • Total de casas analisadas: {len(df)}
  • Features utilizadas: {len(features_clustering)}
  
📁 ARQUIVOS GERADOS:
  • kmeans_elbow_analysis.png - Análise do método do cotovelo
  • kmeans_clusters_visualization.png - Visualização dos clusters
  • kmeans_features_heatmap.png - Heatmap de características
  • houses_with_clusters.csv - Dataset com labels de clusters
  • cluster_profiles.csv - Perfis detalhados dos clusters
  • cluster_interpretations.csv - Interpretação dos clusters

💡 APLICAÇÕES:
  • Segmentação de mercado imobiliário
  • Estratificação de preços
  • Análise de perfis de compradores
  • Recomendação de imóveis similares
""")

print("=" * 70)
