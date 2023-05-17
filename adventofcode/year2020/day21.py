from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce
from typing import Dict, Set


class Food(object):
    def __init__(self, food: str):
        tmp = food.split(" (contains ")
        self._ingredients = set(tmp[0].split(" "))
        self._allergens = set(tmp[1].replace(")", "").split(", "))

    @property
    def ingredients(self) -> Set[str]:
        return self._ingredients

    @property
    def allergens(self) -> Set[str]:
        return self._allergens


class Day21(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._foods = []
        for food in self._load_input_as_lines():
            self._foods.append(Food(food))

        self._unique_ingredients = set([])
        self._allergens_candidates: Dict[str, Set[str]] = {}

    def part_one(self):
        for food in self._foods:
            self._unique_ingredients = self._unique_ingredients.union(food.ingredients)
            for allergen in food.allergens:
                if allergen not in self._allergens_candidates:
                    # first time encountering this allergen, food's ingredients form the base of candidate ingredients that contain this allergen
                    self._allergens_candidates[allergen] = food.ingredients.copy()
                else:
                    # already seen this allergen, so only the ingredients that are in both the food and current candidate ingredients contain this allergen
                    self._allergens_candidates[allergen] = self._allergens_candidates[allergen].intersection(food.ingredients)

        ingredients_with_allergens = reduce(lambda acc, ingredients: acc.union(ingredients), self._allergens_candidates.values(), set([]))
        ingredients_with_no_allergens = self._unique_ingredients.difference(ingredients_with_allergens)

        print(f"ingredients with no allergens : {ingredients_with_no_allergens}")

        appear = 0
        for ingredient in ingredients_with_no_allergens:
            for food in self._foods:
                if ingredient in food.ingredients:
                    appear += 1

        return appear

    def part_two(self):
        danger_list: Dict[str, str] = {}
        while len(self._allergens_candidates) > 0:
            for allergen, ingredients in self._allergens_candidates.items():
                if len(ingredients) == 1:
                    deduced_allergen = allergen
                    deduced_ingredient = list(ingredients)[0]
                    danger_list[allergen] = deduced_ingredient
                    break
            else:
                raise Exception(f"Could not deduce an ingredient")

            self._allergens_candidates.pop(deduced_allergen)
            for allergen in self._allergens_candidates.keys():
                if deduced_ingredient in self._allergens_candidates[allergen]:
                    self._allergens_candidates[allergen].remove(deduced_ingredient)

        return ",".join([danger_list[key] for key in sorted(danger_list.keys())])
