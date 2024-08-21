from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlite3 import Date
from datetime import date, time, datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Lists for testing Client, Project, and Activity dropdown
Client_List = ["No Client", "Multiple Clients", "Marvel Entertainment", "Reynolds, Ryan & Blake", "Wilson, Wade"]
Project_List = ["Tax Preparation", "Monthly Bookkeeping", "Administrative"]
Activity_List = ["Tax Entries", "2024 Transactions", "Filing"]

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
    client: Mapped[str] = mapped_column(String(200), nullable=True)
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
    # Check if previously selected values
    selected_client = request.args.get('selected_client')
    selected_project = request.args.get('selected_project')
    selected_activity = request.args.get('selected_activity')
    selected_tags = ''
    selected_billable = ''
    selected_task = ''
    selected_start_date = ''
    selected_start_time = ''
    selected_end_time = ''

    today = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M')
    tags_data = request.form.get('tags')
    tasks = Task.query.order_by(Task.start_date.desc(), Task.start_time.desc()).all()
    return render_template('index.html', selected_client=selected_client, selected_project=selected_project, selected_activity=selected_activity, clients=Client_List, projects=Project_List, activities=Activity_List, tasks=tasks, today=today, time=current_time, tags=tags_data, datetime=datetime, str=str)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    client_data = request.form.get('client')
    project_data = request.form.get('project')
    activity_data = request.form.get('activity')
    task_data = request.form.get('task')
    tag_data = ','.join(request.form.getlist('tags[]'))
    billable_data = request.form.get('billable')
    billable_boolean = billable_data == 'on'
    start_date_data = request.form.get('start_date')
    start_time_data = str(request.form.get('start_time'))
    end_time_data = str(request.form.get('end_time'))

    if not client_data:
        flash("A client is required. Please try again.", "warning")
        return redirect(url_for('index', selected_project=project_data, selected_activity=activity_data, selected_task=task_data, selected_tags=tag_data, selected_billable=billable_data, selected_start_date=start_date_data, selected_start_time=start_time_data, selected_end_time=end_time_data))
    elif not project_data:
        flash("A project is required. Please try again.", "warning")
        return redirect(url_for('index', selected_client=client_data, selected_activity=activity_data, selected_task=task_data, selected_tags=tag_data, selected_billable=billable_data, selected_start_date=start_date_data, selected_start_time=start_time_data, selected_end_time=end_time_data))
    elif not activity_data:
        flash("An activity is required. Please try again.", "warning")
        return redirect(url_for('index', selected_client=client_data, selected_project=project_data, selected_task=task_data, selected_tags=tag_data, selected_billable=billable_data, selected_start_date=start_date_data, selected_start_time=start_time_data, selected_end_time=end_time_data))
    elif not start_date_data:
        return redirect(url_for('index', selected_client=client_data, selected_project=project_data, selected_activity=activity_data, selected_task=task_data, selected_tags=tag_data, selected_billable=billable_data, selected_start_time=start_time_data, selected_end_time=end_time_data))
    elif not start_time_data:
        return redirect(url_for('index', selected_client=client_data, selected_project=project_data, selected_activity=activity_data, selected_task=task_data, selected_tags=tag_data, selected_billable=billable_data, selected_start_date=start_date_data, selected_end_time=end_time_data))
    elif not end_time_data:
        return redirect(
            url_for('index', selected_client=client_data, selected_project=project_data, selected_activity=activity_data, selected_task=task_data,
                    selected_tags=tag_data, selected_billable=billable_data, selected_start_date=start_date_data,
                    selected_start_time=start_time_data))
    else:
        new_task = Task(client=client_data,
                        project=project_data,
                        activity=activity_data,
                        task=task_data,
                        tags=tag_data,
                        billable=billable_boolean,
                        start_date=start_date_data,
                        start_time=start_time_data,
                        end_time=end_time_data,
                        done=False
                        )
        db.session.add(new_task)
        db.session.commit()
    print(client_data)
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