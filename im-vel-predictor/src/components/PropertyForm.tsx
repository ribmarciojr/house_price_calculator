import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { propertySchema, PropertyFormValues } from "@/lib/validation";
import { PropertyFormData } from "@/types/property";
import {
  Home,
  BedDouble,
  Bath,
  Layers,
  Car,
  MapPin,
  Thermometer,
  Wind,
  Users,
  Archive,
  Loader2,
  Calculator,
} from "lucide-react";

interface PropertyFormProps {
  onSubmit: (data: PropertyFormData) => void;
  isLoading: boolean;
}

export function PropertyForm({ onSubmit, isLoading }: PropertyFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm<PropertyFormValues>({
    resolver: zodResolver(propertySchema),
    defaultValues: {
      area: 3000,
      bedrooms: 3,
      bathrooms: 2,
      stories: 2,
      mainroad: 0,
      guestroom: 0,
      basement: 0,
      hotwaterheating: 0,
      airconditioning: 0,
      parking: 1,
      prefarea: 0,
      furnishingstatus: "vazio",
    },
  });

  const handleFormSubmit = (data: PropertyFormValues) => {
    onSubmit(data as PropertyFormData);
  };

  const ToggleField = ({
    name,
    label,
    icon: Icon,
  }: {
    name: keyof PropertyFormValues;
    label: string;
    icon: React.ComponentType<{ className?: string }>;
  }) => {
    const value = watch(name) as 0 | 1;
    return (
      <div
        className={`toggle-option ${value === 1 ? "active" : ""}`}
        onClick={() => setValue(name, value === 1 ? 0 : 1)}
      >
        <div className="flex items-center gap-3">
          <Icon className="w-5 h-5 text-muted-foreground" />
          <span className="text-sm font-medium text-foreground">{label}</span>
        </div>
        <div
          className={`w-12 h-6 rounded-full transition-colors duration-200 ${
            value === 1 ? "bg-primary" : "bg-muted"
          } relative`}
        >
          <div
            className={`absolute top-1 w-4 h-4 rounded-full bg-card shadow transition-transform duration-200 ${
              value === 1 ? "translate-x-7" : "translate-x-1"
            }`}
          />
        </div>
        {errors[name] && (
          <span className="text-xs text-destructive">
            {errors[name]?.message}
          </span>
        )}
      </div>
    );
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-8">
      {/* Características Principais */}
      <section>
        <h3 className="section-title">
          <Home className="w-5 h-5 text-secondary" />
          Características Principais
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="label-text">Área (m²)</label>
            <input
              type="number"
              {...register("area", { valueAsNumber: true })}
              className="input-field"
              placeholder="Ex: 3000"
            />
            {errors.area && (
              <span className="text-xs text-destructive mt-1 block">
                {errors.area.message}
              </span>
            )}
          </div>

          <div>
            <label className="label-text">
              <BedDouble className="w-4 h-4 inline mr-1" />
              Quartos
              <span className="text-muted-foreground text-xs ml-1">(1-6)</span>
            </label>
            <input
              type="number"
              {...register("bedrooms", { valueAsNumber: true })}
              className="input-field"
              placeholder="Ex: 3"
            />
            {errors.bedrooms && (
              <span className="text-xs text-destructive mt-1 block">
                {errors.bedrooms.message}
              </span>
            )}
          </div>

          <div>
            <label className="label-text">
              <Bath className="w-4 h-4 inline mr-1" />
              Banheiros
              <span className="text-muted-foreground text-xs ml-1">(1-4)</span>
            </label>
            <input
              type="number"
              {...register("bathrooms", { valueAsNumber: true })}
              className="input-field"
              placeholder="Ex: 2"
            />
            {errors.bathrooms && (
              <span className="text-xs text-destructive mt-1 block">
                {errors.bathrooms.message}
              </span>
            )}
          </div>

          <div>
            <label className="label-text">
              <Layers className="w-4 h-4 inline mr-1" />
              Andares
              <span className="text-muted-foreground text-xs ml-1">(1-4)</span>
            </label>
            <input
              type="number"
              {...register("stories", { valueAsNumber: true })}
              className="input-field"
              placeholder="Ex: 2"
            />
            {errors.stories && (
              <span className="text-xs text-destructive mt-1 block">
                {errors.stories.message}
              </span>
            )}
          </div>
        </div>
      </section>

      {/* Vagas e Localização */}
      <section>
        <h3 className="section-title">
          <Car className="w-5 h-5 text-secondary" />
          Vagas e Localização
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="label-text">
              Vagas de Estacionamento
              <span className="text-muted-foreground text-xs ml-1">(0-3)</span>
            </label>
            <input
              type="number"
              {...register("parking", { valueAsNumber: true })}
              className="input-field"
              placeholder="Ex: 1"
            />
            {errors.parking && (
              <span className="text-xs text-destructive mt-1 block">
                {errors.parking.message}
              </span>
            )}
          </div>

          <div>
            <label className="label-text">Status de Mobília</label>
            <select {...register("furnishingstatus")} className="input-field">
              <option value="vazio">Vazio</option>
              <option value="semi-mobiliado">Semi-mobiliado</option>
              <option value="mobiliado">Mobiliado</option>
            </select>
            {errors.furnishingstatus && (
              <span className="text-xs text-destructive mt-1 block">
                {errors.furnishingstatus.message}
              </span>
            )}
          </div>
        </div>
      </section>

      {/* Características Adicionais */}
      <section>
        <h3 className="section-title">
          <MapPin className="w-5 h-5 text-secondary" />
          Características Adicionais
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          <ToggleField
            name="mainroad"
            label="Próximo à Rua Principal"
            icon={MapPin}
          />
          <ToggleField
            name="prefarea"
            label="Localização Preferencial"
            icon={MapPin}
          />
          <ToggleField
            name="guestroom"
            label="Quarto de Hóspedes"
            icon={Users}
          />
          <ToggleField name="basement" label="Porão" icon={Archive} />
          <ToggleField
            name="hotwaterheating"
            label="Aquecimento de Água"
            icon={Thermometer}
          />
          <ToggleField
            name="airconditioning"
            label="Ar Condicionado"
            icon={Wind}
          />
        </div>
      </section>

      {/* Submit Button */}
      <div className="pt-4">
        <button
          type="submit"
          disabled={isLoading}
          className="btn-primary w-full flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Calculando...
            </>
          ) : (
            <>
              <Calculator className="w-5 h-5" />
              Calcular Preço do Imóvel
            </>
          )}
        </button>
      </div>
    </form>
  );
}
