from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlite3 import Date
from datetime import date, time, datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# will need foreign keys later to link up to an employee db, client db, project db, etc
class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee: Mapped[str] = mapped_column(String(200), nullable=True, default="Bob Bookkeeper")
    group: Mapped[str] = mapped_column(String(200), nullable=True, default="Accounting")
    role: Mapped[str] = mapped_column(String(200), nullable=True, default="Bookkeeper")
    pay_type: Mapped[str] = mapped_column(String(200), nullable=True, default="Regular")
    department: Mapped[str] = mapped_column(String(200), nullable=True, default="Department")
    project: Mapped[str] = mapped_column(String(200), nullable=False)
    activity: Mapped[str] = mapped_column(String(200), nullable=True, default="Activity")
    client: Mapped[str] = mapped_column(String(200), nullable=False)
    task: Mapped[str] = mapped_column(String(200), nullable=False)
    tags: Mapped[str] = mapped_column(String(200), nullable=True)
    billable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    bill_rate: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    bill_frequency: Mapped[str] = mapped_column(String(200), nullable=True, default="Bill Frequency")
    bill_total: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    created_date: Mapped[str] = mapped_column(String(25), nullable=True)
    start_date: Mapped[str] = mapped_column(String(25), nullable=False)
    start_time: Mapped[str] = mapped_column(String(25), nullable=False)
    end_date: Mapped[str] = mapped_column(String(25), nullable=True)
    end_time: Mapped[str] = mapped_column(String(25), nullable=False)
    duration_hours: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    duration_decimal: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<task {self.task}>'


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M')
    tasks = Task.query.all()
    print(current_time)
    return render_template('index.html', tasks=tasks, today=today, time=current_time)


@app.route('/add', methods=['POST'])
def add_task():
    client_data = request.form.get('client')
    project_data = request.form.get('project')
    task_data = request.form.get('task')
    tag_data = request.form.get('tags')
    billable_data = request.form.get('billable')
    billable_boolean = False
    if billable_data == 'on':
        billable_boolean = True
    start_date_data = str(request.form.get('start_date'))
    start_time_data = str(request.form.get('start_time'))
    end_time_data = str(request.form.get('end_time'))
    if project_data:
        new_task = Task(client=client_data, project=project_data, task=task_data, tags=tag_data, billable=billable_boolean, start_date=start_date_data, start_time=start_time_data, end_time=end_time_data, done=False)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))


# @app.route('/check/<int:task_id>')
# def check_task(task_id):
#     task = Task.query.get_or_404(task_id)
#     task.done = not task.done
#     db.session.commit()
#     return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)