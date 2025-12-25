"""
Demo script to showcase the Resume Matching System
Run this to see the system in action with example data
"""

from resume_matcher import ResumeMatcher
import json


def create_demo_job_description():
    """Create a sample job description for demo."""
    return """
    Python Developer - Full Stack
    
    We are seeking an experienced Python Developer to join our dynamic team.
    
    Requirements:
    - 3+ years of professional Python development experience
    - Strong experience with Django or Flask web frameworks
    - Proficiency in REST API development
    - Database experience: PostgreSQL, MySQL, or MongoDB
    - Version control with Git
    - Experience with cloud platforms (AWS preferred)
    - Understanding of software development best practices
    - Strong problem-solving and debugging skills
    
    Nice to have:
    - Experience with Docker and containerization
    - Knowledge of CI/CD pipelines
    - Frontend experience (React, JavaScript)
    - Machine learning experience
    
    Education: Bachelor's degree in Computer Science or related field
    """


def create_demo_resume_text(name, skills, experience_years):
    """Create a sample resume text for demo."""
    return f"""
    {name}
    Email: {name.lower().replace(' ', '.')}@email.com
    Phone: (555) 123-4567
    
    PROFESSIONAL SUMMARY
    Experienced software developer with {experience_years} years of experience in Python development.
    Skilled in building scalable web applications and REST APIs.
    
    TECHNICAL SKILLS
    {', '.join(skills)}
    
    WORK EXPERIENCE
    
    Senior Python Developer | Tech Company Inc. | 2020 - Present
    - Developed and maintained Django-based web applications
    - Built RESTful APIs serving thousands of requests per day
    - Optimized database queries improving performance by 40%
    - Collaborated with cross-functional teams using Agile methodology
    
    Python Developer | StartupXYZ | 2018 - 2020
    - Built Flask applications for client projects
    - Integrated third-party APIs and payment gateways
    - Wrote unit tests achieving 85% code coverage
    
    EDUCATION
    Bachelor of Science in Computer Science
    University Name | 2018
    """


def run_demo():
    """Run a demonstration of the resume matching system."""
    print("=" * 80)
    print("AI-POWERED RESUME SCREENING DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Initialize matcher
    print("Initializing Resume Matcher...")
    matcher = ResumeMatcher()
    print("✓ System ready\n")
    
    # Create demo job description
    job_description = create_demo_job_description()
    print("Job Description:")
    print("-" * 80)
    print(job_description)
    print()
    
    # Create demo resumes
    demo_resumes = [
        {
            'name': 'John Smith',
            'skills': ['Python', 'Django', 'REST APIs', 'PostgreSQL', 'Git', 'AWS'],
            'experience': 4,
            'file': 'demo_resume_john.txt'
        },
        {
            'name': 'Sarah Johnson',
            'skills': ['Python', 'Flask', 'MySQL', 'JavaScript', 'React'],
            'experience': 2,
            'file': 'demo_resume_sarah.txt'
        },
        {
            'name': 'Mike Chen',
            'skills': ['Java', 'Spring Boot', 'MongoDB', 'Docker'],
            'experience': 5,
            'file': 'demo_resume_mike.txt'
        },
        {
            'name': 'Emily Davis',
            'skills': ['Python', 'Django', 'PostgreSQL', 'Git', 'AWS', 'Docker', 'CI/CD'],
            'experience': 3,
            'file': 'demo_resume_emily.txt'
        }
    ]
    
    # Create resume files
    resume_paths = []
    for resume_data in demo_resumes:
        resume_text = create_demo_resume_text(
            resume_data['name'],
            resume_data['skills'],
            resume_data['experience']
        )
        with open(resume_data['file'], 'w', encoding='utf-8') as f:
            f.write(resume_text)
        resume_paths.append(resume_data['file'])
        print(f"Created demo resume: {resume_data['name']}")
    
    print(f"\nProcessing {len(resume_paths)} resumes...\n")
    
    # Match candidates
    results = matcher.match_candidates(
        job_description=job_description,
        resume_paths=resume_paths,
        top_n=10,
        min_score=0.0
    )
    
    # Display results
    print("=" * 80)
    print("MATCHING RESULTS")
    print("=" * 80)
    print()
    
    for i, candidate in enumerate(results, 1):
        print(f"Rank #{i}: {candidate['name']}")
        print(f"  📧 Email: {candidate['email']}")
        print(f"  ⭐ Match Score: {candidate['match_score']}%")
        print(f"  🎯 Skills Match: {candidate['skills_match']*100:.1f}%")
        print(f"  📄 Resume: {candidate['file_path']}")
        
        # Show matched skills
        if candidate['candidate_data']['skills']:
            print(f"  💼 Skills: {', '.join(candidate['candidate_data']['skills'][:8])}")
        print()
    
    # Summary
    print("-" * 80)
    print("SUMMARY")
    print(f"Total candidates processed: {len(resume_paths)}")
    print(f"Top matches returned: {len(results)}")
    if results:
        avg_score = sum(c['match_score'] for c in results) / len(results)
        print(f"Average match score: {avg_score:.1f}%")
        print(f"Best match: {results[0]['name']} ({results[0]['match_score']}%)")
    
    print("\n" + "=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)
    
    # Cleanup demo files
    import os
    for file in resume_paths:
        if os.path.exists(file):
            os.remove(file)
    print("\nDemo files cleaned up.")


if __name__ == "__main__":
    try:
        run_demo()
    except Exception as e:
        print(f"\nError during demo: {e}")
        print("Make sure you have installed all requirements:")
        print("  pip install -r requirements.txt")
        print("  python -m spacy download en_core_web_sm")

