import { AlertTriangle, X, RefreshCw } from "lucide-react";

interface ErrorMessageProps {
  message: string;
  onClose: () => void;
  onRetry?: () => void;
}

export function ErrorMessage({ message, onClose, onRetry }: ErrorMessageProps) {
  return (
    <div className="animate-fade-in p-4 rounded-xl border border-destructive/30 bg-destructive/10">
      <div className="flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h4 className="font-medium text-foreground mb-1">Erro ao calcular</h4>
          <p className="text-sm text-muted-foreground">{message}</p>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded hover:bg-destructive/20 transition-colors"
        >
          <X className="w-4 h-4 text-muted-foreground" />
        </button>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-3 flex items-center gap-2 text-sm text-primary hover:text-primary/80 transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Tentar novamente
        </button>
      )}
    </div>
  );
}
