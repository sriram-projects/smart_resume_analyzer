import os 
import re 
from docx import Document 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def extract_text_from_docx(file_path): 
    doc = Document(file_path) 
    return " ".join([para.text for para in doc.paragraphs])

def analyze_resume(text): 
    keywords = ["Python", "Machine Learning", "Data Analysis","Problem solving", "Communication", "Leadership"] 
    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()] 
    score = (len(found_keywords) / len(keywords)) * 10  
    if len(found_keywords) < len(keywords): 
        feedback = f"consider adding more keywords like:{','.join(set(keywords) - set(found_keywords))}"
    else :
        feedback = "Great job! Your resume covers key skills." 
    return round(score, 2), feedback

def generate_resume(details):
    file_path = f"{details['Name'].replace(' ', '_')}_Resume.pdf"
    
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter


    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkblue)
    c.drawString(50, height - 50, details["Name"])
    
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(50, height - 70, f"Job Title: {details['Job Title']}")
    c.drawString(50, height - 90, f"Email: {details['Email']}")
    c.drawString(50, height - 110, f"Phone: {details['Phone']}")
    

    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    c.line(50, height - 130, width - 50, height - 130)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 160, "Objectives:")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 180, details["Objectives"])

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 220, "Skills:")
    c.setFont("Helvetica", 12)
    skills = details["Skills"].split(", ")
    y_position = height - 240
    for skill in skills:
        c.drawString(70, y_position, f"- {skill}")
        y_position -= 20
        if y_position < 50:  
            c.showPage()  
            y_position = height - 50  

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position - 20, "Experience:")
    c.setFont("Helvetica", 12)
    c.drawString(50, y_position - 40, details["Experience"])

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position - 80, "Education:")
    c.setFont("Helvetica", 12)
    c.drawString(50, y_position - 100, details["Education"])

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position - 140, "Certificates:")
    c.setFont("Helvetica", 12)
    certificates = details["Certificates"].split(", ")
    y_position -= 160
    for certificate in certificates:
        c.drawString(70, y_position, f"- {certificate}")
        y_position -= 20
        if y_position < 50:  
            c.showPage()  
            y_position = height - 50 

    c.save()
    return file_path



def generate_cover_letter(name, job_title, skills): 
    letter = f"Dear Hiring Manager,\n\nMy name is {name}, and I am excited to apply for the {job_title} position. With expertise in {', '.join(skills)}, I am confident in my ability to contribute effectively to your team.\n\nI look forward to the opportunity to discuss how my skills align with your needs.\n\nBest regards,\n{name}" 
    return letter

def main():
    print("Welcome to Smart Resume Analyzer!") 
    user_choice = input("Do you want to (1) Upload Resume or (2) Generate Resume? ")
    if user_choice == "1":
        file_path = input("Enter the path of your resume (DOCX format): ")
        if os.path.exists(file_path):
            text = extract_text_from_docx(file_path)
            score, feedback = analyze_resume(text)
            print(f"Resume Score: {score}/10")
            print(f"Feedback: {feedback}")
        else:
            print("File not found. Please check the path.")
    elif user_choice == "2":
        details = {
            "Name": input("Enter your name: "),
            "Job Title": input("Enter job title: "),
            "Skills": input("Enter your skills (comma-separated): "),
            "Experience": input("Enter your experience: "),
            "Education": input("Enter your education: "),
            "Email": input("Enter your email: "),
            "Phone": input("Enter your phone number: "), 
            "Objectives": input("Enter your objectives: "),
            "Certificates": input("Enter your certificates (comma-separated): ")
        }
        resume_path = generate_resume(details)
        print(f"Your auto-generated resume is saved as {resume_path}")
        generate_cover = input("Do you want to generate a cover letter? (yes/no): ")
        if generate_cover.lower() == "yes":
            cover_letter = generate_cover_letter(details["Name"], details["Job Title"], details["Skills"].split(", "))
            print("\nGenerated Cover Letter:\n")
            print(cover_letter)
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__": 
    main()

