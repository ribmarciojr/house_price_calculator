from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator, ConfigDict
import joblib
import pandas as pd
import numpy as np
from typing import Optional

app = FastAPI(
    title="API de Previsão de Preços de Casas",
    description="API para prever preços de imóveis usando Random Forest",
    version="1.0.0"
)

# Configurar CORS para permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

try:
    model = joblib.load('random_forest_model.pkl')
    feature_info = joblib.load('feature_info.pkl')
    print("✓ Modelo carregado com sucesso!")
except Exception as e:
    print(f"✗ Erro ao carregar modelo: {e}")
    model = None
    feature_info = None

class HouseFeatures(BaseModel):
    area: int = Field(..., description="Área da casa em pés quadrados", ge=1650, le=16200)
    bedrooms: int = Field(..., description="Número de quartos", ge=1, le=6)
    bathrooms: int = Field(..., description="Número de banheiros", ge=1, le=4)
    stories: int = Field(..., description="Número de andares", ge=1, le=4)
    mainroad: int = Field(..., description="Próximo à rua principal (0=não, 1=sim)", ge=0, le=1)
    guestroom: int = Field(..., description="Possui quarto de hóspedes (0=não, 1=sim)", ge=0, le=1)
    basement: int = Field(..., description="Possui porão (0=não, 1=sim)", ge=0, le=1)
    hotwaterheating: int = Field(..., description="Possui aquecimento de água (0=não, 1=sim)", ge=0, le=1)
    airconditioning: int = Field(..., description="Possui ar-condicionado (0=não, 1=sim)", ge=0, le=1)
    parking: int = Field(..., description="Número de vagas de garagem", ge=0, le=3)
    prefarea: int = Field(..., description="Localização preferencial (0=não, 1=sim)", ge=0, le=1)
    furnishingstatus: str = Field(..., description="Status de mobília: 'mobiliado', 'semi-mobiliado' ou 'vazio'")

    @field_validator('furnishingstatus')
    @classmethod
    def validate_furnishing(cls, v):
        valid_values = ['mobiliado', 'semi-mobiliado', 'vazio']
        if v not in valid_values:
            raise ValueError(f"furnishingstatus deve ser um dos seguintes: {', '.join(valid_values)}")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
        }
    )

class PredictionResponse(BaseModel):
    preco_predito: float = Field(..., description="Preço predito da casa")
    preco_formatado: str = Field(..., description="Preço formatado em reais")
    features_utilizadas: dict = Field(..., description="Features utilizadas na predição")
    confianca: str = Field(..., description="Nível de confiança da predição")

@app.post("/predict", response_model=PredictionResponse)
async def predict_price(house: HouseFeatures):
    """
    Endpoint para prever o preço de uma casa com base nas características fornecidas.
    
    **Parâmetros:**
    - **area**: Área da casa em pés quadrados (1650-16200)
    - **bedrooms**: Número de quartos (1-6)
    - **bathrooms**: Número de banheiros (1-4)
    - **stories**: Número de andares (1-4)
    - **mainroad**: Próximo à rua principal (0=não, 1=sim)
    - **guestroom**: Possui quarto de hóspedes (0=não, 1=sim)
    - **basement**: Possui porão (0=não, 1=sim)
    - **hotwaterheating**: Possui aquecimento de água (0=não, 1=sim)
    - **airconditioning**: Possui ar-condicionado (0=não, 1=sim)
    - **parking**: Número de vagas de garagem (0-3)
    - **prefarea**: Localização preferencial (0=não, 1=sim)
    - **furnishingstatus**: Status de mobília ('mobiliado', 'semi-mobiliado' ou 'vazio')
    
    **Retorna:**
    - Preço predito da casa
    - Preço formatado em reais
    - Features utilizadas
    - Nível de confiança
    """
    
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Modelo não carregado. Execute model_training.py primeiro."
        )
    
    try:
        input_data = {
            'area': house.area,
            'bedrooms': house.bedrooms,
            'bathrooms': house.bathrooms,
            'stories': house.stories,
            'mainroad': house.mainroad,
            'guestroom': house.guestroom,
            'basement': house.basement,
            'hotwaterheating': house.hotwaterheating,
            'airconditioning': house.airconditioning,
            'parking': house.parking,
            'prefarea': house.prefarea,
            'furnishingstatus_semi-mobiliado': 1 if house.furnishingstatus == 'semi-mobiliado' else 0,
            'furnishingstatus_vazio': 1 if house.furnishingstatus == 'vazio' else 0
        }
        
        df_input = pd.DataFrame([input_data])
        
        prediction = model.predict(df_input)[0]

        confianca_score = 0
        if 3000 <= house.area <= 8000:
            confianca_score += 40
        elif house.area > 1650:
            confianca_score += 20
        
        if house.bathrooms >= 2:
            confianca_score += 30
        else:
            confianca_score += 15
        
        if house.airconditioning == 1:
            confianca_score += 15
        
        if house.parking >= 1:
            confianca_score += 15
        
        if confianca_score >= 80:
            confianca = "Alta"
        elif confianca_score >= 60:
            confianca = "Média"
        else:
            confianca = "Baixa"
        
        response = PredictionResponse(
            preco_predito=float(prediction),
            preco_formatado=f"R$ {prediction:,.2f}",
            features_utilizadas=input_data,
            confianca=confianca
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer predição: {str(e)}"
        )


@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "mensagem": "API de Previsão de Preços de Casas",
        "versao": "1.0.0",
        "endpoints": {
            "/predict": "POST - Fazer predição de preço",
            "/health": "GET - Verificar status da API",
            "/docs": "GET - Documentação interativa Swagger",
            "/redoc": "GET - Documentação alternativa ReDoc"
        },
        "status": "online",
        "modelo_carregado": model is not None
    }


@app.get("/health")
async def health_check():
    """Health check endpoint - responde imediatamente quando API está pronta"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")
    return {
        "status": "healthy",
        "modelo": "carregado",
        "versao": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    import sys
    
    # Verificar se uma porta foi especificada como argumento
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Porta inválida: {sys.argv[1]}. Usando porta padrão 8000.")
    
    print("=" * 70)
    print("🚀 INICIANDO API DE PREVISÃO DE PREÇOS DE CASAS")
    print("=" * 70)
    print(f"\n📍 Endpoints disponíveis:")
    print(f"  • http://localhost:{port}/")
    print(f"  • http://localhost:{port}/predict (POST)")
    print(f"  • http://localhost:{port}/docs (Documentação Swagger)")
    print(f"  • http://localhost:{port}/redoc (Documentação ReDoc)")
    print("\n" + "=" * 70)
    print(f"💡 Para usar outra porta, execute: python api.py <porta>")
    print(f"   Exemplo: python api.py 8080")
    print("=" * 70 + "\n")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=port)
    except OSError as e:
        if "address already in use" in str(e).lower():
            print(f"\n❌ ERRO: Porta {port} já está em uso!")
            print(f"💡 Soluções:")
            print(f"   1. Use outra porta: python api.py 8080")
            print(f"   2. Mate o processo: pkill -f 'python.*api.py'")
            print(f"   3. Encontre o processo: lsof -i :{port}")
        else:
            print(f"\n❌ ERRO: {e}")
        sys.exit(1)
