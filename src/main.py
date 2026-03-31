from sqlalchemy.orm import Session

from army.db import SessionLocal
from army.models import WeaponAbility, WeaponProfile


def main():
    session: Session = SessionLocal()
    weapon_profiles = session.query(WeaponProfile)

    for wp in weapon_profiles:
        print(wp)

if __name__ == "__main__":
    main()
