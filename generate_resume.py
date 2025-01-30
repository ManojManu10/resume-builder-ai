import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def generate_resume_content(data):
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Prepare base prompt for both profile types
        base_prompt = f"""Create a professional ATS-friendly resume in HTML format that follows these rules:
        1. Use a clean, professional layout with proper spacing
        2. Include a header with name and contact details
        3. Use appropriate section headings in uppercase
        4. Format dates consistently
        5. Use bullet points for achievements and responsibilities
        6. Highlight key skills and accomplishments
        7. Ensure content is keyword-optimized for ATS
        8. Use action verbs and quantifiable achievements
        
        The resume should include these sections:
        - Header with contact information
        - Professional Summary
        - Skills
        - Work Experience (with bullet points)
        - Education
        - Additional sections based on profile type
        
        Use this styling:
        - Font: Times New Roman
        - Clean margins and spacing
        - Professional bullet points
        - Consistent date formatting
        """

        # Add profile-specific details to prompt
        if data['profile_type'] == 'fresher':
            prompt = base_prompt + f"""
            Create the resume for a fresher/student with these details:
            Name: {data.get('name', '')}
            Email: {data.get('email', '')}
            Phone: {data.get('phone', '')}
            LinkedIn: {data.get('linkedin', '')}
            Objective: {data.get('objective', '')}
            Education: {data.get('education', '')}
            Skills: {data.get('skills', '')}
            Projects: {data.get('projects', '')}
            Internships: {data.get('internships', '')}
            
            Focus on:
            - Academic achievements
            - Technical skills
            - Projects and internships
            - Extra-curricular activities
            """
        else:
            prompt = base_prompt + f"""
            Create the resume for an experienced professional with these details:
            Name: {data.get('name', '')}
            Email: {data.get('email', '')}
            Phone: {data.get('phone', '')}
            LinkedIn: {data.get('linkedin', '')}
            Experience: {data.get('experience', '')}
            Education: {data.get('education_exp', '')}
            Skills: {data.get('skills', '')}
            Achievements: {data.get('achievements', '')}
            
            Focus on:
            - Professional achievements
            - Leadership and impact
            - Technical expertise
            - Career progression
            """

        # Generate enhanced resume content
        response = model.generate_content(prompt)
        resume_content = response.text

        # Clean up the response
        resume_content = resume_content.replace('```html', '').replace('```', '')
        resume_content = resume_content.strip()

        return resume_content

    except Exception as e:
        return f"Error generating resume: {str(e)}"
