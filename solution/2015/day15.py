import re

class Day15(object):
    INGREDIENT_SUM = 100

    def __init__(self, input_file):
        self._ingredients = []
        self._ingredient_properties = {}

        with open(input_file) as f:
            for l in f.readlines():
                r = re.match('^(\w*)\: capacity (\-?\d+), durability (\-?\d+), flavor (\-?\d+), texture (\-?\d+), calories (\-?\d+)$', l)

                if r is None:
                    raise Exception('invalid input : ' + l)

                self._ingredient_properties[r.group(1)] = {'capacity': int(r.group(2)),
                                                          'durability': int(r.group(3)),
                                                          'flavor': int(r.group(4)),
                                                          'texture': int(r.group(5)),
                                                          'calories': int(r.group(6))}
                self._ingredients = self._ingredient_properties.keys()

    def _get_recipe_goodness(self, recipe, calories_requirement=None):
        capacity = 0
        durability = 0
        flavor = 0
        texture = 0
        calories = 0
        for i, weight in enumerate(recipe):
            capacity += weight*self._ingredient_properties[self._ingredients[i]]['capacity']
            durability += weight*self._ingredient_properties[self._ingredients[i]]['durability']
            flavor += weight*self._ingredient_properties[self._ingredients[i]]['flavor']
            texture += weight*self._ingredient_properties[self._ingredients[i]]['texture']
            calories += weight*self._ingredient_properties[self._ingredients[i]]['calories']

        return max(capacity,0)*max(durability,0)*max(flavor,0)*max(texture,0)*(1 if calories_requirement is None or calories_requirement == calories else 0)

    def _generate_recipes(self, ingredient_sum, num_ingredients):
        # lazy load recipes
        if num_ingredients == 1:
            yield (ingredient_sum,)
        else:
            for i in xrange(ingredient_sum + 1):
                for j in self._generate_recipes(ingredient_sum - i, num_ingredients - 1):
                    yield (i,) + j

    def part_one(self):
        best_recipe = 0
        recipes = self._generate_recipes(self.INGREDIENT_SUM, len(self._ingredients))
        for recipe in recipes:
            recipe_goodness = self._get_recipe_goodness(recipe)

            if best_recipe == 0 or best_recipe < recipe_goodness:
                best_recipe = recipe_goodness

        return best_recipe

    def part_two(self):
        best_recipe = 0
        recipes = self._generate_recipes(self.INGREDIENT_SUM, len(self._ingredients))
        for recipe in recipes:
            recipe_goodness = self._get_recipe_goodness(recipe, calories_requirement=500)

            if best_recipe == 0 or best_recipe < recipe_goodness:
                best_recipe = recipe_goodness

        return best_recipe


if __name__ == '__main__':
    p = Day15('../../input/2015/day15.txt')

    print('-----part one-----')
    print(p.part_one())

    print('-----part two-----')
    print(p.part_two())
