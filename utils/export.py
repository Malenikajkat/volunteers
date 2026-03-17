import pandas as pd
from database.db import SessionLocal
from models.volunteer import Volunteer
from models.task import Task
from models.assignment import Assignment
from datetime import date
import os


os.makedirs("reports", exist_ok=True)


def export_volunteer_report_to_excel(filename="reports/volunteer_report.xlsx"):
    db = SessionLocal()
    try:
        data = []
        volunteers = db.query(Volunteer).all()

        for v in volunteers:
            assignments = db.query(Assignment).filter(Assignment.volunteer_id == v.id).all()
            tasks_count = len(assignments)
            total_hours = sum((a.hours_worked or 0) for a in assignments)

            data.append({
                "Имя": v.name,
                "Специализация": v.specialization or "—",
                "Кол-во задач": tasks_count,
                "Часы": round(total_hours, 2)
            })

        df = pd.DataFrame(data)
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Активность волонтёров")
        print(f"✅ Отчёт по волонтёрам сохранён: {filename}")
    except Exception as e:
        print(f"❌ Ошибка при экспорте отчёта по волонтёрам: {e}")
    finally:
        db.close()


def export_tasks_report_to_pdf(filename="reports/tasks_report.xlsx"):
    db = SessionLocal()
    try:
        data = []
        results = db.query(Task, Volunteer, Assignment)\
            .join(Assignment, Task.id == Assignment.task_id)\
            .join(Volunteer, Volunteer.id == Assignment.volunteer_id).all()

        for task, volunteer, assignment in results:
            deadline_str = "—"
            if task.deadline:
                if isinstance(task.deadline, str):
                    deadline_str = task.deadline
                elif isinstance(task.deadline, date):
                    deadline_str = task.deadline.strftime("%d.%m.%Y")

            data.append({
                "Задача": task.title,
                "Срок": deadline_str,
                "Исполнитель": volunteer.name,
                "Часы": round(assignment.hours_worked or 0, 2)
            })

        if not data:
            data.append({
                "Задача": "Нет данных",
                "Срок": "",
                "Исполнитель": "",
                "Часы": ""
            })

        df = pd.DataFrame(data)
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Задачи и исполнители")
        print(f"✅ Сводный отчёт по задачам сохранён: {filename}")
    except Exception as e:
        print(f"❌ Ошибка при экспорте сводного отчёта: {e}")
    finally:
        db.close()