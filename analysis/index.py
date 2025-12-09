import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Configurações de visualização
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ====================================================
# 1. CARREGAMENTO DOS DADOS
# ====================================================
print("=" * 70)
print("CARREGANDO DATASET: houses.csv")
print("=" * 70)

df = pd.read_csv('./houses.csv')
print("✓ Dataset carregado com sucesso!")

# ====================================================
# TRANSFORMAÇÕES DOS DADOS
# ====================================================
print("\n" + "=" * 70)
print("APLICANDO TRANSFORMAÇÕES NOS DADOS")
print("=" * 70)

# Converter colunas yes/no para 1/0
colunas_binarias = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 
                    'airconditioning', 'prefarea']

for col in colunas_binarias:
    df[col] = df[col].map({'yes': 1, 'no': 0})
    print(f"✓ Coluna '{col}' convertida: yes → 1, no → 0")

# Traduzir coluna furnishingstatus
traducao_mobilia = {
    'unfurnished': 'vazio',
    'semi-furnished': 'semi-mobiliado',
    'furnished': 'mobiliado'
}
df['furnishingstatus'] = df['furnishingstatus'].map(traducao_mobilia)
print(f"✓ Coluna 'furnishingstatus' traduzida")
print(f"  - unfurnished → vazio")
print(f"  - semi-furnished → semi-mobiliado")
print(f"  - furnished → mobiliado")

print("\n✓ Todas as transformações aplicadas com sucesso!")

