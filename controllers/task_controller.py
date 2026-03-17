from database.db import SessionLocal
from models.task import Task
from models.assignment import Assignment
from sqlalchemy import and_
from datetime import datetime


class TaskController:
    @staticmethod
    def add_task(title, description, deadline, required_volunteers):
        db = SessionLocal()
        try:
            if not title or len(title.strip()) == 0:
                return False, "Название задачи обязательно"
            if required_volunteers < 1:
                return False, "Требуется хотя бы один волонтер"

            new_task = Task(
                title=title,
                description=description,
                deadline=deadline,
                required_volunteers=required_volunteers
            )
            db.add(new_task)
            db.commit()
            db.refresh(new_task)
            return True, "Задача добавлена"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()

    @staticmethod
    def get_all_tasks():
        db = SessionLocal()
        try:
            tasks = db.query(Task).all()
            return [t for t in tasks]
        finally:
            db.close()

    @staticmethod
    def assign_volunteer_to_task(volunteer_id, task_id):
        db = SessionLocal()
        try:
            existing = db.query(Assignment).filter(
                and_(Assignment.volunteer_id == volunteer_id, Assignment.task_id == task_id)
            ).first()
            if existing:
                return False, "Волонтер уже назначен на эту задачу"

            assignment = Assignment(
                volunteer_id=volunteer_id,
                task_id=task_id,
                hours_worked=0.0
            )
            db.add(assignment)
            db.commit()
            return True, "Волонтер назначен"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()

    @staticmethod
    def record_hours(volunteer_id, task_id, hours):
        if hours <= 0:
            return False, "Часы должны быть больше 0"

        db = SessionLocal()
        try:
            assignment = db.query(Assignment).filter(
                and_(Assignment.volunteer_id == volunteer_id, Assignment.task_id == task_id)
            ).first()
            if not assignment:
                return False, "Назначение не найдено"

            assignment.hours_worked += hours
            db.commit()
            return True, "Часы обновлены"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()

    @staticmethod
    def get_tasks_by_volunteer(volunteer_id):
        db = SessionLocal()
        try:
            result = db.query(Task, Assignment.hours_worked).join(Assignment).filter(
                Assignment.volunteer_id == volunteer_id
            ).all()
            return [(t.id, t.title, t.description, t.deadline, hw) for t, hw in result]
        finally:
            db.close()