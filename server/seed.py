#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from app import app
from models import db, Zookeeper, Animal, Enclosure

fake = Faker()

with app.app_context():
    # Clear existing data
    Animal.query.delete()
    Zookeeper.query.delete()
    Enclosure.query.delete()

    # Seed Zookeepers
    zookeepers = [
        Zookeeper(
            name=fake.name(),
            birthday=fake.date_between(start_date='-70y', end_date='-18y')
        )
        for _ in range(25)
    ]
    db.session.add_all(zookeepers)

    # Seed Enclosures
    environments = ['Desert', 'Pond', 'Ocean', 'Field', 'Trees', 'Cave', 'Cage']
    enclosures = [
        Enclosure(
            environment=rc(environments),
            open_to_visitors=rc([True, False])
        )
        for _ in range(25)
    ]
    db.session.add_all(enclosures)

    # Seed Animals
    species = ['Lion', 'Tiger', 'Bear', 'Hippo', 'Rhino', 'Elephant', 'Ostrich', 'Snake', 'Monkey']
    animals = []
    used_names = set()

    for _ in range(200):
        name = fake.first_name()
        while name in used_names:
            name = fake.first_name()
        used_names.add(name)
        animals.append(
            Animal(
                name=name,
                species=rc(species),
                zookeeper=rc(zookeepers),
                enclosure=rc(enclosures)
            )
        )

    db.session.add_all(animals)

    # Commit all changes
    db.session.commit()

    print("Database seeded successfully!")
