import { useState } from "react";
import { Recipe, NUTRITION_COLUMNS } from "@/types/recipe";
import { Clock, ChevronDown, ChevronUp, UtensilsCrossed } from "lucide-react";

const PLACEHOLDER = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop";

function normalizeImageUrl(url?: string | null): string {
  if (!url) return PLACEHOLDER;
  const trimmed = url.trim();
  return trimmed.startsWith("http://") || trimmed.startsWith("https://") ? trimmed : PLACEHOLDER;
}

function formatDuration(iso: string): string {
  if (!iso) return "—";
  const match = iso.match(/PT(?:(\d+)H)?(?:(\d+)M)?/);
  if (!match) return iso;
  const hours = parseInt(match[1] ?? "0");
  const minutes = parseInt(match[2] ?? "0");
  const total = hours * 60 + minutes;
  return total > 0 ? `${total} min` : "—";
}

const oneDecimalFormatter = new Intl.NumberFormat("en-US", { maximumFractionDigits: 1 });

function formatNutritionValue(value: number, key?: keyof Recipe): string {
  if (!Number.isFinite(value)) return "—";
  if (key === "Calories") return Math.round(value).toString();
  return oneDecimalFormatter.format(value);
}

interface RecipeCardProps {
  recipe: Recipe;
}

function RecipeImage({ src, alt }: { src: string; alt: string }) {
  const [imgSrc, setImgSrc] = useState(normalizeImageUrl(src));
  return (
    <div className="h-40 overflow-hidden rounded-t-xl">
      <img
        src={imgSrc}
        alt={alt}
        className="h-full w-full object-cover"
        loading="lazy"
        onError={() => {
          if (imgSrc !== PLACEHOLDER) {
            setImgSrc(PLACEHOLDER);
          }
        }}
      />
    </div>
  );
}

export default function RecipeCard({ recipe }: RecipeCardProps) {
  const [expanded, setExpanded] = useState(false);
  const safeImage = normalizeImageUrl(recipe.image_url);

  return (
    <div className="recipe-card">
      <RecipeImage src={safeImage} alt={recipe.Name} />
      <div className="p-5">
        <div className="mb-3 flex items-start justify-between gap-2">
          <h3 className="font-display text-lg font-semibold text-card-foreground leading-tight">
            {recipe.Name}
          </h3>
          <span className="shrink-0 rounded-full bg-accent px-2.5 py-0.5 text-xs font-semibold text-accent-foreground">
            {Math.round(recipe.Calories)} cal
          </span>
        </div>

        <div className="mb-3 flex items-center gap-4 text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <Clock className="h-3.5 w-3.5" /> {formatDuration(recipe.TotalTime)}
          </span>
          <span className="flex items-center gap-1">
            <UtensilsCrossed className="h-3.5 w-3.5" /> {recipe.RecipeIngredientParts.length} ingredients
          </span>
        </div>

        {/* Nutrition mini-bar */}
        <div className="mb-3 grid grid-cols-3 gap-2 text-xs">
          <div className="rounded-md bg-muted p-2 text-center">
            <div className="font-semibold text-foreground">{formatNutritionValue(recipe.ProteinContent)}g</div>
            <div className="text-muted-foreground">Protein</div>
          </div>
          <div className="rounded-md bg-muted p-2 text-center">
            <div className="font-semibold text-foreground">{formatNutritionValue(recipe.CarbohydrateContent)}g</div>
            <div className="text-muted-foreground">Carbs</div>
          </div>
          <div className="rounded-md bg-muted p-2 text-center">
            <div className="font-semibold text-foreground">{formatNutritionValue(recipe.FatContent)}g</div>
            <div className="text-muted-foreground">Fat</div>
          </div>
        </div>

        <button
          onClick={() => setExpanded(!expanded)}
          className="flex w-full items-center justify-center gap-1 rounded-lg border bg-background py-2 text-xs font-medium text-muted-foreground transition-colors hover:bg-muted"
        >
          {expanded ? "Less" : "More"} details
          {expanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
        </button>

        {expanded && (
          <div className="mt-4 animate-fade-in space-y-4 text-sm">
            {/* Full nutrition */}
            <div>
              <h4 className="mb-2 font-semibold text-foreground">Nutritional Values</h4>
              <div className="grid grid-cols-2 gap-1.5 text-xs">
                {NUTRITION_COLUMNS.map((col) => (
                  <div key={col} className="flex justify-between rounded bg-muted px-2 py-1">
                    <span className="text-muted-foreground">{col.replace('Content', '')}</span>
                    <span className="font-medium text-foreground">
                      {formatNutritionValue(recipe[col as keyof Recipe] as number, col as keyof Recipe)}{col === 'Calories' ? ' kcal' : 'g'}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Ingredients */}
            <div>
              <h4 className="mb-2 font-semibold text-foreground">Ingredients</h4>
              <ul className="list-inside list-disc space-y-0.5 text-muted-foreground">
                {recipe.RecipeIngredientParts.map((ing, i) => (
                  <li key={i}>{ing}</li>
                ))}
              </ul>
            </div>

            {/* Instructions */}
            <div>
              <h4 className="mb-2 font-semibold text-foreground">Instructions</h4>
              <ol className="list-inside list-decimal space-y-1 text-muted-foreground">
                {recipe.RecipeInstructions.map((step, i) => (
                  <li key={i}>{step}</li>
                ))}
              </ol>
            </div>

            {/* Time */}
            <div className="flex gap-4 text-xs text-muted-foreground">
              <span>Prep: {formatDuration(recipe.PrepTime)}</span>
              <span>Cook: {formatDuration(recipe.CookTime)}</span>
              <span>Total: {formatDuration(recipe.TotalTime)}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
