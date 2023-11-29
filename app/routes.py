import csv
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import *
from app.forms import *
from werkzeug.urls import *
from werkzeug.utils import secure_filename
import uuid as uuid
import os


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
    # populate_data()

    course_json = [
        {
            "id": 1,
            "code": "ACCT 22400",
            "name": "Accounting for the Real World"
        },
        {
            "id": 2,
            "code": "ACCT 22500",
            "name": "Financial Accounting"
        },
        {
            "id": 3,
            "code": "ACCT 22600",
            "name": "Management Accounting"
        },
        {
            "id": 4,
            "code": "ACCT 30700",
            "name": "Commercial Law"
        },
        {
            "id": 5,
            "code": "ACCT 31500",
            "name": "Cost Analysis and Decision Making"
        },
        {
            "id": 6,
            "code": "ACCT 32000",
            "name": "Accounting Information Systems"
        },
        {
            "id": 7,
            "code": "ACCT 34500",
            "name": "Intermediate Accounting I"
        },
        {
            "id": 8,
            "code": "ACCT 34600",
            "name": "Intermediate Accounting II"
        },
        {
            "id": 9,
            "code": "ACCT 39700",
            "name": "Selected Topics in Accounting"
        },
        {
            "id": 10,
            "code": "ACCT 40200",
            "name": "Advanced Accounting"
        },
        {
            "id": 11,
            "code": "ACCT 40600",
            "name": "Auditing"
        },
        {
            "id": 12,
            "code": "ACCT 49300",
            "name": "Tax Accounting"
        },
        {
            "id": 13,
            "code": "ACCT 49400",
            "name": "Advanced Tax Accounting"
        },
        {
            "id": 14,
            "code": "ACCT 49600",
            "name": "Practicum in Tax Accounting"
        },
        {
            "id": 15,
            "code": "ACCT 49700",
            "name": "Selected Topics: Accounting"
        },
        {
            "id": 16,
            "code": "ACCT 49800",
            "name": "Internship with Academic Enhancement"
        },
        {
            "id": 17,
            "code": "ACCT 49900",
            "name": "Independent Study: Accounting"
        },
        {
            "id": 18,
            "code": "ANTH 10100",
            "name": "Anthropology of the World: Explorations in Cultural and Biologic"
        },
        {
            "id": 19,
            "code": "ANTH 10300",
            "name": "Biological Anthropology"
        },
        {
            "id": 20,
            "code": "ANTH 10400",
            "name": "Cultural Anthropology"
        },
        {
            "id": 21,
            "code": "ANTH 10700",
            "name": "World Archaeology"
        },
        {
            "id": 22,
            "code": "ANTH 11500",
            "name": "Box Office Archaeology: Movies, Mummies, and the Real Indiana Jo"
        },
        {
            "id": 23,
            "code": "ANTH 19000",
            "name": "Selected Topics in Anthropology"
        },
        {
            "id": 24,
            "code": "ANTH 21100",
            "name": "Introduction to Primates"
        },
        {
            "id": 25,
            "code": "ANTH 22600",
            "name": "East Asia: Gender and Identity"
        },
        {
            "id": 26,
            "code": "ANTH 22800",
            "name": "Critical Issues in Asian America"
        },
        {
            "id": 27,
            "code": "ANTH 29000",
            "name": "Seminar in World Ethnography: Selected Topics"
        },
        {
            "id": 28,
            "code": "ANTH 30200",
            "name": "Ethnographic Field Methods"
        },
        {
            "id": 29,
            "code": "ANTH 30500",
            "name": "Archaeological Methods and Techniques"
        },
        {
            "id": 30,
            "code": "ANTH 30800",
            "name": "Methods in Field Primatology"
        },
        {
            "id": 31,
            "code": "ANTH 31100",
            "name": "Primate Behavior and Ecology"
        },
        {
            "id": 32,
            "code": "ANTH 31500",
            "name": "Animals & Human Exceptionalism"
        },
        {
            "id": 33,
            "code": "ANTH 32000",
            "name": "Anthropology of Religion"
        },
        {
            "id": 34,
            "code": "ANTH 33500",
            "name": "Women and Culture"
        },
        {
            "id": 35,
            "code": "ANTH 37000",
            "name": "Applied Anthropology"
        },
        {
            "id": 36,
            "code": "ANTH 47900",
            "name": "Anthropology Fieldwork/Research"
        },
        {
            "id": 37,
            "code": "ANTH 49500",
            "name": "Anthropology Capstone"
        },
        {
            "id": 38,
            "code": "ART 10100",
            "name": "Theory and Practice: Play and Exploration"
        },
        {
            "id": 39,
            "code": "ART 11000",
            "name": "Introduction to Drawing: Seeing the World"
        },
        {
            "id": 40,
            "code": "ART 14000",
            "name": "Introduction to Painting"
        },
        {
            "id": 41,
            "code": "ART 14100",
            "name": "Introduction to Painting: From Wilderness to Wasteland"
        },
        {
            "id": 42,
            "code": "ART 14200",
            "name": "Introduction to Painting: Identities Re-Imagined"
        },
        {
            "id": 43,
            "code": "ART 16100",
            "name": "Introduction to Print Media: Sustainable Practice"
        },
        {
            "id": 44,
            "code": "ART 21000",
            "name": "Intermediate Drawing"
        },
        {
            "id": 45,
            "code": "ART 21200",
            "name": "Figure Drawing"
        },
        {
            "id": 46,
            "code": "ART 26900",
            "name": "Intermediate Print Media: Selected Topics"
        },
        {
            "id": 47,
            "code": "ART 30000",
            "name": "Theory and Practice 3: Professional Practices"
        },
        {
            "id": 48,
            "code": "ART 32700",
            "name": "Graphic Design III"
        },
        {
            "id": 49,
            "code": "ART 32900",
            "name": "Advanced Graphic Design: Selected Topics"
        },
        {
            "id": 50,
            "code": "ART 40100",
            "name": "Theory and Practice: Professional Practices"
        },
        {
            "id": 51,
            "code": "ARTH 11100",
            "name": "Episodes in Western Art"
        },
        {
            "id": 52,
            "code": "ARTH 13500",
            "name": "Introduction to Visual Culture"
        },
        {
            "id": 53,
            "code": "ARTH 20100",
            "name": "Practicing Art History"
        },
        {
            "id": 54,
            "code": "ARTH 20500",
            "name": "Chemistry and Art"
        },
        {
            "id": 55,
            "code": "ARTH 21700",
            "name": "British Art and Architecture I: 1066-1660"
        },
        {
            "id": 56,
            "code": "ARTH 21800",
            "name": "British Art and Architecture II: 1660-1914"
        },
        {
            "id": 57,
            "code": "ARTH 31800",
            "name": "Memorable Cities"
        },
        {
            "id": 58,
            "code": "ARTH 48000",
            "name": "Senior Portfolio: Architectural Studies"
        },
        {
            "id": 59,
            "code": "ARTH 49000",
            "name": "Seminar: Art History"
        },
        {
            "id": 60,
            "code": "BIOL 10100",
            "name": "Plagues and Peoples"
        },
        {
            "id": 61,
            "code": "BIOL 10210",
            "name": "Biology of Sex"
        },
        {
            "id": 62,
            "code": "BIOL 11800",
            "name": "Island Biology"
        },
        {
            "id": 63,
            "code": "BIOL 20500",
            "name": "Biology of Aging"
        },
        {
            "id": 64,
            "code": "BIOL 21200",
            "name": "Conservation Biology"
        },
        {
            "id": 65,
            "code": "BIOL 30200",
            "name": "Research in Biology"
        },
        {
            "id": 66,
            "code": "BIOL 41100",
            "name": "Biology Seminar"
        },
        {
            "id": 67,
            "code": "BINT 10100",
            "name": "World of Business"
        },
        {
            "id": 68,
            "code": "BINT 39800",
            "name": "Internship for Credit"
        },
        {
            "id": 69,
            "code": "CHEM 10100",
            "name": "Chemistry and Your Body"
        },
        {
            "id": 70,
            "code": "CHEM 12100",
            "name": "Principles of Chemistry"
        },
        {
            "id": 71,
            "code": "CHEM 22100",
            "name": "Organic Chemistry"
        },
        {
            "id": 72,
            "code": "CHEM 22200",
            "name": "Organic Chemistry II"
        },
        {
            "id": 73,
            "code": "CHEM 23200",
            "name": "Quantitative Chemistry"
        },
        {
            "id": 74,
            "code": "CHEM 33100",
            "name": "Physical Chemistry: Thermodynamics and Kinetics"
        },
        {
            "id": 75,
            "code": "CHEM 34300",
            "name": "Inorganic Chemistry"
        },
        {
            "id": 76,
            "code": "CHEM 43200",
            "name": "Bio-Organic Chemistry"
        },
        {
            "id": 77,
            "code": "CHEM 44200",
            "name": "Computational Chemistry"
        },
        {
            "id": 78,
            "code": "CHIN 10100",
            "name": "Elementary Chinese I"
        },
        {
            "id": 79,
            "code": "CHIN 10200",
            "name": "Elementary Chinese II"
        },
        {
            "id": 80,
            "code": "CNPH 11100",
            "name": "Cinema Production 1"
        },
        {
            "id": 81,
            "code": "CNPH 20500",
            "name": "Photographic Currents"
        },
        {
            "id": 82,
            "code": "CNPH 20700",
            "name": "European Cinema"
        },
        {
            "id": 83,
            "code": "CNPH 30000",
            "name": "Fiction Film Theory"
        },
        {
            "id": 84,
            "code": "CNPH 30500",
            "name": "Contemporary Film Criticism"
        },
        {
            "id": 85,
            "code": "CNPH 44300",
            "name": "Photo Workshop"
        },
        {
            "id": 86,
            "code": "CMST 11000",
            "name": "Public Communication"
        },
        {
            "id": 87,
            "code": "CMST 11500",
            "name": "Business and Profesional Communication"
        },
        {
            "id": 88,
            "code": "CMST 14000",
            "name": "Small Group Communication"
        },
        {
            "id": 89,
            "code": "CMST 39500",
            "name": "Internship: Communication Studies"
        },
        {
            "id": 90,
            "code": "COMP 10700",
            "name": "Introduction to 2D Game Development"
        },
        {
            "id": 91,
            "code": "COMP 11500",
            "name": "Discrete Structures for Computer Science"
        },
        {
            "id": 92,
            "code": "COMP 17100",
            "name": "Principles of Computing Science I"
        },
        {
            "id": 93,
            "code": "COMP 17200",
            "name": "Principles of Computer Science II"
        },
        {
            "id": 94,
            "code": "COMP 20500",
            "name": "Advanced Web Programming"
        },
        {
            "id": 95,
            "code": "COMP 22000",
            "name": "Introduction to Data Structures"
        },
        {
            "id": 96,
            "code": "COMP 30600",
            "name": "Mobile Development"
        },
        {
            "id": 97,
            "code": "CSCR 10600",
            "name": "Introduction to African Diaspora Studies"
        },
        {
            "id": 98,
            "code": "CSCR 11000",
            "name": "Introduction to Asian American Studies"
        },
        {
            "id": 99,
            "code": "CSCR 21100",
            "name": "American Gangster: Social Portrayals of Gangs"
        },
        {
            "id": 100,
            "code": "CSCR 25600",
            "name": "The Politics of Whiteness"
        },
        {
            "id": 101,
            "code": "DNCE 10000",
            "name": "Introduction to Dance"
        },
        {
            "id": 102,
            "code": "DNCE 11100",
            "name": "Ballet I"
        },
        {
            "id": 103,
            "code": "DNCE 13100",
            "name": "Jazz Dance I"
        },
        {
            "id": 104,
            "code": "DNCE 30100",
            "name": "Survey of Dance History"
        },
        {
            "id": 105,
            "code": "DOCU 10100",
            "name": "Documentary Immersion"
        },
        {
            "id": 106,
            "code": "ECON 12000",
            "name": "Principles of Economics"
        },
        {
            "id": 107,
            "code": "ECON 20100",
            "name": "Micro Analysis"
        },
        {
            "id": 108,
            "code": "ECON 30100",
            "name": "Labor Economics"
        },
        {
            "id": 109,
            "code": "EDUC 10000",
            "name": "Education and Society"
        },
        {
            "id": 110,
            "code": "EDUC 21010",
            "name": "Educational Psychology"
        },
        {
            "id": 111,
            "code": "EDUC 34100",
            "name": "Science, Technology, and Society"
        }
    ]

    major_json = [
        {
            "id": 1,
            "name": "Accounting",
            "school": "School of Business"
        },
        {
            "id": 2,
            "name": "Business Administration",
            "school": "School of Business"
        },
        {
            "id": 3,
            "name": "Film, Photography, & Visual Arts Major",
            "school": "Roy H. Park School of Communications"
        },
        {
            "id": 4,
            "name": "Television & Digital Media Production Major",
            "school": "Roy H. Park School of Communications"
        },
        {
            "id": 5,
            "name": "Exercise Science",
            "school": "School of Health Sciences and Human Performance"
        },
        {
            "id": 6,
            "name": "Occupational Science",
            "school": "School of Health Sciences and Human Performance"
        },
        {
            "id": 7,
            "name": "Clinical Health Studies",
            "school": "School of Health Sciences and Human Performance"
        },
        {
            "id": 8,
            "name": "Speech-Language Pathology",
            "school": "School of Health Sciences and Human Performance"
        },
        {
            "id": 9,
            "name": "Biochemistry",
            "school": "School of Humanities and Sciences"
        },
        {
            "id": 10,
            "name": "Biology",
            "school": "School of Humanities and Sciences"
        },
        {
            "id": 11,
            "name": "Race, Power, and Resistance",
            "school": "School of Humanities and Sciences"
        },
        {
            "id": 12,
            "name": "Chemistry",
            "school": "School of Humanities and Sciences"
        },
        {
            "id": 13,
            "name": "Computer Science",
            "school": "School of Humanities and Sciences"
        },
        {
            "id": 14,
            "name": "Mathematics",
            "school": "School of Humanities and Sciences"
        },
        {
            "id": 15,
            "name": "Politics",
            "school": "School of Humanities and Sciences"
        },
        {
            "id": 16,
            "name": "World Languages and Cultures",
            "school": "School of Humanities and Sciences"
        },
        {
            "id": 17,
            "name": "Writing",
            "school": "School of Humanities and Sciences"
        },
        {
            "id": 18,
            "name": "Music Education",
            "school": "School of Music, Theatre, and Dance"
        },
        {
            "id": 19,
            "name": "Performance",
            "school": "School of Music, Theatre, and Dance"
        },
        {
            "id": 20,
            "name": "Composition",
            "school": "School of Music, Theatre, and Dance"
        },
        {
            "id": 21,
            "name": "Acting",
            "school": "School of Music, Theatre, and Dance"
        },
        {
            "id": 22,
            "name": "Stage Management",
            "school": "School of Music, Theatre, and Dance"
        },
        {
            "id": 23,
            "name": "Theatre Studies",
            "school": "School of Music, Theatre, and Dance"
        }
    ]

    org_json = [
      {
        "id": 1,
        "name": "Katalyst K-pop Dance"
      },
      {
        "id": 2,
        "name": "Ithaca College Anime Club"
      },
      {
        "id": 3,
        "name": "Asian American Alliance"
      },
      {
        "id": 4,
        "name": "IC Unbound Dance Company"
      },
      {
        "id": 5,
        "name": "Pulse Hip Hop Team"
      },
      {
        "id": 6,
        "name": "IC Swim Club"
      },
      {
        "id": 7,
        "name": "Ithaca College Running Club"
      },
      {
        "id": 8,
        "name": "Ithaca College Softball"
      },
      {
        "id": 9,
        "name": "First Generation Organization"
      },
      {
        "id": 10,
        "name": "African Students Association"
      },
      {
        "id": 11,
        "name": "Biology Club"
      },
      {
        "id": 12,
        "name": "Black Student Union of Ithaca College"
      },
      {
        "id": 13,
        "name": "Brothers for Brothers"
      },
      {
        "id": 14,
        "name": "IC After Dark"
      },
      {
        "id": 15,
        "name": "IC Astronomy Club"
      },
      {
        "id": 16,
        "name": "IC Disney Club"
      },
      {
        "id": 17,
        "name": "IC Ping Pong"
      },
      {
        "id": 18,
        "name": "Ithaca College Mock Trial"
      },
      {
        "id": 19,
        "name": "Ithaca College Nerf Club"
      },
      {
        "id": 20,
        "name": "Sister 2 Sister"
      }
    ]

    professor_json = [
  {
    "id": 1,
    "name": "Katlyn Brumfield",
    "department": "Art"
  },
  {
    "id": 2,
    "name": "Patti Capaldi",
    "department": "Art"
  },
  {
    "id": 3,
    "name": "Dara Engler",
    "department": "Art"
  },
  {
    "id": 4,
    "name": "Bill Hastings",
    "department": "Art"
  },
  {
    "id": 5,
    "name": "Pat Hunsinger",
    "department": "Art"
  },
  {
    "id": 6,
    "name": "Neil Infalvi",
    "department": "Art"
  },
  {
    "id": 7,
    "name": "Amber Lia-Kloppel",
    "department": "Art"
  },
  {
    "id": 8,
    "name": "Maria McMahon",
    "department": "Art"
  },
  {
    "id": 9,
    "name": "Jason Otero",
    "department": "Art"
  },
  {
    "id": 10,
    "name": "Grace Troxell",
    "department": "Art"
  },
  {
    "id": 11,
    "name": "Paulina Velázquez Solís",
    "department": "Art"
  },
  {
    "id": 12,
    "name": "Paul Wilson",
    "department": "Art History"
  },
  {
    "id": 13,
    "name": "Jennifer Jolly",
    "department": "Art History"
  },
  {
    "id": 14,
    "name": "Risham Majeed",
    "department": "Art History"
  },
  {
    "id": 15,
    "name": "Gary Wells",
    "department": "Art History"
  },
  {
    "id": 16,
    "name": "Lauren O'Connell",
    "department": "Architecture Studies"
  },
  {
    "id": 17,
    "name": "David Salomon",
    "department": "Architecture Studies"
  },
  {
    "id": 18,
    "name": "Zohreh Soltani",
    "department": "Architecture Studies"
  },
  {
    "id": 19,
    "name": "Jean Hardwick",
    "department": "Biology"
  },
  {
    "id": 20,
    "name": "Rebecca Brady",
    "department": "Biology"
  },
  {
    "id": 21,
    "name": "Elijah Carter",
    "department": "Biology"
  },
  {
    "id": 22,
    "name": "Lisa Corewyn",
    "department": "Biology"
  },
  {
    "id": 23,
    "name": "Edward Cluett",
    "department": "Biology"
  },
  {
    "id": 24,
    "name": "Nandadevi Cortes Rodriguez",
    "department": "Biology"
  },
  {
    "id": 25,
    "name": "David Gondek",
    "department": "Biology"
  },
  {
    "id": 26,
    "name": "Leann Kanda",
    "department": "Biology"
  },
  {
    "id": 27,
    "name": "Maki Inada",
    "department": "Biology"
  },
  {
    "id": 28,
    "name": "Te-Wen Lo",
    "department": "Biology"
  },
  {
    "id": 29,
    "name": "Peter J. Melcher",
    "department": "Biology"
  },
  {
    "id": 30,
    "name": "Brooks Miner",
    "department": "Biology"
  },
  {
    "id": 31,
    "name": "Andrew Smith",
    "department": "Biology"
  },
  {
    "id": 32,
    "name": "Susan Swensen Witherup",
    "department": "Biology"
  },
  {
    "id": 33,
    "name": "Ian Woods",
    "department": "Biology"
  },
  {
    "id": 34,
    "name": "Belisa Gonzalez",
    "department": "Center for the Study of Culture, Race, and Ethnicity"
  },
  {
    "id": 35,
    "name": "M Horsley",
    "department": "Center for the Study of Culture, Race, and Ethnicity"
  },
  {
    "id": 36,
    "name": "Mika Kennedy",
    "department": "Center for the Study of Culture, Race, and Ethnicity"
  },
  {
    "id": 37,
    "name": "Pamela Sertzen",
    "department": "Center for the Study of Culture, Race, and Ethnicity"
  },
  {
    "id": 38,
    "name": "Kai Wen Yang",
    "department": "Center for the Study of Culture, Race, and Ethnicity"
  },
  {
    "id": 39,
    "name": "Mike Haaf",
    "department": "Chemistry"
  },
  {
    "id": 40,
    "name": "Rebecca Craig",
    "department": "Chemistry"
  },
  {
    "id": 41,
    "name": "Jamie Ellis",
    "department": "Chemistry"
  },
  {
    "id": 42,
    "name": "Akiko Fillinger",
    "department": "Chemistry"
  },
  {
    "id": 43,
    "name": "Janet Hunting",
    "department": "Chemistry"
  },
  {
    "id": 44,
    "name": "Anna Larsen",
    "department": "Chemistry"
  },
  {
    "id": 45,
    "name": "DJ Robinson",
    "department": "Chemistry"
  },
  {
    "id": 46,
    "name": "Daisy Rosas Vargas",
    "department": "Chemistry"
  },
  {
    "id": 47,
    "name": "Andrew Torelli",
    "department": "Chemistry"
  },
  {
    "id": 48,
    "name": "Scott Ulrich",
    "department": "Chemistry"
  },
  {
    "id": 49,
    "name": "Ali Erkan",
    "department": "Computer Science"
  },
  {
    "id": 50,
    "name": "Toby Dragon",
    "department": "Computer Science"
  },
  {
    "id": 51,
    "name": "John Barr",
    "department": "Computer Science"
  },
  {
    "id": 52,
    "name": "Adam Lee",
    "department": "Computer Science"
  },
  {
    "id": 53,
    "name": "Sharon Stansfield",
    "department": "Computer Science"
  },
  {
    "id": 54,
    "name": "Doug Turnbull",
    "department": "Computer Science"
  },
  {
    "id": 55,
    "name": "Shaianne Osterreich",
    "department": "Economics"
  },
  {
    "id": 56,
    "name": "Elia Kacapyr",
    "department": "Economics"
  },
  {
    "id": 57,
    "name": "Elizabeth Kaletski",
    "department": "Economics"
  },
  {
    "id": 58,
    "name": "William Kolberg",
    "department": "Economics"
  },
  {
    "id": 59,
    "name": "Sara Levy",
    "department": "Education"
  },
  {
    "id": 60,
    "name": "Peter C Martin",
    "department": "Education"
  },
  {
    "id": 61,
    "name": "Jeane Copenhaver-Johnson",
    "department": "Education"
  },
  {
    "id": 62,
    "name": "Sean Eversley-Bradwell",
    "department": "Education"
  },
  {
    "id": 63,
    "name": "Ellie Fulmer",
    "department": "Education"
  },
  {
    "id": 64,
    "name": "Nia Nunn",
    "department": "Education"
  },
  {
    "id": 65,
    "name": "Shuzhan Li",
    "department": "Education"
  },
  {
    "id": 66,
    "name": "Jeff Perry",
    "department": "Education"
  },
  {
    "id": 67,
    "name": "Mike Cecere",
    "department": "Education"
  },
  {
    "id": 68,
    "name": "Karen Patricio",
    "department": "Education"
  },
  {
    "id": 69,
    "name": "Molly Buck",
    "department": "Education"
  },
  {
    "id": 70,
    "name": "Chris Holmes",
    "department": "Literatures in English"
  },
  {
    "id": 71,
    "name": "Derek Adams",
    "department": "Literatures in English"
  },
  {
    "id": 72,
    "name": "Kasia Bartoszynska",
    "department": "Literatures in English"
  },
  {
    "id": 73,
    "name": "Alexis Becker",
    "department": "Literatures in English"
  },
  {
    "id": 74,
    "name": "Dan Breen",
    "department": "Literatures in English"
  },
  {
    "id": 75,
    "name": "Ann Byrne",
    "department": "Literatures in English"
  },
  {
    "id": 76,
    "name": "Hugh Egan",
    "department": "Literatures in English"
  },
  {
    "id": 77,
    "name": "Paul Hansom",
    "department": "Literatures in English"
  },
  {
    "id": 78,
    "name": "Katharine Kittredge",
    "department": "Literatures in English"
  },
  {
    "id": 79,
    "name": "David Kramer",
    "department": "Literatures in English"
  },
  {
    "id": 80,
    "name": "Christopher Matusiak",
    "department": "Literatures in English"
  },
  {
    "id": 81,
    "name": "Jennifer Spitzer",
    "department": "Literatures in English"
  },
  {
    "id": 82,
    "name": "Robert Sullivan",
    "department": "Literatures in English"
  },
  {
    "id": 83,
    "name": "Jake Brenner",
    "department": "Environmental Studies and Sciences"
  },
  {
    "id": 84,
    "name": "Susan Allen",
    "department": "Environmental Studies and Sciences"
  },
  {
    "id": 85,
    "name": "Jason Hamilton",
    "department": "Environmental Studies and Sciences"
  },
  {
    "id": 86,
    "name": "Michael Smith",
    "department": "Environmental Studies and Sciences"
  },
  {
    "id": 87,
    "name": "Anne Stork",
    "department": "Environmental Studies and Sciences"
  },
  {
    "id": 88,
    "name": "Paula Turkon",
    "department": "Environmental Studies and Sciences"
  },
  {
    "id": 89,
    "name": "Matthew Klemm",
    "department": "History"
  },
  {
    "id": 90,
    "name": "Jonathan Ablard",
    "department": "History"
  },
  {
    "id": 91,
    "name": "Karin Breuer",
    "department": "History"
  },
  {
    "id": 92,
    "name": "Jason Freitag",
    "department": "History"
  },
  {
    "id": 93,
    "name": "Zoe Shan Lin",
    "department": "History"
  },
  {
    "id": 94,
    "name": "Pearl Ponce",
    "department": "History"
  },
  {
    "id": 95,
    "name": "Michael Trotti",
    "department": "History"
  },
  {
    "id": 96,
    "name": "Zenon Wasyliw",
    "department": "History"
  },
  {
    "id": 97,
    "name": "Thomas J. Pfaff",
    "department": "Mathematics"
  },
  {
    "id": 98,
    "name": "David A Brown",
    "department": "Mathematics"
  },
  {
    "id": 99,
    "name": "James Conklin",
    "department": "Mathematics"
  },
  {
    "id": 100,
    "name": "Ted Galanthay",
    "department": "Mathematics"
  },
  {
    "id": 101,
    "name": "Joash Geteregechi",
    "department": "Mathematics"
  },
  {
    "id": 102,
    "name": "Peter Maceli",
    "department": "Mathematics"
  },
  {
    "id": 103,
    "name": "Megan Martinez",
    "department": "Mathematics"
  },
  {
    "id": 104,
    "name": "Holli Mast",
    "department": "Mathematics"
  },
  {
    "id": 105,
    "name": "Teresa Moore",
    "department": "Mathematics"
  },
  {
    "id": 106,
    "name": "Daniel Visscher",
    "department": "Mathematics"
  },
  {
    "id": 107,
    "name": "Aaron Weinberg",
    "department": "Mathematics"
  },
  {
    "id": 108,
    "name": "Emilie Wiesner",
    "department": "Mathematics"
  },
  {
    "id": 109,
    "name": "Osman Yurekli",
    "department": "Mathematics"
  },
  {
    "id": 110,
    "name": "Michael Richardson",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 111,
    "name": "Maria DiFrancesco",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 112,
    "name": "Julia Cozzarelli",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 113,
    "name": "Marella Feltrin-Morris",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 114,
    "name": "Mat Fournier",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 115,
    "name": "Enrique Gonzalez-Conty",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 116,
    "name": "Annette Levine",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 117,
    "name": "Camilo Malagon",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 118,
    "name": "Sergio Pedro",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 119,
    "name": "James Pfrehm",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 120,
    "name": "Gladys M. Varona-Lacey",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 121,
    "name": "Silvia M. Abbiati",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 122,
    "name": "Hong Li",
    "department": "World Languages, Literatures, and Cultures"
  },
  {
    "id": 123,
    "name": "Craig Duncan",
    "department": "Philosophy and Religion"
  },
  {
    "id": 124,
    "name": "Samah Choudhury",
    "department": "Philosophy and Religion"
  },
  {
    "id": 125,
    "name": "Serge Grigoriev",
    "department": "Philosophy and Religion"
  },
  {
    "id": 126,
    "name": "Christopher House",
    "department": "Philosophy and Religion"
  },
  {
    "id": 127,
    "name": "Frederik Kaufman",
    "department": "Philosophy and Religion"
  },
  {
    "id": 128,
    "name": "Rebecca Lesses",
    "department": "Philosophy and Religion"
  },
  {
    "id": 129,
    "name": "Tatiana Patrone",
    "department": "Philosophy and Religion"
  },
  {
    "id": 130,
    "name": "Jonathan Peeters",
    "department": "Philosophy and Religion"
  },
  {
    "id": 131,
    "name": "Eric Steinschneider",
    "department": "Philosophy and Religion"
  },
  {
    "id": 132,
    "name": "Rachel Wagner",
    "department": "Philosophy and Religion"
  },
  {
    "id": 133,
    "name": "Beth Ellen Clark Joseph",
    "department": "Physics and Astronomy"
  },
  {
    "id": 134,
    "name": "Matthew C. Sullivan",
    "department": "Physics and Astronomy"
  },
  {
    "id": 135,
    "name": "Colleen Countryman",
    "department": "Physics and Astronomy"
  },
  {
    "id": 136,
    "name": "Jerome Fung",
    "department": "Physics and Astronomy"
  },
  {
    "id": 137,
    "name": "Luke Keller",
    "department": "Physics and Astronomy"
  },
  {
    "id": 138,
    "name": "Eric Leibensperger",
    "department": "Physics and Astronomy"
  },
  {
    "id": 139,
    "name": "Matthew Price",
    "department": "Physics and Astronomy"
  },
  {
    "id": 140,
    "name": "Kelley D. Sullivan",
    "department": "Physics and Astronomy"
  },
  {
    "id": 141,
    "name": "Chip Gagnon",
    "department": "Politics"
  },
  {
    "id": 142,
    "name": "Carlos Figueroa",
    "department": "Politics"
  },
  {
    "id": 143,
    "name": "Juan Arroyo",
    "department": "Politics"
  },
  {
    "id": 144,
    "name": "Atuk Sumru",
    "department": "Politics"
  },
  {
    "id": 145,
    "name": "Donald Beachler",
    "department": "Politics"
  },
  {
    "id": 146,
    "name": "Evgenia Ilieva",
    "department": "Politics"
  },
  {
    "id": 147,
    "name": "Naeem Inayatullah",
    "department": "Politics"
  },
  {
    "id": 148,
    "name": "Amy Rothschild",
    "department": "Politics"
  },
  {
    "id": 149,
    "name": "Peyi Soyinka-Airewele",
    "department": "Politics"
  },
  {
    "id": 150,
    "name": "Mary Turner DePalma",
    "department": "Psychology"
  },
  {
    "id": 151,
    "name": "Bernard Beins",
    "department": "Psychology"
  },
  {
    "id": 152,
    "name": "Brandy Bessette-Symons",
    "department": "Psychology"
  },
  {
    "id": 153,
    "name": "Natasha Bharj",
    "department": "Psychology"
  },
  {
    "id": 154,
    "name": "Jessye Cohen-Filipic",
    "department": "Psychology"
  },
  {
    "id": 155,
    "name": "Amanda Faherty",
    "department": "Psychology"
  },
  {
    "id": 156,
    "name": "Jeff Holmes",
    "department": "Psychology"
  },
  {
    "id": 157,
    "name": "Judith Pena-Shaff",
    "department": "Psychology"
  },
  {
    "id": 158,
    "name": "Cyndy Scheibe",
    "department": "Psychology"
  },
  {
    "id": 159,
    "name": "Hugh Stephenson",
    "department": "Psychology"
  },
  {
    "id": 160,
    "name": "Leigh Ann Vaughn",
    "department": "Psychology"
  },
  {
    "id": 161,
    "name": "Katherine Cohen-Filipic",
    "department": "Sociology"
  },
  {
    "id": 162,
    "name": "Jarron Bowman",
    "department": "Sociology"
  },
  {
    "id": 163,
    "name": "Joslyn Brenton",
    "department": "Sociology"
  },
  {
    "id": 164,
    "name": "Sergio A. Cabrera",
    "department": "Sociology"
  },
  {
    "id": 165,
    "name": "Jessica Dunning-Lozano",
    "department": "Sociology"
  },
  {
    "id": 166,
    "name": "Stephen Sweet",
    "department": "Sociology"
  },
  {
    "id": 167,
    "name": "Alicia Swords",
    "department": "Sociology"
  },
  {
    "id": 168,
    "name": "Eleanor Henderson",
    "department": "Writing"
  },
  {
    "id": 169,
    "name": "Barbara Adams",
    "department": "Writing"
  },
  {
    "id": 170,
    "name": "Cory Brown",
    "department": "Writing"
  },
  {
    "id": 171,
    "name": "Susan Adams Delaney",
    "department": "Writing"
  },
  {
    "id": 172,
    "name": "Anthony DiRenzo",
    "department": "Writing"
  },
  {
    "id": 173,
    "name": "Megan Graham",
    "department": "Writing"
  },
  {
    "id": 174,
    "name": "Rajpreet Heir",
    "department": "Writing"
  },
  {
    "id": 175,
    "name": "Nick Kowalczyk",
    "department": "Writing"
  },
  {
    "id": 176,
    "name": "Katharyn Howd Machan",
    "department": "Writing"
  },
  {
    "id": 177,
    "name": "Joan Marcus",
    "department": "Writing"
  },
  {
    "id": 178,
    "name": "Katie Marks",
    "department": "Writing"
  },
  {
    "id": 179,
    "name": "Vinita Prabhakar",
    "department": "Writing"
  },
  {
    "id": 180,
    "name": "Amy Quan",
    "department": "Writing"
  },
  {
    "id": 181,
    "name": "Mary Lourdes Silva",
    "department": "Writing"
  },
  {
    "id": 182,
    "name": "Priya Sirohi",
    "department": "Writing"
  },
  {
    "id": 183,
    "name": "Jim Stafford",
    "department": "Writing"
  },
  {
    "id": 184,
    "name": "Catherine Taylor",
    "department": "Writing"
  },
  {
    "id": 185,
    "name": "Jack Wang",
    "department": "Writing"
  },
  {
    "id": 186,
    "name": "Jaime Warburton",
    "department": "Writing"
  },
  {
    "id": 187,
    "name": "Jacob White",
    "department": "Writing"
  },
  {
    "id": 188,
    "name": "Augusto Facchini",
    "department": "Writing"
  },
  {
    "id": 189,
    "name": "Rachel Fomalhaut",
    "department": "Writing"
  }
]

    user_json = [
          {
            "id": 1,
            "username": "alice.apple",
            "email": "alice.apple@example.com",
            "class_year": 2027,
            "internship": True,
            "study_abroad": False,
            "student_research": True
          },
          {
            "id": 2,
            "username": "betty.blueberry",
            "email": "betty.blueberry@example.com",
            "class_year": 2026,
            "internship": False,
            "study_abroad": True,
            "student_research": False
          },
          {
            "id": 3,
            "username": "charlie.cheese",
            "email": "charlie.cheese@example.com",
            "class_year": 2024,
            "internship": True,
            "study_abroad": True,
            "student_research": True
          },
          {
            "id": 4,
            "username": "danny.doughnut",
            "email": "danny.doughnut@example.com",
            "class_year": 2026,
            "internship": False,
            "study_abroad": False,
            "student_research": False
          },
          {
            "id": 5,
            "username": "eve.eggplant",
            "email": "eve.eggplant@example.com",
            "class_year": 2024,
            "internship": True,
            "study_abroad": True,
            "student_research": False
          },
          {
            "id": 6,
            "username": "frank.figs",
            "email": "frank.figs@example.com",
            "class_year": 2024,
            "internship": False,
            "study_abroad": True,
            "student_research": True
          },
          {
            "id": 7,
            "username": "gina.grapefruit",
            "email": "gina.grapefruit@example.com",
            "class_year": 2025,
            "internship": True,
            "study_abroad": False,
            "student_research": True
          },
          {
            "id": 8,
            "username": "henry.honeydew",
            "email": "henry.honeydew@example.com",
            "class_year": 2026,
            "internship": False,
            "study_abroad": True,
            "student_research": False
          },
          {
            "id": 9,
            "username": "ivy.icecream",
            "email": "ivy.icecream@example.com",
            "class_year": 2026,
            "internship": True,
            "study_abroad": False,
            "student_research": True
          },
          {
            "id": 10,
            "username": "jack.jalapeno",
            "email": "jack.jalapeno@example.com",
            "class_year": 2024,
            "internship": True,
            "study_abroad": True,
            "student_research": False
          },
          {
            "id": 11,
            "username": "kate.kiwi",
            "email": "kate.kiwi@example.com",
            "class_year": 2025,
            "internship": False,
            "study_abroad": False,
            "student_research": True
          },
          {
            "id": 12,
            "username": "leo.lemon",
            "email": "leo.lemon@example.com",
            "class_year": 2027,
            "internship": True,
            "study_abroad": True,
            "student_research": False
          },
          {
            "id": 13,
            "username": "maria.mango",
            "email": "maria.mango@example.com",
            "class_year": 2025,
            "internship": True,
            "study_abroad": False,
            "student_research": False
          },
          {
            "id": 14,
            "username": "nick.nectarine",
            "email": "nick.nectarine@example.com",
            "class_year": 2025,
            "internship": False,
            "study_abroad": True,
            "student_research": True
          },
          {
            "id": 15,
            "username": "olivia.orange",
            "email": "olivia.orange@example.com",
            "class_year": 2026,
            "internship": True,
            "study_abroad": True,
            "student_research": False
          }
    ]

    for each_element in course_json:
        course = Course(id=each_element["id"], code=each_element["code"], name=each_element["name"])
        db.session.add(course)
        db.session.commit()

    for each_element in major_json:
        major = Major(id=each_element["id"], name=each_element["name"], school=each_element["school"])
        db.session.add(major)
        db.session.commit()

    for each_element in org_json:
        org = Org(id=each_element["id"], name=each_element["name"])
        db.session.add(org)
        db.session.commit()

    for each_element in professor_json:
        professor = Professor(id=each_element["id"], name=each_element["name"], department=each_element["department"])
        db.session.add(professor)
        db.session.commit()

    for each_element in user_json:
        user = User(username=each_element["username"], email=each_element["email"], class_year=each_element["class_year"],
                    internship=each_element["internship"], student_research=each_element["student_research"], study_abroad=each_element["study_abroad"])
        db.session.add(user)
        db.session.commit()

    # sample advisees
    for i in range(1, 6):
        match_join = Match(advisee_id=i, advisor_id=None)
        db.session.add(match_join)
        db.session.commit()

    for j in range(6, 16):
        match_join = Match(advisee_id=None, advisor_id=j)
        db.session.add(match_join)
        db.session.commit()

    interest_json = [
      {
        "id": 1,
        "name": "Reading"
      },
      {
        "id": 2,
        "name": "Writing"
      },
      {
        "id": 3,
        "name": "Photography"
      },
      {
        "id": 4,
        "name": "Painting/Drawing"
      },
      {
        "id": 5,
        "name": "Music"
      },
      {
        "id": 6,
        "name": "Hiking"
      },
      {
        "id": 7,
        "name": "Gaming"
      },
      {
        "id": 8,
        "name": "Cooking/Baking"
      },
      {
        "id": 9,
        "name": "Yoga/Fitness"
      },
      {
        "id": 10,
        "name": "Dancing"
      },
      {
        "id": 11,
        "name": "Gardening"
      },
      {
        "id": 12,
        "name": "Coding/Programming"
      },
      {
        "id": 13,
        "name": "Film/TV Series"
      },
      {
        "id": 14,
        "name": "Podcasting"
      },
      {
        "id": 15,
        "name": "Traveling"
      },
      {
        "id": 16,
        "name": "Graphic Design"
      },
      {
        "id": 17,
        "name": "Volunteering"
      },
      {
        "id": 18,
        "name": "Meditation"
      },
      {
        "id": 19,
        "name": "Language Learning"
      },
      {
        "id": 20,
        "name": "Collecting"
      },
      {
        "id": 21,
        "name": "DIY Crafts"
      },
      {
        "id": 22,
        "name": "Cycling"
      },
      {
        "id": 23,
        "name": "Running"
      },
      {
        "id": 24,
        "name": "Astronomy"
      },
      {
        "id": 25,
        "name": "Fashion Design"
      },
      {
        "id": 26,
        "name": "Fishing"
      },
      {
        "id": 27,
        "name": "Chess/Board Games"
      },
      {
        "id": 28,
        "name": "Rock Climbing"
      },
      {
        "id": 29,
        "name": "Astrophotography"
      },
      {
        "id": 30,
        "name": "Bird Watching"
      }
    ]

    m2u_json = [
      {
        "id": 1,
        "major_id": 19,
        "user_id": 6
      },
      {
        "id": 2,
        "major_id": 21,
        "user_id": 7
      },
      {
        "id": 3,
        "major_id": 14,
        "user_id": 8
      },
      {
        "id": 4,
        "major_id": 15,
        "user_id": 9
      },
      {
        "id": 5,
        "major_id": 16,
        "user_id": 10
      },
      {
        "id": 6,
        "major_id": 5,
        "user_id": 11
      },
      {
        "id": 7,
        "major_id": 6,
        "user_id": 12
      },
      {
        "id": 8,
        "major_id": 5,
        "user_id": 13
      },
      {
        "id": 9,
        "major_id": 15,
        "user_id": 14
      },
      {
        "id": 10,
        "major_id": 3,
        "user_id": 15
      }
    ]

    for each_element in interest_json:
        interest = Interest(id=each_element["id"], name=each_element["name"])
        db.session.add(interest)
        db.session.commit()

    for each_element in m2u_json:
        m2u = MajorToUser(id=each_element["id"], major_id=each_element["major_id"], user_id=each_element["user_id"])
        db.session.add(m2u)
        db.session.commit()

    return render_template('index.html', title='Home')


