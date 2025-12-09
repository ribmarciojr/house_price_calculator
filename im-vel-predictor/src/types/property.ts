export interface PropertyFormData {
  area: number;
  bedrooms: number;
  bathrooms: number;
  stories: number;
  mainroad: 0 | 1;
  guestroom: 0 | 1;
  basement: 0 | 1;
  hotwaterheating: 0 | 1;
  airconditioning: 0 | 1;
  parking: number;
  prefarea: 0 | 1;
  furnishingstatus: "mobiliado" | "semi-mobiliado" | "vazio";
}

export interface PredictionResponse {
  preco_formatado: string;
  confianca: string;
  features?: Record<string, number | string>;
}

export interface ApiError {
  message: string;
  status?: number;
}
