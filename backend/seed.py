import random
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.application import Application

COMPANIES = ['Google', 'Microsoft', 'Apple', 'Meta', 'Amazon', 'Netflix', 'Stripe', 'Spotify', 'Twitter', 'Tesla', 'SpaceX', 'Airbnb', 'Uber', 'Lyft', 'Slack']
ROLES = ['Software Engineer', 'Frontend Engineer', 'Backend Developer', 'Full Stack Developer', 'Data Scientist', 'DevOps Engineer', 'Product Manager', 'UX Designer']
STAGES = ['APPLIED', 'SCREENING', 'INTERVIEW', 'OFFER', 'REJECTED', 'WITHDRAWN']
LOCATIONS = ['San Francisco, CA', 'New York, NY', 'Remote', 'London, UK', 'Austin, TX', 'Seattle, WA', 'Berlin, Germany']

def seed_data():
    app = create_app()
    with app.app_context():
        print("Seeding users and applications...")
        
        users = []
        for i in range(1, 4):
            # Create a user
            email = f"user{i}@example.com"
            existing_user = db.session.query(User).filter_by(email=email).first()
            if not existing_user:
                user = User(
                    email=email,
                    password_hash=generate_password_hash("password123"),
                    full_name=f"Test User {i}"
                )
                db.session.add(user)
                db.session.flush() # get user ID
                users.append(user)
                print(f"Created user: {user.email}")
            else:
                users.append(existing_user)
                print(f"User {existing_user.email} already exists")

        # Now create 10 applications for each user
        for user in users:
            existing_apps = db.session.query(Application).filter_by(user_id=user.id).count()
            apps_to_create = max(0, 10 - existing_apps)
            
            for _ in range(apps_to_create):
                applied_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 60))
                min_sal = random.randint(60, 120) * 1000
                app_obj = Application(
                    user_id=user.id,
                    company_name=random.choice(COMPANIES),
                    role_title=random.choice(ROLES),
                    job_url=f"https://careers.example.com/jobs/{random.randint(1000, 9999)}",
                    location=random.choice(LOCATIONS),
                    salary_min=min_sal,
                    salary_max=min_sal + random.randint(10, 40) * 1000,
                    stage=random.choice(STAGES),
                    applied_date=applied_date.date()
                )
                db.session.add(app_obj)
            
            if apps_to_create > 0:
                print(f"Added {apps_to_create} applications for {user.email}")

        db.session.commit()
        print("Seeding complete! You can log in with: user1@example.com / password123")

if __name__ == '__main__':
    seed_data()