# ====================================================
# 2. INFORMAÇÕES GERAIS DO DATASET
# ====================================================
print("\n" + "=" * 70)
print("INFORMAÇÕES GERAIS")
print("=" * 70)
print(f"Shape do dataset: {df.shape}")
print(f"Total de linhas: {len(df)}")
print(f"Total de colunas: {len(df.columns)}")
print(f"Memória utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# ====================================================
# 3. CABEÇALHOS E TIPOS DE DADOS
# ====================================================
print("\n" + "=" * 70)
print("CABEÇALHOS DO DATASET")
print("=" * 70)
for i, col in enumerate(df.columns, 1):
    tipo = df[col].dtype
    print(f"{i:2d}. {col:25s} - Tipo: {tipo}")

# ====================================================
# 4. ANÁLISE DE VALORES NULOS
# ====================================================
print("\n" + "=" * 70)
print("ANÁLISE DE VALORES NULOS")
print("=" * 70)
valores_nulos = df.isnull().sum()
percentual_nulos = (df.isnull().sum() / len(df)) * 100

print(f"{'Coluna':<25} {'Nulos':>10} {'Percentual':>12}")
print("-" * 70)
for col in df.columns:
    nulos = valores_nulos[col]
    perc = percentual_nulos[col]
    if nulos > 0:
        print(f"{col:<25} {nulos:>10} {perc:>11.2f}%")

if valores_nulos.sum() == 0:
    print("✓ Nenhum valor nulo encontrado no dataset!")

# ====================================================
# 5. ESTATÍSTICAS DESCRITIVAS
# ====================================================
print("\n" + "=" * 70)
print("ESTATÍSTICAS DESCRITIVAS (VARIÁVEIS NUMÉRICAS)")
print("=" * 70)
print(df.describe())

# ====================================================
# 6. PRIMEIRAS E ÚLTIMAS LINHAS
# ====================================================
print("\n" + "=" * 70)
print("PRIMEIRAS 5 LINHAS DO DATASET")
print("=" * 70)
print(df.head())

print("\n" + "=" * 70)
print("ÚLTIMAS 5 LINHAS DO DATASET")
print("=" * 70)
print(df.tail())

# ====================================================
# 7. INFORMAÇÕES DETALHADAS
# ====================================================
print("\n" + "=" * 70)
print("INFORMAÇÕES DETALHADAS DAS COLUNAS")
print("=" * 70)
df.info()

# ====================================================
# 8. ANÁLISE DE VALORES ÚNICOS (VARIÁVEIS CATEGÓRICAS)
# ====================================================
print("\n" + "=" * 70)
print("ANÁLISE DE VALORES ÚNICOS (VARIÁVEIS CATEGÓRICAS)")
print("=" * 70)
colunas_categoricas = df.select_dtypes(include=['object']).columns
for col in colunas_categoricas:
    print(f"\n{col}:")
    print(f"  Valores únicos: {df[col].nunique()}")
    print(f"  Valores: {df[col].unique()}")

# ====================================================
# 9. MAPA DE CORRELAÇÃO
# ====================================================
print("\n" + "=" * 70)
print("GERANDO MAPA DE CORRELAÇÃO")
print("=" * 70)

# Selecionar apenas colunas numéricas
df_numeric = df.select_dtypes(include=[np.number])

if len(df_numeric.columns) > 1:
    # Calcular matriz de correlação
    correlation_matrix = df_numeric.corr()
    
    # Criar figura
    plt.figure(figsize=(12, 10))
    
    # Criar heatmap
    sns.heatmap(correlation_matrix, 
                annot=True, 
                fmt='.2f', 
                cmap='coolwarm', 
                center=0,
                square=True,
                linewidths=1,
                cbar_kws={"shrink": 0.8})
    
    plt.title('Mapa de Correlação entre Variáveis Numéricas', 
              fontsize=16, 
              fontweight='bold',
              pad=20)
    plt.tight_layout()
    
    # Salvar figura
    plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Mapa de correlação salvo como 'correlation_heatmap.png'")
    
    # Exibir correlações mais fortes (exceto diagonal)
    print("\n" + "-" * 70)
    print("CORRELAÇÕES MAIS FORTES (> 0.5 ou < -0.5)")
    print("-" * 70)
    
    # Encontrar correlações fortes
    strong_corr = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            if abs(correlation_matrix.iloc[i, j]) > 0.5:
                strong_corr.append({
                    'Variável 1': correlation_matrix.columns[i],
                    'Variável 2': correlation_matrix.columns[j],
                    'Correlação': correlation_matrix.iloc[i, j]
                })
    
    if strong_corr:
        df_strong_corr = pd.DataFrame(strong_corr)
        df_strong_corr = df_strong_corr.sort_values('Correlação', 
                                                      key=abs, 
                                                      ascending=False)
        print(df_strong_corr.to_string(index=False))
    else:
        print("Nenhuma correlação forte encontrada (|r| > 0.5)")
    
    plt.show()
else:
    print("⚠ Não há colunas numéricas suficientes para gerar mapa de correlação")

# ====================================================
# 10. TABELA DE SUMARIZAÇÃO DOS DADOS
# ====================================================
print("\n" + "=" * 70)
print("TABELA DE SUMARIZAÇÃO DOS DADOS")
print("=" * 70)

# Criar DataFrame de sumarização
sumarizacao = []

for col in df.columns:
    info_col = {
        'Coluna': col,
        'Tipo': str(df[col].dtype),
        'Não-Nulos': df[col].count(),
        'Nulos': df[col].isnull().sum(),
        '% Nulos': f"{(df[col].isnull().sum() / len(df)) * 100:.2f}%",
        'Únicos': df[col].nunique(),
    }
    
    # Adicionar estatísticas para colunas numéricas
    if df[col].dtype in ['int64', 'float64']:
        valores = df[col].dropna()
        
        # Métricas solicitadas
        info_col['Média'] = f"{valores.mean():.2f}"
        info_col['Mediana'] = f"{valores.median():.2f}"
        
        # Moda (pode ter múltiplos valores)
        moda = valores.mode()
        info_col['Moda'] = f"{moda.iloc[0]:.2f}" if len(moda) > 0 else 'N/A'
        
        info_col['Desvio Padrão'] = f"{valores.std():.2f}"
        info_col['Variância'] = f"{valores.var():.2f}"
        info_col['Erro Padrão'] = f"{valores.sem():.2f}"
        info_col['Mínimo'] = f"{valores.min():.2f}" if df[col].dtype == 'float64' else valores.min()
        info_col['Máximo'] = f"{valores.max():.2f}" if df[col].dtype == 'float64' else valores.max()
        info_col['Amplitude'] = f"{valores.max() - valores.min():.2f}" if df[col].dtype == 'float64' else valores.max() - valores.min()
        
        # Quartis adicionais
        info_col['Q1 (25%)'] = f"{valores.quantile(0.25):.2f}"
        info_col['Q3 (75%)'] = f"{valores.quantile(0.75):.2f}"
        info_col['IQR'] = f"{valores.quantile(0.75) - valores.quantile(0.25):.2f}"
        
    else:
        # Para colunas categóricas, mostrar valores mais frequentes
        top_value = df[col].mode()[0] if len(df[col].mode()) > 0 else 'N/A'
        info_col['Moda'] = top_value
        info_col['Frequência Moda'] = df[col].value_counts().iloc[0] if len(df[col].value_counts()) > 0 else 0
        info_col['% Moda'] = f"{(df[col].value_counts().iloc[0] / len(df) * 100):.2f}%" if len(df[col].value_counts()) > 0 else "0%"
    
    sumarizacao.append(info_col)

# Criar DataFrame de sumarização
df_sumarizacao = pd.DataFrame(sumarizacao)

# Exibir tabela completa
print("\n📊 RESUMO COMPLETO DAS COLUNAS:")
print("=" * 70)
print(df_sumarizacao.to_string(index=False))

# Sumarização por tipo de dado
print("\n" + "=" * 70)
print("📈 SUMARIZAÇÃO POR TIPO DE DADO")
print("=" * 70)

tipos_dados = df.dtypes.value_counts()
print("\nDistribuição dos Tipos de Dados:")
for tipo, count in tipos_dados.items():
    print(f"  • {tipo}: {count} colunas ({(count/len(df.columns)*100):.1f}%)")

# Estatísticas gerais do dataset
print("\n" + "=" * 70)
print("📋 ESTATÍSTICAS GERAIS DO DATASET")
print("=" * 70)
print(f"  • Total de Registros: {len(df):,}")
print(f"  • Total de Colunas: {len(df.columns)}")
print(f"  • Colunas Numéricas: {len(df.select_dtypes(include=[np.number]).columns)}")
print(f"  • Colunas Categóricas: {len(df.select_dtypes(include=['object']).columns)}")
print(f"  • Total de Valores: {df.size:,}")
print(f"  • Total de Valores Nulos: {df.isnull().sum().sum()}")
print(f"  • Percentual de Completude: {((df.size - df.isnull().sum().sum()) / df.size * 100):.2f}%")
print(f"  • Memória Utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Tabela detalhada de métricas estatísticas
print("\n" + "=" * 70)
print("📊 MÉTRICAS ESTATÍSTICAS DETALHADAS - VARIÁVEIS NUMÉRICAS")
print("=" * 70)

metricas_numericas = []
for col in df.select_dtypes(include=[np.number]).columns:
    valores = df[col].dropna()
    metricas_numericas.append({
        'Variável': col,
        'Média': f"{valores.mean():.2f}",
        'Mediana': f"{valores.median():.2f}",
        'Moda': f"{valores.mode().iloc[0]:.2f}" if len(valores.mode()) > 0 else 'N/A',
        'Desvio Padrão': f"{valores.std():.2f}",
        'Variância': f"{valores.var():.2f}",
        'Erro Padrão': f"{valores.sem():.2f}",
        'Mínimo': valores.min(),
        'Máximo': valores.max(),
        'Amplitude': valores.max() - valores.min()
    })

df_metricas = pd.DataFrame(metricas_numericas)
print(df_metricas.to_string(index=False))

# Salvar sumarização em CSV
df_sumarizacao.to_csv('sumarizacao_dados.csv', index=False, encoding='utf-8-sig')
df_metricas.to_csv('metricas_estatisticas.csv', index=False, encoding='utf-8-sig')
print(f"\n✓ Tabela de sumarização salva como 'sumarizacao_dados.csv'")
print(f"✓ Métricas estatísticas salvas como 'metricas_estatisticas.csv'")

# Gerar tabela de sumarização como imagem
print("\n" + "=" * 70)
print("GERANDO IMAGENS DAS TABELAS DE SUMARIZAÇÃO")
print("=" * 70)

# ====================================================
# IMAGEM 1: Tabela de Métricas Estatísticas Principais
# ====================================================
fig1, ax1 = plt.subplots(figsize=(18, 10))
ax1.axis('tight')
ax1.axis('off')

# Preparar dados da tabela principal de métricas
tabela_metricas = []
colunas_metricas = ['Variável', 'Média', 'Mediana', 'Moda', 'Desv. Padrão', 
                    'Variância', 'Erro Padrão', 'Mín', 'Máx', 'Amplitude']

for _, row in df_metricas.iterrows():
    tabela_metricas.append([
        row['Variável'],
        row['Média'],
        row['Mediana'],
        row['Moda'],
        row['Desvio Padrão'],
        row['Variância'],
        row['Erro Padrão'],
        str(row['Mínimo']),
        str(row['Máximo']),
        str(row['Amplitude'])
    ])

table_data1 = [colunas_metricas] + tabela_metricas

table1 = ax1.table(cellText=table_data1,
                  cellLoc='center',
                  loc='center',
                  colWidths=[0.12] * len(colunas_metricas))

table1.auto_set_font_size(False)
table1.set_fontsize(8)
table1.scale(1, 2.2)

# Estilizar cabeçalho
for i in range(len(colunas_metricas)):
    cell = table1[(0, i)]
    cell.set_facecolor('#2E75B6')
    cell.set_text_props(weight='bold', color='white', size=9)

# Alternar cores das linhas
for i in range(1, len(table_data1)):
    for j in range(len(colunas_metricas)):
        cell = table1[(i, j)]
        if i % 2 == 0:
            cell.set_facecolor('#DEEAF6')
        else:
            cell.set_facecolor('#F2F7FC')

plt.suptitle('Métricas Estatísticas Completas - Variáveis Numéricas', 
             fontsize=18, 
             fontweight='bold',
             y=0.98)

info_text1 = f"Dataset: houses.csv | Total: {len(df)} registros | Variáveis Numéricas: {len(df_metricas)}"
plt.figtext(0.5, 0.02, info_text1, 
           ha='center', 
           fontsize=10,
           style='italic',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

plt.tight_layout()
plt.savefig('tabela_metricas_estatisticas.png', dpi=300, bbox_inches='tight')
print("✓ Imagem 1 salva: 'tabela_metricas_estatisticas.png'")
plt.close()

# ====================================================
# IMAGEM 2: Tabela Resumida (Overview)
# ====================================================
fig2, ax2 = plt.subplots(figsize=(16, 12))
ax2.axis('tight')
ax2.axis('off')

# Preparar dados resumidos com informações principais
tabela_resumo = []
colunas_resumo = ['Coluna', 'Tipo', 'Não-Nulos', 'Únicos', 'Média', 'Mediana', 
                  'Desv. Padrão', 'Mín', 'Máx']

for _, row in df_sumarizacao.iterrows():
    linha = [row['Coluna'], row['Tipo'], str(row['Não-Nulos']), str(row['Únicos'])]
    
    if 'Média' in row and pd.notna(row['Média']):
        linha.extend([
            row['Média'],
            row['Mediana'],
            row['Desvio Padrão'],
            str(row['Mínimo']),
            str(row['Máximo'])
        ])
    else:
        linha.extend(['-', '-', '-', '-', '-'])
    
    tabela_resumo.append(linha)

table_data2 = [colunas_resumo] + tabela_resumo

table2 = ax2.table(cellText=table_data2,
                  cellLoc='center',
                  loc='center',
                  colWidths=[0.14, 0.09, 0.09, 0.08, 0.11, 0.11, 0.13, 0.11, 0.11])

table2.auto_set_font_size(False)
table2.set_fontsize(8)
table2.scale(1, 2)

# Estilizar cabeçalho
for i in range(len(colunas_resumo)):
    cell = table2[(0, i)]
    cell.set_facecolor('#70AD47')
    cell.set_text_props(weight='bold', color='white', size=9)

# Alternar cores das linhas
for i in range(1, len(table_data2)):
    for j in range(len(colunas_resumo)):
        cell = table2[(i, j)]
        if i % 2 == 0:
            cell.set_facecolor('#E2EFDA')
        else:
            cell.set_facecolor('#F0F7EC')

plt.suptitle('Tabela de Sumarização Geral do Dataset', 
             fontsize=18, 
             fontweight='bold',
             y=0.98)

info_text2 = f"Completude: 100% | Memória: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB | {len(df.columns)} colunas"
plt.figtext(0.5, 0.02, info_text2, 
           ha='center', 
           fontsize=10,
           style='italic',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

plt.tight_layout()
plt.savefig('tabela_sumarizacao_geral.png', dpi=300, bbox_inches='tight')
print("✓ Imagem 2 salva: 'tabela_sumarizacao_geral.png'")
plt.close()

# ====================================================
# IMAGEM 3: Tabela de Definições das Métricas
# ====================================================
fig3, ax3 = plt.subplots(figsize=(14, 10))
ax3.axis('tight')
ax3.axis('off')

definicoes = [
    ['Métrica', 'Definição', 'Interpretação'],
    ['Média', 'Soma dos valores / nº observações', 'Valor central dos dados'],
    ['Mediana', 'Valor central do conjunto ordenado', 'Divide dados ao meio, robusta a outliers'],
    ['Moda', 'Valor mais frequente', 'Representa o valor típico/comum'],
    ['Desvio Padrão', 'Raiz da variância', 'Dispersão em torno da média'],
    ['Variância', 'Média dos quadrados dos desvios', 'Medida de variabilidade'],
    ['Erro Padrão', 'Desv. Padrão / √n', 'Precisão da média amostral'],
    ['Mínimo', 'Menor valor observado', 'Limite inferior dos dados'],
    ['Máximo', 'Maior valor observado', 'Limite superior dos dados'],
    ['Amplitude', 'Máximo - Mínimo', 'Extensão total dos dados'],
    ['Q1 (25%)', 'Primeiro quartil', '25% dos dados são menores'],
    ['Q3 (75%)', 'Terceiro quartil', '75% dos dados são menores'],
    ['IQR', 'Q3 - Q1', 'Amplitude interquartil']
]

table3 = ax3.table(cellText=definicoes,
                  cellLoc='left',
                  loc='center',
                  colWidths=[0.15, 0.35, 0.40])

table3.auto_set_font_size(False)
table3.set_fontsize(9)
table3.scale(1, 2.5)

# Estilizar cabeçalho
for i in range(3):
    cell = table3[(0, i)]
    cell.set_facecolor('#FF6B6B')
    cell.set_text_props(weight='bold', color='white', size=10)

# Alternar cores das linhas
for i in range(1, len(definicoes)):
    for j in range(3):
        cell = table3[(i, j)]
        if i % 2 == 0:
            cell.set_facecolor('#FFE5E5')
        else:
            cell.set_facecolor('#FFF5F5')

plt.suptitle('Glossário de Métricas Estatísticas', 
             fontsize=18, 
             fontweight='bold',
             y=0.98)

plt.figtext(0.5, 0.02, 'Referência para interpretação das métricas calculadas', 
           ha='center', 
           fontsize=10,
           style='italic',
           bbox=dict(boxstyle='round', facecolor='#FFE5E5', alpha=0.5))

plt.tight_layout()
plt.savefig('glossario_metricas.png', dpi=300, bbox_inches='tight')
print("✓ Imagem 3 salva: 'glossario_metricas.png'")
plt.close()

print("\n✓ Todas as imagens foram geradas com sucesso!")

print("\n" + "=" * 70)
print("ANÁLISE CONCLUÍDA!")
print("=" * 70)
