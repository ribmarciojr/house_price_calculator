import { useState } from "react";
import { PropertyForm } from "@/components/PropertyForm";
import { PriceResult } from "@/components/PriceResult";
import { ErrorMessage } from "@/components/ErrorMessage";
import { predictPrice } from "@/lib/api";
import { PropertyFormData, PredictionResponse } from "@/types/property";
import { Building2, Sparkles } from "lucide-react";

const Index = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lastFormData, setLastFormData] = useState<PropertyFormData | null>(
    null
  );

  const handleSubmit = async (data: PropertyFormData) => {
    setIsLoading(true);
    setError(null);
    setResult(null);
    setLastFormData(data);

    try {
      const response = await predictPrice(data);
      setResult(response);
    } catch (err) {
      const errorMessage =
        err instanceof Error
          ? err.message
          : "Erro desconhecido. Tente novamente.";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    if (lastFormData) {
      handleSubmit(lastFormData);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl gradient-navy">
              <Building2 className="w-8 h-8 text-gold" />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-display font-bold text-foreground">
                Calculadora de Imóveis
              </h1>
              <p className="text-sm text-muted-foreground">
                Estimativa inteligente de preços
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 md:py-12">
        <div className="max-w-4xl mx-auto">
          {/* Intro */}
          <div className="mb-8 text-center">
            <h2 className="text-xl md:text-2xl font-display text-foreground mb-2">
              Descubra o valor do seu imóvel
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Preencha as características do imóvel abaixo para obter uma
              estimativa precisa do seu valor de mercado.
            </p>
          </div>

          {/* Form Card */}
          <div className="glass-card rounded-2xl p-6 md:p-8 mb-8">
            <PropertyForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-8">
              <ErrorMessage
                message={error}
                onClose={() => setError(null)}
                onRetry={handleRetry}
              />
            </div>
          )}

          {/* Result */}
          {result && (
            <PriceResult result={result} onClose={() => setResult(null)} />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-card mt-auto">
        <div className="container mx-auto px-4 py-6">
          <p className="text-center text-sm text-muted-foreground">
            Os valores apresentados são estimativas e podem variar conforme
            condições de mercado.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
