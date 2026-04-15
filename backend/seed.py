# backend/seed.py
import random
import sys
from faker import Faker
from app import create_app
from app.extensions import db
from app.models import User, Project, Comment, Milestone, CollaborationRequest
from app.services.auth_service import AuthService

fake = Faker()

app = create_app()
app.app_context().push()

def clear_data():
    print("⚠️ Dropping all tables...")
    db.drop_all()
    db.create_all()
    print("✅ Database tables recreated.")

def create_users(count=8):
    users = []
    for i in range(count):
        email = fake.unique.email()
        username = fake.unique.user_name()
        password = "password123"
        user, error = AuthService.register_user(email, username, password)
        if error:
            print(f"❌ Failed to create user {username}: {error}")
            continue
        user.bio = fake.paragraph(nb_sentences=2)
        user.location = fake.city()
        user.avatar_url = f"https://i.pravatar.cc/150?u={user.id}"
        db.session.add(user)
        users.append(user)
        print(f"   Created user: {username} ({email})")
    db.session.commit()
    print(f"✅ Created {len(users)} users.")
    return users

def create_projects(users, count=20):
    projects = []
    stages = ["planning", "in_progress", "completed"]
    for _ in range(count):
        owner = random.choice(users)
        project = Project(
            title=fake.sentence(nb_words=6),
            description=fake.paragraph(nb_sentences=5),
            user_id=owner.id,
            stage=random.choice(stages),
            support_needed=fake.sentence() if random.random() > 0.5 else None
        )
        db.session.add(project)
        projects.append(project)
    db.session.commit()
    print(f"✅ Created {len(projects)} projects.")
    return projects

def create_milestones(projects):
    count = 0
    for project in projects:
        for _ in range(random.randint(0, 5)):
            milestone = Milestone(
                title=fake.sentence(nb_words=4),
                description=fake.sentence() if random.random() > 0.3 else None,
                project_id=project.id
            )
            milestone.completed = random.random() > 0.7  # Set after creation
            db.session.add(milestone)
            count += 1
    db.session.commit()
    print(f"✅ Created {count} milestones.")

def create_comments(users, projects):
    count = 0
    for project in projects:
        for _ in range(random.randint(0, 8)):
            author = random.choice(users)
            comment = Comment(
                content=fake.paragraph(nb_sentences=2),
                user_id=author.id,
                project_id=project.id
            )
            db.session.add(comment)
            count += 1
    db.session.commit()
    print(f"✅ Created {count} comments.")

def create_likes(users, projects):
    count = 0
    for project in projects:
        likers = random.sample(users, k=random.randint(0, len(users)))
        for user in likers:
            if not project.is_liked_by(user):
                project.liked_by.append(user)
                count += 1
    db.session.commit()
    print(f"✅ Created {count} likes.")

def create_collaboration_requests(users, projects):
    count = 0
    for project in projects:
        possible_requesters = [u for u in users if u.id != project.user_id]
        for _ in range(random.randint(0, 2)):
            if not possible_requesters:
                continue
            requester = random.choice(possible_requesters)
            existing = CollaborationRequest.query.filter_by(
                project_id=project.id, requester_id=requester.id, status="pending"
            ).first()
            if existing:
                continue
            req = CollaborationRequest(
                project_id=project.id,
                requester_id=requester.id,
                message=fake.sentence() if random.random() > 0.5 else None
            )
            db.session.add(req)
            count += 1
    db.session.commit()
    print(f"✅ Created {count} collaboration requests.")

if __name__ == "__main__":
    print("\n🚀 Starting database seed...")
    print(f"📁 Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    confirm = input("⚠️ This will DELETE ALL EXISTING DATA. Continue? (yes/no): ")
    if confirm.lower() != "yes":
        print("Aborted.")
        sys.exit(0)

    clear_data()
    users = create_users(8)
    projects = create_projects(users, 20)
    create_milestones(projects)
    create_comments(users, projects)
    create_likes(users, projects)
    create_collaboration_requests(users, projects)

    print("\n🎉 Seeding complete! You can now log in with any user using password: password123")