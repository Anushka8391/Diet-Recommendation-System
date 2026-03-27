import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer


def scaling(dataframe):
    scaler = StandardScaler()
    prep_data = scaler.fit_transform(dataframe.iloc[:, 6:15].to_numpy())
    return prep_data, scaler


def nn_predictor(prep_data):
    neigh = NearestNeighbors(metric='cosine', algorithm='brute')
    neigh.fit(prep_data)
    return neigh


def build_pipeline(neigh, scaler, params):
    transformer = FunctionTransformer(neigh.kneighbors, kw_args=params)
    pipeline = Pipeline([('std_scaler', scaler), ('NN', transformer)])
    return pipeline


def extract_ingredient_filtered_data(dataframe, ingredients):
    """Filter recipes to those containing all specified ingredients.

    Uses case-insensitive substring matching directly on RecipeIngredientParts.
    This avoids storing preprocessed per-row ingredient sets in memory, which is
    important for low-memory deployment targets.
    """
    if not ingredients:
        return dataframe
    filtered = dataframe
    for ingredient in ingredients:
        q = (ingredient or "").strip()
        if not q:
            continue
        filtered = filtered[
            filtered['RecipeIngredientParts'].str.contains(q, case=False, regex=False, na=False)
        ]
    return filtered


def apply_pipeline(pipeline, _input, extracted_data):
    _input = np.array(_input).reshape(1, -1)
    return extracted_data.iloc[pipeline.transform(_input)[0]]


def recommend(dataframe, _input, ingredients=[], params={'n_neighbors': 5, 'return_distance': False}):
    extracted_data = extract_ingredient_filtered_data(dataframe, ingredients)
    if extracted_data.shape[0] >= params['n_neighbors']:
        prep_data, scaler = scaling(extracted_data)
        neigh = nn_predictor(prep_data)
        pipeline = build_pipeline(neigh, scaler, params)
        return apply_pipeline(pipeline, _input, extracted_data)
    return None


def extract_quoted_strings(s):
    if not isinstance(s, str):
        return []
    return re.findall(r'"([^"]*)"', s)


def output_recommended_recipes(dataframe):
    if dataframe is None:
        return None
    output = dataframe.to_dict("records")
    for recipe in output:
        recipe['RecipeIngredientParts'] = extract_quoted_strings(recipe.get('RecipeIngredientParts'))
        recipe['RecipeInstructions'] = extract_quoted_strings(recipe.get('RecipeInstructions'))
        # Dataset stores time fields as integers; coerce to str for Pydantic v2 compatibility.
        for time_field in ('CookTime', 'PrepTime', 'TotalTime'):
            recipe[time_field] = str(recipe.get(time_field, ''))
    return output
