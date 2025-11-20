"""Script to seed Indian and Bihari recipes"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipeapp.settings')
django.setup()

from django.contrib.auth.models import User
from recipes.models import Recipe

# Get or create a demo user
demo_user, _ = User.objects.get_or_create(
    username='demo_chef',
    defaults={'email': 'demo@recipeapp.com'}
)

indian_recipes = [
    {
        'title': 'Butter Chicken (Murgh Makhani)',
        'description': 'Creamy and aromatic butter chicken, a classic Indian dish with tender chicken pieces in a rich tomato-based gravy.',
        'ingredients': 'Chicken breast\nButter\nCream\nTomato puree\nOnions\nGarlic\nGinger\nSpices (cumin, coriander, garam masala)',
        'instructions': 'Marinate chicken\nCook in tandoor or grill\nPrepare tomato gravy\nAdd butter and cream\nCombine chicken with gravy\nGarnish with cilantro',
        'calories': 350,
        'protein': 35.0,
        'fat': 18.0,
        'carbs': 12.0,
        'dietary_type': 'none',
        'is_shared': True,
    },
    {
        'title': 'Palak Paneer',
        'description': 'Soft paneer cheese cubes in a creamy spinach sauce, a nutritious Indian vegetarian delight.',
        'ingredients': 'Paneer (Indian cheese)\nSpinach\nCream\nOnions\nGarlic\nGinger\nTomatoes\nGaram masala\nCumin seeds',
        'instructions': 'Blanch and puree spinach\nCut paneer into cubes\nPrepare onion-tomato base\nAdd spinach puree\nStir in cream\nAdd paneer\nCook until ready',
        'calories': 280,
        'protein': 18.0,
        'fat': 20.0,
        'carbs': 10.0,
        'dietary_type': 'vegetarian',
        'is_shared': True,
    },
    {
        'title': 'Bihari Litti-Chokha',
        'description': 'Traditional Bihari stuffed bread with roasted vegetable curry, a wholesome and flavorful meal.',
        'ingredients': 'Wheat flour\nRoasted gram flour\nSpices\nAloo (potato)\nBrinjal (eggplant)\nTomato\nOnion\nGinger\nGarlic\nChilies',
        'instructions': 'Prepare dough\nMake filling with roasted gram and spices\nStuff and shape litti\nBake or roast\nPrepare chokha by roasting vegetables\nMash and season',
        'calories': 320,
        'protein': 10.0,
        'fat': 8.0,
        'carbs': 52.0,
        'dietary_type': 'vegetarian',
        'is_shared': True,
    },
    {
        'title': 'Tandoori Chicken',
        'description': 'Marinated and roasted chicken with aromatic tandoori spices, a popular Indian appetizer.',
        'ingredients': 'Chicken drumsticks\nYogurt\nTandoori masala\nLemon juice\nGarlic paste\nGinger paste\nChilies\nCilantro',
        'instructions': 'Marinate chicken in yogurt and spices for 2-4 hours\nArrange on skewers\nCook in tandoor or oven at 425F\nBaste with butter halfway\nCook until charred and cooked through',
        'calories': 200,
        'protein': 28.0,
        'fat': 8.0,
        'carbs': 4.0,
        'dietary_type': 'none',
        'is_shared': True,
    },
    {
        'title': 'Chana Masala',
        'description': 'Spiced chickpea curry, a hearty and protein-rich vegetarian Indian dish.',
        'ingredients': 'Chickpeas\nOnions\nTomatoes\nGinger-garlic paste\nGreen chilies\nCumin\nCoriander\nGaram masala\nTurmeric\nCilantro',
        'instructions': 'Soak and cook chickpeas or use canned\nSauté onions until golden\nAdd ginger-garlic paste\nAdd tomatoes and spices\nAdd chickpeas\nCook for 20 minutes\nGarnish with cilantro',
        'calories': 220,
        'protein': 12.0,
        'fat': 4.0,
        'carbs': 35.0,
        'dietary_type': 'vegan',
        'is_shared': True,
    },
    {
        'title': 'Bihari Sattu Paratha',
        'description': 'Stuffed flatbread with roasted gram flour, a traditional Bihari breakfast favorite.',
        'ingredients': 'Wheat flour\nSattu (roasted gram flour)\nOnions\nGreen chilies\nGinger\nSpices\nGhee\nSalt',
        'instructions': 'Prepare dough with wheat flour\nMake filling with sattu, onions, and spices\nRoll out dough, fill, and seal\nRoll into paratha\nCook on griddle with ghee until golden',
        'calories': 310,
        'protein': 12.0,
        'fat': 12.0,
        'carbs': 40.0,
        'dietary_type': 'vegetarian',
        'is_shared': True,
    },
    {
        'title': 'Aloo Gobi (Potato & Cauliflower)',
        'description': 'Crispy fried potato and cauliflower with aromatic spices, a popular Indian side dish.',
        'ingredients': 'Potatoes\nCauliflower\nOnions\nTomatoes\nGinger-garlic paste\nTurmeric\nCumin\nCoriander\nGreen chilies\nCilantro',
        'instructions': 'Cut potatoes and cauliflower into florets\nHeat oil in pan\nAdd cumin seeds\nAdd onions and cook until golden\nAdd ginger-garlic paste\nAdd tomatoes and spices\nAdd vegetables\nCook until tender',
        'calories': 180,
        'protein': 5.0,
        'fat': 8.0,
        'carbs': 25.0,
        'dietary_type': 'vegan',
        'is_shared': True,
    },
    {
        'title': 'Bihari Dal-Puri',
        'description': 'Spiced lentil curry with puffed fried bread, a classic Bihari breakfast combination.',
        'ingredients': 'Masoor dal (red lentils)\nAll-purpose flour\nOnions\nTomatoes\nSpices\nCumin\nTurmeric\nGinger\nGarlic\nOil',
        'instructions': 'Cook lentils until soft\nPrepare dough for puri\nFry puri until puffed and golden\nSauté onions\nAdd spices and tomatoes\nAdd cooked lentils\nCook until combined',
        'calories': 300,
        'protein': 12.0,
        'fat': 10.0,
        'carbs': 42.0,
        'dietary_type': 'vegetarian',
        'is_shared': True,
    },
    {
        'title': 'Rogan Josh',
        'description': 'Aromatic lamb curry with yogurt and spices, a Kashmiri-inspired Indian classic.',
        'ingredients': 'Lamb meat\nYogurt\nOnions\nTomatoes\nGinger-garlic paste\nCumin\nCoriander\nCardamom\nCinnamon\nBay leaf\nCloves',
        'instructions': 'Cut lamb into cubes\nMarinate in yogurt and spices for 30 minutes\nSauté onions until golden\nAdd ginger-garlic paste\nAdd yogurt and marinated lamb\nAdd tomatoes and spices\nCook until tender',
        'calories': 380,
        'protein': 42.0,
        'fat': 20.0,
        'carbs': 8.0,
        'dietary_type': 'none',
        'is_shared': True,
    },
    {
        'title': 'Khichdi',
        'description': 'Comfort food rice and lentil dish, often served with ghee and vegetables.',
        'ingredients': 'Basmati rice\nMoong dal\nGhee\nOnions\nGinger\nGreen chilies\nCumin seeds\nTurmeric\nCilantro',
        'instructions': 'Wash rice and dal\nHeat ghee in pot\nAdd cumin seeds\nAdd onions and cook until golden\nAdd ginger and chilies\nAdd rice and dal\nAdd water and turmeric\nCook until everything is soft and mushy',
        'calories': 250,
        'protein': 8.0,
        'fat': 6.0,
        'carbs': 44.0,
        'dietary_type': 'vegetarian',
        'is_shared': True,
    },
]

# Create recipes
for recipe_data in indian_recipes:
    recipe, created = Recipe.objects.get_or_create(
        user=demo_user,
        title=recipe_data['title'],
        defaults=recipe_data
    )
    if created:
        print(f"✓ Created: {recipe.title}")
    else:
        print(f"→ Already exists: {recipe.title}")

print(f"\n✓ Seeding complete! {len(indian_recipes)} Indian & Bihari recipes added.")
