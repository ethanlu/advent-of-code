import re

input = ['Sprinkles: capacity 2, durability 0, flavor -2, texture 0, calories 3','Butterscotch: capacity 0, durability 5, flavor -3, texture 0, calories 3','Chocolate: capacity 0, durability 0, flavor 5, texture -1, calories 8','Candy: capacity 0, durability -1, flavor 0, texture 5, calories 8']

class Day15(object):
    INGREDIENT_SUM = 100

    def __init__(self, ingredients):
        self.ingredients = []
        self.ingredient_properties = {}

        for i in ingredients:
            r = re.match('^(\w*)\: capacity (\-?\d+), durability (\-?\d+), flavor (\-?\d+), texture (\-?\d+), calories (\-?\d+)$', i)

            if r is None:
                raise Exception('invalid input : ' + i)

            self.ingredient_properties[r.group(1)] = {'capacity': int(r.group(2)),
                                                      'durability': int(r.group(3)),
                                                      'flavor': int(r.group(4)),
                                                      'texture': int(r.group(5)),
                                                      'calories': int(r.group(6))}
            self.ingredients = self.ingredient_properties.keys()

    def _get_recipe_goodness(self, recipe, calories_requirement=None):
        capacity = 0
        durability = 0
        flavor = 0
        texture = 0
        calories = 0
        for i, weight in enumerate(recipe):
            capacity += weight*self.ingredient_properties[self.ingredients[i]]['capacity']
            durability += weight*self.ingredient_properties[self.ingredients[i]]['durability']
            flavor += weight*self.ingredient_properties[self.ingredients[i]]['flavor']
            texture += weight*self.ingredient_properties[self.ingredients[i]]['texture']
            calories += weight*self.ingredient_properties[self.ingredients[i]]['calories']

        return max(capacity,0)*max(durability,0)*max(flavor,0)*max(texture,0)*(1 if calories_requirement is None or calories_requirement == calories else 0)

    def _generate_recipes_elegantly(self, ingredient_sum, num_ingredients):
        # lazy load recipes
        if num_ingredients == 1:
            yield (ingredient_sum,)
        else:
            for i in xrange(ingredient_sum + 1):
                for j in self._generate_recipes_elegantly(ingredient_sum - i, num_ingredients - 1):
                    yield (i,) + j

    def _generate_recipes(self, ingredient_sum, num_ingredients):
        if num_ingredients <= 1:
            return (ingredient_sum,)
        else:
            recipes = []
            for i in range(ingredient_sum + 1):
                sub_recipes = self._generate_recipes(ingredient_sum - i, num_ingredients - 1)
                if type(sub_recipes) == list:
                    for sub_recipe in sub_recipes:
                        recipes.append((i,) + sub_recipe)
                else:
                    recipes.append((i,) + sub_recipes)
            return list(recipes)

    def part_one(self, elegant=False):
        best_recipe = 0
        recipes = self._generate_recipes_elegantly(self.INGREDIENT_SUM, len(self.ingredients)) if elegant else self._generate_recipes(self.INGREDIENT_SUM, len(self.ingredients))
        for recipe in recipes:
            recipe_goodness = self._get_recipe_goodness(recipe)

            if best_recipe == 0 or best_recipe < recipe_goodness:
                best_recipe = recipe_goodness

        return best_recipe

    def part_two(self, elegant=False):
        best_recipe = 0
        recipes = self._generate_recipes_elegantly(self.INGREDIENT_SUM, len(self.ingredients)) if elegant else self._generate_recipes(self.INGREDIENT_SUM, len(self.ingredients))
        for recipe in recipes:
            recipe_goodness = self._get_recipe_goodness(recipe, calories_requirement=500)

            if best_recipe == 0 or best_recipe < recipe_goodness:
                best_recipe = recipe_goodness

        return best_recipe
