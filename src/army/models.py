from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class WeaponAbility(Base):
    __tablename__ = "WeaponAbility"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"{self.name}: {self.description}"


class WeaponType(Base):
    __tablename__ = "WeaponType"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    value: Mapped[str] = mapped_column(String, unique=True, nullable=False)


weapon_profile_abilities = Table(
    "WeaponProfileAbility",  # must match existing table name
    Base.metadata,
    Column("weapon_profile_id", ForeignKey("WeaponProfile.id"), primary_key=True),
    Column("weapon_ability_id", ForeignKey("WeaponAbility.id"), primary_key=True),
)


class WeaponProfile(Base):
    __tablename__ = "WeaponProfile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    weapon_abilities: Mapped[list["WeaponAbility"]] = relationship(
        secondary=weapon_profile_abilities
    )
    attack: Mapped[int] = mapped_column(Integer)
    hit: Mapped[int] = mapped_column(Integer)
    wound: Mapped[int] = mapped_column(Integer)
    rend: Mapped[int] = mapped_column(Integer)
    damage: Mapped[int] = mapped_column(Integer)
    weapon_type_id: Mapped[int] = mapped_column(
        ForeignKey("WeaponType.id"), nullable=False
    )
    weapon_type: Mapped["WeaponType"] = relationship()
    range: Mapped[str] = mapped_column(String)

    def __eq__(self, other: WeaponProfile) -> bool:  # type:ignore
        return (
            self.name == other.name
            and self.weapon_abilities == other.weapon_abilities
            and self.attack == other.attack
            and self.hit == other.hit
            and self.wound == other.wound
            and self.rend == other.rend
            and self.damage == other.damage
            and self.weapon_type == other.weapon_type
            and self.range == other.range
        )

    def __repr__(self) -> str:
        return f"{self.name}"


class BattleProfile(Base):
    __tablename__ = "BattleProfile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unit_size: Mapped[int] = mapped_column(Integer)
    points: Mapped[int] = mapped_column(Integer)
    can_be_reinforced: Mapped[int] = mapped_column(Integer)
    base_size: Mapped[str] = mapped_column(String)


class Warscroll(Base):
    __tablename__ = "Warscroll"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    move: Mapped[int] = mapped_column(Integer)
    save: Mapped[int] = mapped_column(Integer)
    control: Mapped[int] = mapped_column(Integer)
    health: Mapped[int] = mapped_column(Integer)
    battle_profile_id: Mapped[int] = mapped_column(ForeignKey("BattleProfile.id"))
    url: Mapped[str] = mapped_column(String)
    lore: Mapped[str] = mapped_column(String)
