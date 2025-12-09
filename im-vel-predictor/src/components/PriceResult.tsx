import { PredictionResponse } from "@/types/property";
import { TrendingUp, Shield, Info, X } from "lucide-react";

interface PriceResultProps {
  result: PredictionResponse;
  onClose: () => void;
}

export function PriceResult({ result, onClose }: PriceResultProps) {
  const getConfidenceColor = (confidence: string) => {
    const confidenceLower = confidence.toLowerCase();
    if (confidenceLower.includes("alta") || confidenceLower.includes("high")) {
      return "bg-success text-success-foreground";
    }
    if (confidenceLower.includes("média") || confidenceLower.includes("medium")) {
      return "bg-secondary text-secondary-foreground";
    }
    return "bg-muted text-muted-foreground";
  };

  return (
    <div className="animate-slide-up">
      <div className="result-card relative overflow-hidden">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-full bg-primary-foreground/10 hover:bg-primary-foreground/20 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-gold/10 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-gold/5 rounded-full translate-y-1/2 -translate-x-1/2" />

        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-6">
            <TrendingUp className="w-6 h-6 text-gold" />
            <h3 className="text-xl font-semibold">Resultado da Avaliação</h3>
          </div>

          <div className="mb-6">
            <p className="text-sm text-primary-foreground/70 mb-2">Preço Estimado</p>
            <p className="text-4xl md:text-5xl font-display font-bold text-gold animate-pulse-subtle">
              {result.preco_formatado}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Shield className="w-5 h-5 text-primary-foreground/70" />
            <span className="text-sm text-primary-foreground/70">Nível de Confiança:</span>
            <span className={`confidence-badge ${getConfidenceColor(result.confianca)}`}>
              {result.confianca}
            </span>
          </div>
        </div>
      </div>

      {/* Features Section */}
      {result.features && Object.keys(result.features).length > 0 && (
        <div className="mt-6 p-6 rounded-xl glass-card">
          <div className="flex items-center gap-2 mb-4">
            <Info className="w-5 h-5 text-muted-foreground" />
            <h4 className="font-semibold text-foreground">Features Utilizadas no Cálculo</h4>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {Object.entries(result.features).map(([key, value]) => (
              <div key={key} className="p-3 rounded-lg bg-muted/50">
                <p className="text-xs text-muted-foreground capitalize">{key.replace(/_/g, " ")}</p>
                <p className="text-sm font-medium text-foreground">{String(value)}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