@app.route('/advisee_form', methods=['GET', 'POST'])
@login_required
def advisee_form():
    form = AdviseeForm()
    form.student_orgs.choices = [(o.id,o.name) for o in Org.query.all()]
    form.major.choices = [(m.id, m.name) for m in Major.query.all()]
    form.primary_advisor.choices = [(p.id, p.name) for p in Professor.query.all()]
    form.interests.choices = [(i.id, i.name) for i in Interest.query.all()]
    form.courses.choices = [(c.id, c.name) for c in Course.query.all()]

    if form.validate_on_submit():
        user = current_user
        user.pronouns = form.pronouns.data
        user.class_year = form.class_year.data
        user.internship = form.internship.data
        user.study_abroad = form.study_abroad.data
        user.student_research = form.student_research.data

        for each_major_id in form.major.data:
            major_join = MajorToUser(major_id=each_major_id, user_id=user.id)
            db.session.add(major_join)
            db.session.commit()
        for each_org_id in form.student_orgs.data:
            org_join = StudentOrgToUser(org_id=each_org_id, user_id=user.id)
            db.session.add(org_join)
            db.session.commit()
        for each_course_id in form.courses.data:
            course_join = CourseToUser(course_id=each_course_id, user_id=user.id)
            db.session.add(course_join)
            db.session.commit()
        for each_course_id in form.student_orgs.data:
            course_join = CourseToUser(course_id=each_course_id, user_id=user.id)
            db.session.add(course_join)
            db.session.commit()
        for each_prof_id in form.primary_advisor.data:
            user.primary_advisor_id = each_prof_id
            db.session.commit()

        return redirect(url_for('advisee_matches'))
    return render_template('advisee_signup_form.html', title='Advisee Form', form=form)


