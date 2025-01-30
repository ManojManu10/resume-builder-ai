from flask import Flask, render_template, request, flash, send_from_directory
from generate_resume import generate_resume_content
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)

def get_sample_data(profile_type):
    if profile_type == 'fresher':
        return {
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'phone': '+1 (555) 123-4567',
            'linkedin': 'https://linkedin.com/in/johnsmith',
            'objective': 'Recent Computer Science graduate seeking an entry-level software developer position to leverage my strong programming skills and academic projects experience.',
            'education': 'Bachelor of Science in Computer Science\nUniversity of Technology\nGraduation: May 2024\nGPA: 3.8/4.0\nRelevant Coursework: Data Structures, Algorithms, Web Development, Database Management',
            'projects': '1. E-commerce Website\n- Developed a full-stack e-commerce platform using React and Node.js\n- Implemented secure payment processing and user authentication\n- Achieved 95% test coverage\n\n2. Machine Learning Model\n- Created a predictive model for stock prices using Python and TensorFlow\n- Achieved 85% accuracy in predictions',
            'internships': 'Software Development Intern | Tech Solutions Inc.\nJune 2023 - August 2023\n- Developed and maintained web applications using React and Django\n- Collaborated with senior developers on feature implementation\n- Reduced page load time by 40% through optimization',
            'skills': 'Programming Languages: Python, Java, JavaScript, HTML/CSS\nFrameworks: React, Node.js, Django\nTools: Git, Docker, AWS\nSoft Skills: Problem Solving, Team Collaboration, Communication',
            'certifications': 'AWS Certified Cloud Practitioner (2023)\nGoogle IT Automation with Python Professional Certificate (2023)',
            'achievements': '- Dean\'s List for 4 consecutive semesters\n- Winner of University Hackathon 2023\n- Published paper on AI applications in healthcare'
        }
    else:
        return {
            'name': 'Sarah Johnson',
            'email': 'sarah.johnson@email.com',
            'phone': '+1 (555) 987-6543',
            'linkedin': 'https://linkedin.com/in/sarahjohnson',
            'experience': 'Senior Software Engineer | Tech Corp\nJan 2020 - Present\n- Led a team of 5 developers in developing cloud-native applications\n- Reduced system downtime by 75% through implementing robust monitoring\n- Mentored junior developers and conducted code reviews\n\nSoftware Engineer | Innovation Labs\nJun 2017 - Dec 2019\n- Developed microservices using Java Spring Boot\n- Improved API response time by 60%\n- Implemented CI/CD pipeline reducing deployment time by 40%',
            'education_exp': 'Master of Science in Software Engineering\nTech University\nGraduation: 2017\n\nBachelor of Science in Computer Science\nState University\nGraduation: 2015',
            'skills': 'Programming: Java, Python, Go, JavaScript\nFrameworks: Spring Boot, React, Angular\nCloud: AWS, Azure, Kubernetes\nLeadership: Team Management, Agile Methodologies, Technical Planning',
            'certifications': 'AWS Solutions Architect Professional\nGoogle Cloud Professional Engineer\nCertified Scrum Master',
            'achievements': '- Received Best Technical Leader Award 2022\n- Patents: 2 filed, 1 granted in distributed systems\n- Speaker at multiple tech conferences'
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Collect form data
            form_data = {
                'profile_type': request.form.get('profile_type'),
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'linkedin': request.form.get('linkedin'),
                'skills': request.form.get('skills'),
                'certifications': request.form.get('certifications'),
                'achievements': request.form.get('achievements')
            }

            # Add profile-specific fields
            if form_data['profile_type'] == 'fresher':
                form_data.update({
                    'objective': request.form.get('objective'),
                    'education': request.form.get('education'),
                    'projects': request.form.get('projects'),
                    'internships': request.form.get('internships')
                })
            else:
                form_data.update({
                    'experience': request.form.get('experience'),
                    'education_exp': request.form.get('education_exp')
                })

            # Validate required fields
            required_fields = ['name', 'email', 'phone', 'skills']
            if form_data['profile_type'] == 'fresher':
                required_fields.extend(['education'])
            else:
                required_fields.extend(['experience', 'education_exp'])

            missing_fields = [field for field in required_fields if not form_data.get(field)]
            if missing_fields:
                flash(f"Please fill in all required fields: {', '.join(missing_fields)}", 'error')
                return render_template('index.html')

            # Generate resume content
            resume_content = generate_resume_content(form_data)

            # Check if there was an error
            if resume_content.startswith('Error'):
                flash(resume_content, 'error')
                return render_template('index.html')

            # Show preview page with all templates
            return render_template('preview.html', 
                                resume_content=resume_content,
                                form_data=form_data)

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('index.html')

    # For GET request, return form with sample data
    profile_type = request.args.get('profile_type', 'fresher')
    sample_data = get_sample_data(profile_type)
    return render_template('index.html', sample_data=sample_data)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get the selected template and form data
        selected_template = request.form.get('final_template')
        form_data = {key: request.form.get(key) for key in request.form.keys()}
        
        # Generate resume content
        resume_content = generate_resume_content(form_data)
        
        # Render the selected template
        template_file = f"resume_templates/template{selected_template}.html"
        
        return render_template(template_file,
                            resume=resume_content,
                            name=form_data['name'],
                            email=form_data['email'],
                            phone=form_data['phone'],
                            linkedin=form_data.get('linkedin'),
                            profile_type=form_data['profile_type'])

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)