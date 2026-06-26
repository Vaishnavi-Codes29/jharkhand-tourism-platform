#!/usr/bin/env python3
"""Seed the database with test homestays and destinations"""

import sys
from datetime import datetime
from models import db, User, Destination, Service, Booking
from app import app

def seed_db():
    """Add test data to database"""
    with app.app_context():
        # Drop all tables and recreate from scratch
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables from current schema...")
        db.create_all()
        
        # Check existing data
        dest_count = Destination.query.count()
        service_count = Service.query.count()
        user_count = User.query.count()
        
        print(f"Current state: {dest_count} destinations, {service_count} services, {user_count} users")
        
        if service_count > 0:
            print("✓ Services already exist. Skipping seed.")
            return
        
        # Create a provider user
        provider = User.query.filter_by(email='provider@local.test').first()
        if not provider:
            provider = User(name='Provider User', email='provider@local.test', role='homestay_owner')
            provider.set_password('provider')
            db.session.add(provider)
            db.session.commit()
            print("✓ Created provider user")
        
        # Create destinations (tribal categories)
        destinations = [
            Destination(name='Santhal Tribal Land', category='Santhal', location='Sahebganj', 
                       description='Santhal tribal homeland', latitude=24.2, longitude=87.5),
            Destination(name='Munda Territory', category='Munda', location='Khunti',
                       description='Home of the Munda tribe', latitude=23.3, longitude=84.8),
            Destination(name='Oraon Region', category='Oraon', location='Gumla',
                       description='Oraon tribal region', latitude=23.2, longitude=84.4),
            Destination(name='Ho Lands', category='Ho', location='West Singhbhum',
                       description='Ho tribe homeland', latitude=22.8, longitude=84.3),
            Destination(name='Kharia Mountain', category='Kharia', location='Simdega',
                       description='High altitude Kharia stay', latitude=23.0, longitude=84.0),
            Destination(name='Birhor Forest', category='Birhor', location='Hazaribagh',
                       description='Forest home of Birhor tribe', latitude=23.8, longitude=84.7),
        ]
        db.session.add_all(destinations)
        db.session.commit()
        print(f"✓ Created {len(destinations)} destinations")
        
        # Create services (homestays)
        services_data = [
            {'dest_id': 1, 'name': 'Santhal Forest Hut', 'price': 800, 'capacity': 4, 'tribe': 'Santhal'},
            {'dest_id': 2, 'name': 'Munda Village Home', 'price': 650, 'capacity': 3, 'tribe': 'Munda'},
            {'dest_id': 3, 'name': 'Oraon Eco Cottage', 'price': 950, 'capacity': 2, 'tribe': 'Oraon'},
            {'dest_id': 4, 'name': 'Ho Tribe River Camp', 'price': 700, 'capacity': 4, 'tribe': 'Ho'},
            {'dest_id': 5, 'name': 'Kharia Mountain Stay', 'price': 750, 'capacity': 2, 'tribe': 'Kharia'},
            {'dest_id': 6, 'name': 'Birhor Forest Camp', 'price': 600, 'capacity': 5, 'tribe': 'Birhor'},
        ]
        
        for s in services_data:
            service = Service(
                provider_id=provider.id,
                destination_id=s['dest_id'],
                name=s['name'],
                service_type='homestay',
                price_per_day=s['price'],
                capacity=s['capacity'],
                availability=True,
                description=f"Authentic {s['tribe']} homestay experience",
                rating=4.5
            )
            db.session.add(service)
        
        db.session.commit()
        print(f"✓ Created {len(services_data)} services (homestays)")
        
        # Verify
        print(f"\n✓ Database seeded successfully!")
        print(f"  - Destinations: {Destination.query.count()}")
        print(f"  - Services: {Service.query.count()}")
        print(f"  - Users: {User.query.count()}")

if __name__ == '__main__':
    seed_db()
