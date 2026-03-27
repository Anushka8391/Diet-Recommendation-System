import os
from contextlib import asynccontextmanager
from typing import Annotated, List, Literal, Optional

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import DEFAULT_N_NEIGHBORS, MEALS_CALORIES_PERC, WEIGHT_LOSS_PLANS
from image_finder import get_image_url
from model import output_recommended_recipes, recommend
from nutrition import build_nutrition_vector, calculate_bmi, calculate_bmr, calculate_tdee

# Absolute path so the app works regardless of working directory.
_DATASET_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'Data', 'dataset.csv'
)

dataset: Optional[pd.DataFrame] = None


def _parse_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        value = int(raw)
        return value if value > 0 else default
    except ValueError:
        return default


@asynccontextmanager
async def lifespan(app: FastAPI):
    global dataset
    if dataset is None:
        # Load only the columns required by the recommendation pipeline and API
        # response, and use compact float dtypes to reduce memory on low-RAM
        # hosts (e.g., Render free instances).
        # DATASET_MAX_ROWS allows tuning memory usage by limiting loaded rows.
        # LOAD_RECIPE_INSTRUCTIONS=false skips a very large text column.
        max_rows = _parse_int_env("DATASET_MAX_ROWS", 500)  # Very small for testing
        load_instructions = os.getenv("LOAD_RECIPE_INSTRUCTIONS", "false").lower() == "true"
        usecols = [
            'RecipeId', 'Name', 'CookTime', 'PrepTime', 'TotalTime',
            'RecipeIngredientParts', 'Calories', 'FatContent',
            'SaturatedFatContent', 'CholesterolContent', 'SodiumContent',
            'CarbohydrateContent', 'FiberContent', 'SugarContent',
            'ProteinContent'
        ]
        if load_instructions:
            usecols.append('RecipeInstructions')
        dtype_map = {
            'Calories': 'float32',
            'FatContent': 'float32',
            'SaturatedFatContent': 'float32',
            'CholesterolContent': 'float32',
            'SodiumContent': 'float32',
            'CarbohydrateContent': 'float32',
            'FiberContent': 'float32',
            'SugarContent': 'float32',
            'ProteinContent': 'float32',
        }
        try:
            dataset = pd.read_csv(
                _DATASET_PATH,
                compression='gzip',
                usecols=usecols,
                dtype=dtype_map,
                nrows=max_rows,
            )
            if 'RecipeInstructions' not in dataset.columns:
                dataset['RecipeInstructions'] = '[]'
            print(f"Dataset loaded successfully with {len(dataset)} rows")
        except Exception as e:
            print(f"Error loading dataset: {e}")
            dataset = pd.DataFrame()  # Empty dataframe as fallback
    yield


app = FastAPI()

_default_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:80",
]
_allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if _allowed_origins_env.strip():
    _allowed_origins = [o.strip() for o in _allowed_origins_env.split(",") if o.strip()]
else:
    _allowed_origins = _default_origins

_allowed_origin_regex = os.getenv("ALLOWED_ORIGIN_REGEX", r"https://.*\.vercel\.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_origin_regex=_allowed_origin_regex,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# ---------------------------------------------------------------------------
# Shared models
# ---------------------------------------------------------------------------

class Recipe(BaseModel):
    Name: str
    CookTime: str
    PrepTime: str
    TotalTime: str
    RecipeIngredientParts: list[str]
    Calories: float
    FatContent: float
    SaturatedFatContent: float
    CholesterolContent: float
    SodiumContent: float
    CarbohydrateContent: float
    FiberContent: float
    SugarContent: float
    ProteinContent: float
    RecipeInstructions: list[str]
    image_url: Optional[str] = None


# ---------------------------------------------------------------------------
# /predict/ — custom nutrition-based recommendation
# ---------------------------------------------------------------------------

class Params(BaseModel):
    n_neighbors: int = DEFAULT_N_NEIGHBORS
    return_distance: bool = False


class PredictionIn(BaseModel):
    nutrition_input: Annotated[list[float], Field(min_length=9, max_length=9)]
    ingredients: list[str] = []
    params: Optional[Params] = None


class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None


# ---------------------------------------------------------------------------
# /generate-meal-plan/ — automatic meal plan from personal data
# ---------------------------------------------------------------------------

class PersonData(BaseModel):
    age: int
    height: float               # cm
    weight: float               # kg
    gender: Literal["Male", "Female"]
    activity: str               # must be a key in ACTIVITY_MULTIPLIERS
    number_of_meals: Literal[3, 4, 5]
    weight_loss: str            # must be a key in WEIGHT_LOSS_PLANS


class MealRecommendation(BaseModel):
    meal_name: str
    recipes: List[Recipe]


class MealPlanOut(BaseModel):
    bmi: float
    bmr: float
    maintain_calories: float    # TDEE (no weight-loss adjustment)
    target_calories: float      # TDEE × weight-loss factor
    meals: List[MealRecommendation]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def home():
    return {"health_check": "OK"}


@app.post("/predict/", response_model=PredictionOut)
def predict(prediction_input: PredictionIn):
    # Temporarily disabled for testing
    return {"output": []}


@app.post("/generate-meal-plan/", response_model=MealPlanOut)
def generate_meal_plan(person: PersonData):
    # Temporarily disabled for testing
    return MealPlanOut(
        bmi=25.0,
        bmr=1500.0,
        maintain_calories=2000,
        target_calories=1800,
        meals=[],
    )
