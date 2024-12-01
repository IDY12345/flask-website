from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Job {self.title}>"


# Create the database tables
with app.app_context():
    db.create_all()

    if Job.query.count() == 0:
        sample_jobs = [
            {"title": "Data Analyst", "location": "Bengaluru,             India", "salary": "Rs. 10,00,000"},
            {"title": "Data Scientist", "location": "Delhi,                 India", "salary": "Rs. 15,00,000"},
            {"title": "Frontend Engineer", "location":                     "Remote", "salary": "Rs. 12,00,000"},
            {"title": "Backend Engineer", "location": "San                 Francisco, USA", "salary": "$120,000"}
        ]
        for job in sample_jobs:
            new_job = Job()  # Create an empty Job instance
            new_job.title = job["title"]  # Set attributes directly
            new_job.location = job["location"]
            new_job.salary = job.get("salary")
            db.session.add(new_job)
            db.session.commit()
            db.session.add(new_job)
        db.session.commit()



@app.route("/")
def hello_world():
    jobs = Job.query.all() 
    return render_template('home.html', jobs=jobs)

@app.route("/api/jobs", methods=["GET", "POST"])
def list_jobs():
    if request.method == "POST":
        # Add a new job
        data = request.get_json()
        new_job = Job()
        new_job.title = data.get('title')
        new_job.location = data.get('location')
        new_job.salary = data.get('salary')
        db.session.add(new_job)
        db.session.commit()
        return jsonify({"message": "Job added                               successfully!"}), 201

    # Retrieve all jobs
    jobs = Job.query.all()
    result = [{"id": job.id, "title": job.title, "location":job.location, "salary": job.salary} for job in jobs]
    return jsonify(result)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
