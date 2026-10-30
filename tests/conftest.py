import pytest
from app import create_app
from app.extensions import db
from app.models import User, FarmerProfile
from app.utils.security import hash_password

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_farmer(app):
    user = User(
        username='test_kisan',
        password_hash=hash_password('secret123'),
        full_name='Test Kisan',
        preferred_language='kn'
    )
    db.session.add(user)
    db.session.flush()

    profile = FarmerProfile(
        user_id=user.id,
        district='Mandya',
        total_land_acres=2.5,
        farmer_category='SMALL',
        has_aadhaar=True,
        has_pm_kisan=True
    )
    db.session.add(profile)
    db.session.commit()
    return user