@app.route('/advisor_form', methods=['GET', 'POST'])
@login_required
def advisor_form():
    form = AdvisorForm()
    form.student_orgs.choices = [(o.id,o.name) for o in Org.query.all()]
    form.major.choices = [(m.id, m.name) for m in Major.query.all()]
    form.primary_advisor.choices = [(p.id, p.name) for p in Professor.query.all()]
    form.interests.choices = [(i.id, i.name) for i in Interest.query.all()]
    form.minor.choices = [(m.id, m.name) for m in Major.query.all()]
    form.course.choices = [(c.id, c.name) for c in Course.query.all()]

    if form.validate_on_submit():
        user = current_user
        user.pronouns = form.pronouns.data
        user.class_year = form.class_year.data
        user.internship = form.internship.data
        user.study_abroad = form.study_abroad.data
        user.student_research = form.student_research.data
        match = Match(advisor_id=user.id)
        db.session.add(match)
        db.session.commit()
        # user.preferred_contact_method = form.preferred_contact_method.data

        for org_id in form.student_orgs.data:
            o2u = StudentOrgToUser(org_id=org_id, user_id=user.id)
            db.session.add(o2u)
            db.session.commit()
        for major_id in form.major.data:
            m2u = MajorToUser(major_id=major_id, user_id=user.id)
            db.session.add(m2u)
            db.session.commit()
        for interest_id in form.interests.data:
            i2u = InterestToUser(interest_id=interest_id, user_id=user.id)
            db.session.add(i2u)
            db.session.commit()
        for course_id in form.course.data:
            c2u = CourseToUser(course_id=course_id, user_id=user.id)
            db.session.add(c2u)
            db.session.commit()
        flash('Congratulations! You are now a peer advisor, {}'.format(form.name.data))
        return redirect(url_for('advisor_profile', username=user.username))
    return render_template('advisor_signup_form.html', title='Advisor Form', form=form)


