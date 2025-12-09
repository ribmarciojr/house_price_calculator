# API de Previsão de Preços de Casas

## 🚀 Como Usar

### 1. Iniciar a API

```bash
source venv/bin/activate
python api.py
```

A API estará disponível em: `http://localhost:8000`

---

## 📡 Endpoint: POST /predict

### URL

```
POST http://localhost:8000/predict
```

### Parâmetros (JSON)

| Parâmetro          | Tipo   | Descrição                     | Range                                    |
| ------------------ | ------ | ----------------------------- | ---------------------------------------- |
| `area`             | int    | Área da casa em pés quadrados | 1650-16200                               |
| `bedrooms`         | int    | Número de quartos             | 1-6                                      |
| `bathrooms`        | int    | Número de banheiros           | 1-4                                      |
| `stories`          | int    | Número de andares             | 1-4                                      |
| `mainroad`         | int    | Próximo à rua principal       | 0 ou 1                                   |
| `guestroom`        | int    | Possui quarto de hóspedes     | 0 ou 1                                   |
| `basement`         | int    | Possui porão                  | 0 ou 1                                   |
| `hotwaterheating`  | int    | Possui aquecimento de água    | 0 ou 1                                   |
| `airconditioning`  | int    | Possui ar-condicionado        | 0 ou 1                                   |
| `parking`          | int    | Número de vagas de garagem    | 0-3                                      |
| `prefarea`         | int    | Localização preferencial      | 0 ou 1                                   |
| `furnishingstatus` | string | Status de mobília             | "mobiliado", "semi-mobiliado" ou "vazio" |

---

## 📝 Exemplos de Uso

### Python com requests

```python
import requests

url = "http://localhost:8000/predict"

data = {
    "area": 7420,
    "bedrooms": 4,
    "bathrooms": 2,
    "stories": 3,
    "mainroad": 1,
    "guestroom": 0,
    "basement": 0,
    "hotwaterheating": 0,
    "airconditioning": 1,
    "parking": 2,
    "prefarea": 1,
    "furnishingstatus": "mobiliado"
}

response = requests.post(url, json=data)
result = response.json()

print(f"Preço Predito: {result['preco_formatado']}")
print(f"Confiança: {result['confianca']}")
```

### cURL

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "area": 7420,
    "bedrooms": 4,
    "bathrooms": 2,
    "stories": 3,
    "mainroad": 1,
    "guestroom": 0,
    "basement": 0,
    "hotwaterheating": 0,
    "airconditioning": 1,
    "parking": 2,
    "prefarea": 1,
    "furnishingstatus": "mobiliado"
  }'
```

### JavaScript (Fetch API)

```javascript
const url = "http://localhost:8000/predict";

const data = {
  area: 7420,
  bedrooms: 4,
  bathrooms: 2,
  stories: 3,
  mainroad: 1,
  guestroom: 0,
  basement: 0,
  hotwaterheating: 0,
  airconditioning: 1,
  parking: 2,
  prefarea: 1,
  furnishingstatus: "mobiliado",
};

fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(data),
})
  .then((response) => response.json())
  .then((result) => {
    console.log("Preço Predito:", result.preco_formatado);
    console.log("Confiança:", result.confianca);
  });
```

---

## 📊 Resposta

### Formato da Resposta (JSON)

```json
{
  "preco_predito": 8825854.44,
  "preco_formatado": "R$ 8,825,854.44",
  "features_utilizadas": {
    "area": 7420,
    "bedrooms": 4,
    "bathrooms": 2,
    "stories": 3,
    "mainroad": 1,
    "guestroom": 0,
    "basement": 0,
    "hotwaterheating": 0,
    "airconditioning": 1,
    "parking": 2,
    "prefarea": 1,
    "furnishingstatus_semi-mobiliado": 0,
    "furnishingstatus_vazio": 0
  },
  "confianca": "Alta"
}
```

### Campos da Resposta

| Campo                 | Tipo   | Descrição                                      |
| --------------------- | ------ | ---------------------------------------------- |
| `preco_predito`       | float  | Preço predito em valor numérico                |
| `preco_formatado`     | string | Preço formatado em reais (R$)                  |
| `features_utilizadas` | object | Todas as features usadas na predição           |
| `confianca`           | string | Nível de confiança: "Alta", "Média" ou "Baixa" |

---

## 📚 Documentação Interativa

Acesse a documentação Swagger gerada automaticamente pelo FastAPI:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## ⚠️ Códigos de Erro

| Código | Descrição                           |
| ------ | ----------------------------------- |
| 200    | Sucesso - Predição realizada        |
| 422    | Erro de validação - Dados inválidos |
| 500    | Erro interno - Modelo não carregado |

### Exemplo de Erro (422)

```json
{
  "detail": [
    {
      "loc": ["body", "area"],
      "msg": "ensure this value is greater than or equal to 1650",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

---

## 🧪 Testar a API

Execute o script de teste incluído:

```bash
python test_api.py
```

---

## 🛑 Parar a API

Para parar o servidor, pressione `CTRL+C` no terminal onde a API está rodando.

Se iniciou em background:

```bash
pkill -f "python api.py"
```

---

## 📦 Arquivos Necessários

- `api.py` - Servidor FastAPI
- `random_forest_model.pkl` - Modelo treinado
- `feature_info.pkl` - Informações das features
- `test_api.py` - Script de teste

---

## 💡 Dicas

1. **Valores Binários**: Use `1` para "sim" e `0` para "não"
2. **Mobília**: Use exatamente `"mobiliado"`, `"semi-mobiliado"` ou `"vazio"`
3. **Confiança**: Baseada na qualidade e combinação das features
4. **Área**: Principal fator de influência no preço (48.78% de importância)
