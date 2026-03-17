from database.db import SessionLocal
from models.volunteer import Volunteer


class VolunteerController:
    @staticmethod
    def add_volunteer(name, age, phone, specialization):
        db = SessionLocal()
        try:
            if not name or len(name.strip()) == 0:
                return False, "Имя волонтера обязательно"

            new_volunteer = Volunteer(
                name=name,
                age=age,
                phone=phone,
                specialization=specialization
            )
            db.add(new_volunteer)
            db.commit()
            db.refresh(new_volunteer)
            return True, "Волонтер добавлен"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()

    @staticmethod
    def get_all_volunteers():
        db = SessionLocal()
        try:
            volunteers = db.query(Volunteer).all()
            return [v for v in volunteers]
        finally:
            db.close()

    @staticmethod
    def search_volunteers(query):
        db = SessionLocal()
        try:
            result = db.query(Volunteer).filter(
                (Volunteer.name.contains(query)) |
                (Volunteer.specialization.contains(query))
            ).all()
            return result
        finally:
            db.close()

    @staticmethod
    def update_volunteer(vol_id, name, age, phone, specialization):
        db = SessionLocal()
        try:
            volunteer = db.query(Volunteer).filter(Volunteer.id == vol_id).first()
            if not volunteer:
                return False, "Волонтер не найден"

            volunteer.name = name
            volunteer.age = age
            volunteer.phone = phone
            volunteer.specialization = specialization

            db.commit()
            return True, "Данные обновлены"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()

    @staticmethod
    def delete_volunteer(vol_id):
        db = SessionLocal()
        try:
            volunteer = db.query(Volunteer).filter(Volunteer.id == vol_id).first()
            if not volunteer:
                return False, "Волонтер не найден"

            db.delete(volunteer)
            db.commit()
            return True, "Волонтер удален"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()