@app.route('/advisee_matches')
def advisee_matches():
    advisor_list = User.query.join(Match, User.id == Match.advisor_id).filter(Match.advisor_id.isnot(None)).all()
    user = current_user

    for each_advisor in advisor_list:
        score = 0

        for each_major in user.m2u:
            for each_advisor_major in each_advisor.m2u:
                if each_major == each_advisor_major:
                    score += 1

        if user.primary_advisor == each_advisor.primary_advisor:
            score += 1

        for each_org in user.o2u:
            for each_advisor_org in each_advisor.o2u:
                if each_org == each_advisor_org:
                    score += 1

        for each_interest in user.i2u:
            for each_advisor_interest in each_advisor.i2u:
                if each_interest == each_advisor_interest:
                    score += 1

        if user.internship == each_advisor.internship:
            score += 1

        if user.study_abroad == each_advisor.study_abroad:
            score += 1

        if user.student_research == each_advisor.student_research:
            score += 1

        for each_course in user.c2u:
            for each_advisor_course in each_advisor.c2u:
                if each_course == each_advisor_course:
                    score += 1

        each_advisor.score = score

    sorted_list = sorted(advisor_list, key=lambda x: x.score)
    if current_user in sorted_list:
        sorted_list.remove(current_user)

    # removes all the possible users that you've already matched with
    match_list = Match.query.filter_by(advisee_id=current_user.id).all()
    temp_list = []
    for each_match in match_list:
        temp_list.append(User.query.get_or_404(each_match.advisor_id))
    for each_advisor in temp_list:
        sorted_list.remove(each_advisor)

    return render_template('advisee_matches.html', advisor_list=sorted_list)


