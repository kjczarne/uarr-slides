from dataclasses import dataclass


@dataclass
class Mom:
    name: str
    age: int
    weight: float


def eat_my_moms_fat(mom: Mom, how_much: float) -> None:
    mom.weight -= how_much


def eat_my_moms_fat_pure(mom: Mom, how_much: float) -> Mom:
    return Mom(mom.name, mom.age, mom.weight - how_much)


def eat_my_moms_fat_semi_pure(mom: Mom, how_much: float) -> Mom:
    mom.weight -= how_much
    return mom


def main():
    mom = Mom(name="Alice", age=42, weight=70.0)
    mom = eat_my_moms_fat_pure(mom, 5.0)
    print(mom)


if __name__ == "__main__":
    main()
