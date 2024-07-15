from models import Person, DriverLicense, Car
from models.engine import Session, Base, engine
import csv


def load():
    # Activate DB and create tables
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()

    new_items = []

    # Add persons
    with open("ch0/data/driver_license.tsv") as f:
        LICENSES = csv.reader(f, delimiter="\t", quotechar='"')
        for l in LICENSES:
            next_item = DriverLicense(
                id=l[0],
                age=l[1],
                height=l[2],
                eye_color=l[3],
                hair_color=l[4],
                gender=l[5],
            )
            new_items.append(next_item)
        session.flush()

        for l in LICENSES:
            next_item = Car(
                # id=l[0],
                registration_plate=l[7],
                manufacturer=l[8],
                model=l[9],
                driver_license_id=l[0],
            )
            new_items.append(next_item)
        session.flush()

    # Add persons
    with open("ch0/data/person.tsv") as f:
        PERSONS = csv.reader(f, delimiter="\t", quotechar='"')
        for p in PERSONS:
            next_item = Person(
                id=p[0],
                name=p[1],
                passport=p[2],
                address_number=p[3],
                address_street=p[4],
                driver_license_id=p[5],
            )
            new_items.append(next_item)
        session.flush()

    session.add_all(new_items)
    session.commit()


if __name__ == '__main__':
    load()
