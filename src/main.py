from sqlalchemy.orm import Session

from army.db import SessionLocal
from army.models import WeaponProfile


def main():
    session: Session = SessionLocal()

    rusty_weapons = (
        session.query(WeaponProfile).where(WeaponProfile.name == "Rusty Weapons").one()
    )

    print(f"{rusty_weapons.name}")
    print(f"{rusty_weapons.attack}")


if __name__ == "__main__":
    main()