@app.route('/advisor_profile/<username>')
@login_required
def advisor_profile(username):
    list1 = Match.query.filter_by(advisor_id=current_user.id).all()
    if len(list1) == 0:
        return render_template('not_an_advisor.html', user=current_user)
    advisor = User.query.filter_by(username=username).first_or_404()
    return render_template('advisor_profile.html', title='Advisor Profile', advisor=advisor)


@app.route('/ongoing_advisee_connections')
@login_required
def ongoing_advisee_connections():
    list1 = Match.query.filter_by(advisor_id=current_user.id).all()
    if len(list1) == 0:
        return render_template('not_an_advisor.html', user=current_user)

    match_list = Match.query.filter_by(advisor_id=current_user.id).all()

    advisee_list = []
    for each_match in match_list:
        advisee = User.query.get(each_match.advisee_id)
        if advisee is not None and advisee is not current_user:
            advisee_list.append(advisee)

    if len(advisee_list) == 0:
        no_advisee = True

    return render_template('ongoing_connection.html', title='Ongoing Connections', advisee_list=advisee_list, no_advisee=no_advisee)


@app.route('/make_connection_for_<userID>')
@login_required
def make_connection(userID):
    match = Match(advisee_id=current_user.id, advisor_id=userID)
    db.session.add(match)
    db.session.commit()

    return redirect(url_for('ongoing_advisors'))


@app.route('/ongoing_advisors')
@login_required
def ongoing_advisors():
    match_list = Match.query.filter_by(advisee_id=current_user.id).all()
    advisor_list = []
    for each_match in match_list:
        advisor_list.append(User.query.get_or_404(each_match.advisor_id))

    return render_template('ongoing_advisors.html', advisor_list=advisor_list, title='Your Advisors')