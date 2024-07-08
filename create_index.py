from opensearchpy import OpenSearch

# Connection settings
host = 'localhost'
port = 9200
auth = ('admin', 'admin')  # Default credentials, change as necessary

# Create an OpenSearch client
client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_auth=auth,
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

# Define the index name and its schema
index_name = "autocomplete"
index_settings = {
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "analyzer": "autocomplete"
      }
    }
  },
  "settings": {
    "analysis": {
      "analyzer": {
        "autocomplete": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
          ]
        }
      }
    }
  }
}

# Check if the index already exists
if not client.indices.exists(index=index_name):
    # Create index with the defined settings and mappings
    client.indices.create(index=index_name, body=index_settings)

# Documents to be indexed
documents = [
    {"id": 1, "name": "Almond"},
    {"id": 2, "name": "Anise"},
    {"id": 3, "name": "Apple"},
    {"id": 4, "name": "Apricot"},
    {"id": 5, "name": "Arrowroot"},
    {"id": 6, "name": "Artichoke"},
    {"id": 7, "name": "Asparagus"},
    {"id": 8, "name": "Avocado"},
    {"id": 9, "name": "Bamboo Shoots"},
    {"id": 10, "name": "Banana"},
    {"id": 11, "name": "Barley"},
    {"id": 12, "name": "Basil"},
    {"id": 13, "name": "Bay Leaf"},
    {"id": 14, "name": "Beef Stroganoff"},
    {"id": 15, "name": "Beetroot"},
    {"id": 16, "name": "Biryani"},
    {"id": 17, "name": "Black Pepper"},
    {"id": 18, "name": "Blackberry"},
    {"id": 19, "name": "Blueberry"},
    {"id": 20, "name": "Bok Choy"},
    {"id": 21, "name": "Brazil Nut"},
    {"id": 22, "name": "Broccoli"},
    {"id": 23, "name": "Brussels Sprout"},
    {"id": 24, "name": "Buckwheat"},
    {"id": 25, "name": "Butternut Squash"},
    {"id": 26, "name": "Cabbage"},
    {"id": 27, "name": "Caesar Salad"},
    {"id": 28, "name": "Cake"},
    {"id": 29, "name": "Cantaloupe"},
    {"id": 30, "name": "Carbonara"},
    {"id": 31, "name": "Carrot"},
    {"id": 32, "name": "Cauliflower"},
    {"id": 33, "name": "Celery"},
    {"id": 34, "name": "Cherry"},
    {"id": 35, "name": "Chickpea"},
    {"id": 36, "name": "Chili Con Carne"},
    {"id": 37, "name": "Chimichanga"},
    {"id": 38, "name": "Cilantro"},
    {"id": 39, "name": "Cinnamon"},
    {"id": 40, "name": "Clam Chowder"},
    {"id": 41, "name": "Coconut"},
    {"id": 42, "name": "Corn"},
    {"id": 43, "name": "Cucumber"},
    {"id": 44, "name": "Curry"},
    {"id": 45, "name": "Date"},
    {"id": 46, "name": "Dill"},
    {"id": 47, "name": "Dumplings"},
    {"id": 48, "name": "Eggplant"},
    {"id": 49, "name": "Enchiladas"},
    {"id": 50, "name": "Fig"},
    {"id": 51, "name": "Fish and Chips"},
    {"id": 52, "name": "French Toast"},
    {"id": 53, "name": "Fried Rice"},
    {"id": 54, "name": "Frittata"},
    {"id": 55, "name": "Garlic"},
    {"id": 56, "name": "Gazpacho"},
    {"id": 57, "name": "Ginger"},
    {"id": 58, "name": "Gnocchi"},
    {"id": 59, "name": "Grape"},
    {"id": 60, "name": "Gumbo"},
    {"id": 61, "name": "Honeydew"},
    {"id": 62, "name": "Hummus"},
    {"id": 63, "name": "Iceberg Lettuce"},
    {"id": 64, "name": "Jalapeno"},
    {"id": 65, "name": "Jambalaya"},
    {"id": 66, "name": "Kiwi"},
    {"id": 67, "name": "Kale"},
    {"id": 68, "name": "Lasagna"},
    {"id": 69, "name": "Lemon"},
    {"id": 70, "name": "Lime"},
    {"id": 71, "name": "Mango"},
    {"id": 72, "name": "Meatloaf"},
    {"id": 73, "name": "Mint"},
    {"id": 74, "name": "Mushroom"},
    {"id": 75, "name": "Nectarine"},
    {"id": 76, "name": "Noodles"},
    {"id": 77, "name": "Nutmeg"},
    {"id": 78, "name": "Olive"},
    {"id": 79, "name": "Onion"},
    {"id": 80, "name": "Orange"},
    {"id": 81, "name": "Oregano"},
    {"id": 82, "name": "Pad Thai"},
    {"id": 83, "name": "Pancakes"},
    {"id": 84, "name": "Parsnip"},
    {"id": 85, "name": "Pasta"},
    {"id": 86, "name": "Pea"},
    {"id": 87, "name": "Peach"},
    {"id": 88, "name": "Pear"},
    {"id": 89, "name": "Pecan"},
    {"id": 90, "name": "Pepperoni"},
    {"id": 91, "name": "Pesto"},
    {"id": 92, "name": "Pineapple"},
    {"id": 93, "name": "Pizza"},
    {"id": 94, "name": "Plum"},
    {"id": 95, "name": "Pomegranate"},
    {"id": 96, "name": "Pork Chop"},
    {"id": 97, "name": "Potato"},
    {"id": 98, "name": "Pudding"},
    {"id": 99, "name": "Pumpkin"},
    {"id": 100, "name": "Quiche"},
    {"id": 101, "name": "Quinoa"},
    {"id": 102, "name": "Ravioli"},
    {"id": 103, "name": "Risotto"},
    {"id": 104, "name": "Radish"},
    {"id": 105, "name": "Raspberry"},
    {"id": 106, "name": "Rhubarb"},
    {"id": 107, "name": "Rosemary"},
    {"id": 108, "name": "Salmon"},
    {"id": 109, "name": "Salsa"},
    {"id": 110, "name": "Sardines"},
    {"id": 111, "name": "Sausage"},
    {"id": 112, "name": "Scallops"},
    {"id": 113, "name": "Shallots"},
    {"id": 114, "name": "Shrimp"},
    {"id": 115, "name": "Spinach"},
    {"id": 116, "name": "Squash"},
    {"id": 117, "name": "Strawberry"},
    {"id": 118, "name": "Sweet Potato"},
    {"id": 119, "name": "Tabbouleh"},
    {"id": 120, "name": "Taco"},
    {"id": 121, "name": "Tangerine"},
    {"id": 122, "name": "Thyme"},
    {"id": 123, "name": "Tomato"},
    {"id": 124, "name": "Tortilla"},
    {"id": 125, "name": "Tuna"},
    {"id": 126, "name": "Turnip"},
    {"id": 127, "name": "Udon"},
    {"id": 128, "name": "Ugli Fruit"},
    {"id": 129, "name": "Vanilla"},
    {"id": 130, "name": "Vegetable Soup"},
    {"id": 131, "name": "Vermicelli"},
    {"id": 132, "name": "Venison"},
    {"id": 133, "name": "Walnut"},
    {"id": 134, "name": "Watercress"},
    {"id": 135, "name": "Watermelon"},
    {"id": 136, "name": "Wasabi"},
    {"id": 137, "name": "Yam"},
    {"id": 138, "name": "Yogurt"},
    {"id": 139, "name": "Zucchini"},
    {"id": 140, "name": "Ziti"}
]

# Index the documents
for doc in documents:
    response = client.index(index=index_name, body=doc, id=doc['id'])
    print(response)
