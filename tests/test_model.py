import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from army.models import Base, WeaponAbility


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)


def test_weapon_ability_creation(db_session):
    ability = WeaponAbility(
        name="Crit Auto-Wound", description="Critical hits automatically wound."
    )
    db_session.add(ability)
    db_session.commit()

    result = db_session.query(WeaponAbility).filter_by(name="Crit Auto-Wound").first()
    assert result is not None
    assert result.description == "Critical hits automatically wound."
    assert result.id is not None  # autoincrement assigned


def test_weapon_ability_repr(db_session):
    ability = WeaponAbility(
        name="Crit Auto-Wound", description="Critical hits automatically wound."
    )
    assert repr(ability) == "Crit Auto-Wound: Critical hits automatically wound."


def test_weapon_ability_name_unique(db_session):
    db_session.add(WeaponAbility(name="Crit Auto-Wound", description="First"))
    db_session.commit()

    db_session.add(WeaponAbility(name="Crit Auto-Wound", description="Duplicate"))
    with pytest.raises(Exception):  # IntegrityError
        db_session.commit()
