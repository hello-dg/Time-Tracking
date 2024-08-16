from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from datetime import date, time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# will need foreign keys later to link up to an employee db, client db, project db, etc
class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client: Mapped[str] = mapped_column(String(250), nullable=False)
    task: Mapped[str] = mapped_column(String(250), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # client = db.Column(db.String(200), nullable=False)  # add index latter
    # department = db.Column(db.String(200), nullable=False)
    # project = db.Column(db.String(200), nullable=False)
    # activity = db.Column(db.String(200), nullable=False)
    # task = db.Column(db.String(200), nullable=False)
    # done = db.Column(db.Boolean, default=False)
    # tags = db.Column(db.String(200), nullable=False)
    # billable = db.Column(db.Boolean, default=False)
    # bill_rate = db.Column(db.Integer, default=0)
    # bill_frequency = db.Column(db.String(100), nullable=False, default="Hourly")
    # bill_total = db.Column(db.Integer, default=0)
    # employee = db.Column(db.String(100), nullable=False, default="Bob Jones", index=True)
    # group = db.Column(db.String(100), nullable=False, default="Accounting")
    # role = db.Column(db.String(100), nullable=False, default="Bookkeeper")
    # pay_type = db.Column(db.String(100), nullable=False, default="Regular")
    # created_Date = db.Column(db.Date, nullable=False, default=date.today)
    # start_Date = db.Column(db.Date, nullable=False)
    # start_Time = db.Column(db.Time, nullable=False, default=time(0, 0))
    # end_Date = db.Column(db.Date, nullable=False)
    # end_Time = db.Column(db.Time, nullable=False, default=time(23, 59))
    # duration_hours = db.Column(db.Time, nullable=False, default=time(23, 59))
    # duration_decimal = db.Column(db.Numeric(4, 2), nullable=False, default=23.98)

    def __repr__(self):
        return f'<task {self.task}>'


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    client_data = request.form.get('client')
    task_data = request.form.get('task')
    if task_data:
        new_task = Task(client=client_data, task=task_data, done=False)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/check/<int:task_id>')
def check_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)