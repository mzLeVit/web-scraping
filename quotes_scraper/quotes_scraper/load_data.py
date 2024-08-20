import json
from mongoengine import connect, Document, StringField, ListField, ReferenceField

#сюди вписати власний ідентифікатор для перевірки
connect(host="your_mongodb_atlas_uri_here")


class Author(Document):
    full_name = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    text = StringField(required=True)
    author = ReferenceField(Author, required=True)
    tags = ListField(StringField())


def load_authors():
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors = json.load(file)
        for author_data in authors:
            author = Author(**author_data)
            author.save()


def load_quotes():
    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes = json.load(file)
        for quote_data in quotes:
            author_name = quote_data.pop('author')
            author = Author.objects(full_name=author_name).first()
            if author:
                quote_data['author'] = author
                quote = Quote(**quote_data)
                quote.save()

if __name__ == "__main__":
    load_authors()
    load_quotes()
    print("Дані успішно завантажено у MongoDB Atlas")
