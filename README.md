# API de Previsão de Preços de Casas

# Dados de Entrada

<img width="1922" height="1080" alt="image" src="https://github.com/user-attachments/assets/915341fb-c883-495d-8019-1538fbd2a279" />

# Previsão do modelo

<img width="1909" height="994" alt="image" src="https://github.com/user-attachments/assets/d682a631-ab27-4563-ba7a-9b474b2d6925" />


## 📦 Requisitos

- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+ (para desenvolvimento frontend)
- npm ou yarn

## 🚀 Início Rápido

### Opção 1: Docker Compose (Recomendado)

Inicia a API backend automaticamente:

```bash
# Iniciar API com Docker Compose
docker-compose up -d

# Verificar status
docker-compose logs -f api

# Verificar health
curl http://localhost:8000/health
```

A API estará disponível em: **http://localhost:8000**

### Opção 2: Docker Build Manual

```bash
# 1. Build da imagem
docker build -t house-price-api .

# 2. Executar container
docker run -d \
  --name house-price-api \
  -p 8000:8000 \
  -v $(pwd)/random_forest_model.pkl:/app/random_forest_model.pkl:ro \
  -v $(pwd)/feature_info.pkl:/app/feature_info.pkl:ro \
  house-price-api

# 3. Verificar status
docker logs -f house-price-api
```

## 🖥️ Interface React (Frontend)

### Instalação e Execução

```bash
# Entrar no diretório do frontend
cd im-vel-predictor

# Instalar dependências
npm install

# Rodar em modo desenvolvimento
npm run dev
```

A interface estará disponível em: **http://localhost:5173**

### Build para Produção

```bash
# Build otimizado
npm run build

# Preview do build
npm run preview
```

### Configuração da API

Certifique-se que a API está rodando em `http://localhost:8000`. O frontend está configurado para se conectar nesse endereço.

Para mudar a URL da API, edite o arquivo:
```typescript
// im-vel-predictor/src/lib/api.ts
const API_URL = "http://localhost:8000";
```

## 📱 Stack Completo

### Backend (API)
- **Framework:** FastAPI
- **Modelo:** Random Forest (scikit-learn)
- **Porta:** 8000
- **Docs:** http://localhost:8000/docs

### Frontend (Interface)
- **Framework:** React + TypeScript
- **Build Tool:** Vite
- **UI:** Shadcn/ui + Tailwind CSS
- **Validação:** Zod + React Hook Form
- **Porta:** 5173 (dev) / 4173 (preview)

## 🛠️ Comandos Úteis

### Backend (API Docker)

```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Reconstruir imagem
docker-compose build --no-cache

# Ver logs em tempo real
docker-compose logs -f api

# Reiniciar API
docker-compose restart api
```

### Frontend (React)

```bash
cd im-vel-predictor

# Desenvolvimento
npm run dev              # Iniciar dev server
npm run build           # Build de produção
npm run preview         # Preview do build
npm run lint            # Verificar código

# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Acessar API

```bash
# Endpoint raiz
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Documentação Swagger
open http://localhost:8000/docs

# Fazer predição
curl -X POST http://localhost:8000/predict \
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

## 📋 Estrutura de Arquivos

```
sis_decision/
├── Dockerfile                      # Definição da imagem Docker
├── docker-compose.yml              # Orquestração de containers
├── .dockerignore                   # Arquivos ignorados no build
├── requirements.txt                # Dependências Python
├── api.py                         # Código da API FastAPI
├── random_forest_model.pkl        # Modelo treinado
├── feature_info.pkl               # Informações das features
└── im-vel-predictor/              # Frontend React
    ├── src/
    │   ├── components/            # Componentes React
    │   ├── lib/                   # Utilitários e API client
    │   ├── types/                 # TypeScript types
    │   └── pages/                 # Páginas
    ├── package.json               # Dependências Node
    └── vite.config.ts             # Configuração Vite
```

## 🔧 Configuração

### Variáveis de Ambiente

```bash
PORT=8000                  # Porta da API
PYTHONUNBUFFERED=1        # Logs em tempo real
```

### Portas Expostas

- **8000**: API FastAPI

### Health Check

- Endpoint: `GET /health`
- Intervalo: 30s
- Timeout: 10s
- Start period: 10s

## 🐳 Deploy em Produção

### Railway / Render / Fly.io

```bash
# Usar Dockerfile diretamente
# A plataforma detectará automaticamente
```

### AWS ECS / Azure Container Instances / GCP Cloud Run

```bash
# 1. Build e tag da imagem
docker build -t your-registry/house-price-api:latest .

# 2. Push para registry
docker push your-registry/house-price-api:latest

# 3. Deploy na plataforma escolhida
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: house-price-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: house-price-api
  template:
    metadata:
      labels:
        app: house-price-api
    spec:
      containers:
        - name: api
          image: your-registry/house-price-api:latest
          ports:
            - containerPort: 8000
          env:
            - name: PORT
              value: "8000"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 30
```

## 🔒 Segurança

### Recomendações de Produção

1. **CORS**: Atualizar `allow_origins` em `api.py` para domínios específicos
2. **HTTPS**: Usar proxy reverso (Nginx/Traefik) com certificado SSL
3. **Rate Limiting**: Adicionar limitação de requisições
4. **Authentication**: Implementar API keys ou JWT
5. **Secrets**: Usar variáveis de ambiente para dados sensíveis

### Exemplo com Nginx

```nginx
server {
    listen 443 ssl;
    server_name api.exemplo.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitoramento

### Logs

```bash
# Docker Compose
docker-compose logs -f api

# Docker direto
docker logs -f house-price-api
```

### Métricas

```bash
# Ver uso de recursos
docker stats house-price-api
```

## 🐛 Troubleshooting

### Problema: Container não inicia

```bash
# Verificar logs
docker-compose logs api

# Verificar se modelos existem
ls -lh random_forest_model.pkl feature_info.pkl
```

### Problema: Erro ao carregar modelo

```bash
# Verificar se arquivos estão montados
docker exec house-price-api ls -lh /app/*.pkl
```

### Problema: Health check falha

```bash
# Testar manualmente
docker exec house-price-api curl http://localhost:8000/health
```

## 📝 Notas

- Imagem base: Python 3.12-slim (~200MB)
- Tamanho final da imagem: ~500MB (incluindo dependências)
- Tempo de startup: ~2-3 segundos
- Modelo carregado em memória (lazy loading)

## 🔄 Atualização de Modelo

Para atualizar o modelo sem rebuild da imagem:

```bash
# 1. Retreinar modelo
python model_training.py

# 2. Reiniciar container (irá carregar novos arquivos)
docker-compose restart api
```
