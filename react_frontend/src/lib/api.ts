import type { Recipe, MealPlan } from "@/types/recipe";

const RAW_BASE_URL = (import.meta.env.VITE_API_URL ?? "").trim();
const BASE_URL = RAW_BASE_URL.replace(/\/+$/, "");

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  if (import.meta.env.PROD && !BASE_URL) {
    throw new ApiError(
      500,
      "Frontend is missing VITE_API_URL. Set it in Vercel Environment Variables and redeploy.",
    );
  }

  let res: Response;
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...init,
    });
  } catch {
    throw new ApiError(
      0,
      "Network error while contacting API. Check backend URL, CORS (ALLOWED_ORIGINS), and backend health.",
    );
  }

  const contentType = res.headers.get("content-type") ?? "";
  const bodyText = await res.text();

  if (!res.ok) {
    throw new ApiError(res.status, bodyText || `Request failed with status ${res.status}`);
  }

  if (!contentType.includes("application/json")) {
    throw new ApiError(
      502,
      "API returned non-JSON response. Verify VITE_API_URL points to backend (Render), not frontend (Vercel).",
    );
  }

  return JSON.parse(bodyText) as T;
}

export interface PredictRequest {
  nutrition_input: [number, number, number, number, number, number, number, number, number];
  ingredients: string[];
  params: { n_neighbors: number; return_distance: false };
}

export interface MealPlanRequest {
  age: number;
  height: number;
  weight: number;
  gender: "Male" | "Female";
  activity: string;
  number_of_meals: 3 | 4 | 5;
  weight_loss: string;
}

export async function predictRecipes(req: PredictRequest): Promise<Recipe[]> {
  const data = await apiFetch<{ output: Recipe[] | null }>("/predict/", {
    method: "POST",
    body: JSON.stringify(req),
  });
  return data.output ?? [];
}

export async function generateMealPlan(req: MealPlanRequest): Promise<MealPlan> {
  return apiFetch<MealPlan>("/generate-meal-plan/", {
    method: "POST",
    body: JSON.stringify(req),
  });
}
