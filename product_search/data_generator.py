from faker import Faker
import random, string

fake = Faker()

def generate_random_products():
    products = []
    for _ in range(400):
        products.append({'product_id': ''.join(random.choices(string.ascii_letters, k=10)),
                         'name': fake.word(),
                         'description': fake.sentence(nb_words=10),
                         'price': round(random.uniform(100, 50000), 2),
                         'available_stock': random.randint(100, 5000)})
    return products