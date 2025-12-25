"""
AI-Powered Resume Screening and Candidate Matching System

This module provides intelligent resume parsing and candidate-job matching
using NLP and machine learning techniques.
"""

import re
import os
from typing import List, Dict, Tuple
from pathlib import Path
import json

try:
    import spacy
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import PyPDF2
    from docx import Document
except ImportError:
    print("Please install required packages: pip install -r requirements.txt")
    raise


class ResumeParser:
    """Extracts structured information from resumes using NLP."""
    
    def __init__(self):
        try:
            # Load spaCy model (download if needed: python -m spacy download en_core_web_sm)
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not found. Using basic parsing.")
            self.nlp = None
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF, DOCX, or TXT files."""
        file_path = Path(file_path)
        ext = file_path.suffix.lower()
        
        if ext == '.pdf':
            return self._extract_from_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return self._extract_from_docx(file_path)
        elif ext == '.txt':
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return text
    
    def _extract_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file."""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
        return text
    
    def _extract_from_txt(self, file_path: Path) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT {file_path}: {e}")
            return ""
    
    def parse_resume(self, file_path: str) -> Dict:
        """Parse resume and extract structured information."""
        text = self.extract_text(file_path)
        
        # Extract key information
        resume_data = {
            'file_path': file_path,
            'name': self._extract_name(text),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'raw_text': text,
            'keywords': self._extract_keywords(text)
        }
        
        return resume_data
    
    def _extract_name(self, text: str) -> str:
        """Extract candidate name (first few lines often contain name)."""
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if len(line) > 3 and len(line) < 50:
                # Simple heuristic: name is usually in first few lines
                return line
        return "Unknown"
    
    def _extract_email(self, text: str) -> str:
        """Extract email address."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number."""
        phone_pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
        matches = re.findall(phone_pattern, text)
        return matches[0] if matches else ""
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills using NLP and keyword matching."""
        # Common technical skills database
        common_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'django', 'flask',
            'sql', 'postgresql', 'mysql', 'mongodb', 'aws', 'docker', 'kubernetes',
            'git', 'linux', 'html', 'css', 'typescript', 'angular', 'vue',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'agile', 'scrum', 'ci/cd', 'rest api', 'graphql', 'microservices'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill)
        
        # Use NLP to find noun phrases that might be skills
        if self.nlp:
            doc = self.nlp(text)
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.lower()
                if len(chunk_text) > 2 and len(chunk_text) < 30:
                    # Check if it looks like a skill
                    if any(keyword in chunk_text for keyword in ['programming', 'language', 'framework', 'tool']):
                        found_skills.append(chunk_text)
        
        return list(set(found_skills))  # Remove duplicates
    
    def _extract_experience(self, text: str) -> str:
        """Extract work experience section."""
        # Look for experience-related keywords
        experience_keywords = ['experience', 'work history', 'employment', 'career']
        lines = text.split('\n')
        
        experience_section = []
        in_experience = False
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in experience_keywords):
                in_experience = True
            if in_experience:
                experience_section.append(line)
                if len(experience_section) > 20:  # Limit section size
                    break
        
        return '\n'.join(experience_section[:15]) if experience_section else text[:500]
    
    def _extract_education(self, text: str) -> str:
        """Extract education section."""
        education_keywords = ['education', 'degree', 'university', 'college', 'bachelor', 'master', 'phd']
        lines = text.split('\n')
        
        education_section = []
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                # Include surrounding lines
                start = max(0, i - 2)
                end = min(len(lines), i + 5)
                education_section.extend(lines[start:end])
        
        return '\n'.join(education_section[:10]) if education_section else ""
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from resume."""
        if self.nlp:
            doc = self.nlp(text)
            keywords = []
            for token in doc:
                if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop:
                    if len(token.text) > 3:
                        keywords.append(token.text.lower())
            return list(set(keywords))[:50]  # Top 50 keywords
        else:
            # Fallback: simple word extraction
            words = re.findall(r'\b[a-z]{4,}\b', text.lower())
            return list(set(words))[:50]


class JobAnalyzer:
    """Analyzes job descriptions to extract requirements."""
    
    def __init__(self):
        self.parser = ResumeParser()
    
    def analyze_job(self, job_description: str) -> Dict:
        """Extract requirements from job description."""
        if isinstance(job_description, (Path, str)) and os.path.isfile(job_description):
            with open(job_description, 'r', encoding='utf-8') as f:
                job_description = f.read()
        
        return {
            'raw_text': job_description,
            'required_skills': self.parser._extract_skills(job_description),
            'keywords': self.parser._extract_keywords(job_description),
            'experience_required': self._extract_experience_years(job_description)
        }
    
    def _extract_experience_years(self, text: str) -> int:
        """Extract required years of experience."""
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience.*?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?.*?experience'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return int(matches[0])
        return 0


class ResumeMatcher:
    """Main class for matching candidates to job requirements."""
    
    def __init__(self):
        self.parser = ResumeParser()
        self.job_analyzer = JobAnalyzer()
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english'
        )
    
    def match_candidates(
        self,
        job_description: str,
        resume_paths: List[str],
        top_n: int = 10,
        min_score: float = 0.0
    ) -> List[Dict]:
        """
        Match candidates to job description.
        
        Args:
            job_description: Job description text or file path
            resume_paths: List of resume file paths
            top_n: Number of top candidates to return
            min_score: Minimum match score (0-1)
        
        Returns:
            List of candidate matches with scores
        """
        # Analyze job description
        job_data = self.job_analyzer.analyze_job(job_description)
        
        # Parse all resumes
        candidates = []
        for resume_path in resume_paths:
            try:
                candidate = self.parser.parse_resume(resume_path)
                candidates.append(candidate)
            except Exception as e:
                print(f"Error parsing {resume_path}: {e}")
                continue
        
        if not candidates:
            return []
        
        # Calculate match scores
        matches = []
        for candidate in candidates:
            score = self._calculate_match_score(job_data, candidate)
            matches.append({
                'name': candidate['name'],
                'email': candidate['email'],
                'file_path': candidate['file_path'],
                'match_score': round(score * 100, 2),
                'skills_match': self._calculate_skills_match(
                    job_data['required_skills'],
                    candidate['skills']
                ),
                'candidate_data': candidate
            })
        
        # Sort by match score
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Filter by minimum score and return top N
        filtered_matches = [
            m for m in matches 
            if m['match_score'] >= min_score * 100
        ]
        
        return filtered_matches[:top_n]
    
    def _calculate_match_score(self, job_data: Dict, candidate: Dict) -> float:
        """Calculate overall match score using TF-IDF and cosine similarity."""
        # Combine job description and candidate resume
        job_text = job_data['raw_text']
        candidate_text = candidate['raw_text']
        
        # Vectorize and calculate similarity
        try:
            vectors = self.vectorizer.fit_transform([job_text, candidate_text])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        except:
            # Fallback: simple keyword matching
            similarity = self._simple_keyword_match(
                job_data['keywords'],
                candidate['keywords']
            )
        
        # Weighted scoring
        skills_weight = 0.4
        experience_weight = 0.3
        semantic_weight = 0.3
        
        # Skills match
        skills_score = self._calculate_skills_match(
            job_data['required_skills'],
            candidate['skills']
        )
        
        # Experience match (simplified)
        experience_score = 1.0  # Could be enhanced with actual experience extraction
        
        # Final weighted score
        final_score = (
            skills_score * skills_weight +
            experience_score * experience_weight +
            similarity * semantic_weight
        )
        
        return min(final_score, 1.0)  # Cap at 1.0
    
    def _calculate_skills_match(self, required_skills: List[str], candidate_skills: List[str]) -> float:
        """Calculate skills match percentage."""
        if not required_skills:
            return 0.0
        
        required_lower = [s.lower() for s in required_skills]
        candidate_lower = [s.lower() for s in candidate_skills]
        
        matched = sum(1 for skill in required_lower if skill in candidate_lower)
        return matched / len(required_skills) if required_skills else 0.0
    
    def _simple_keyword_match(self, job_keywords: List[str], candidate_keywords: List[str]) -> float:
        """Simple keyword overlap calculation."""
        if not job_keywords or not candidate_keywords:
            return 0.0
        
        job_set = set(job_keywords)
        candidate_set = set(candidate_keywords)
        
        overlap = len(job_set & candidate_set)
        total = len(job_set | candidate_set)
        
        return overlap / total if total > 0 else 0.0


# Example usage
if __name__ == "__main__":
    matcher = ResumeMatcher()
    
    job_desc = """
    Python Developer Position
    
    We are looking for an experienced Python Developer to join our team.
    
    Requirements:
    - 3+ years of Python development experience
    - Experience with Django or Flask frameworks
    - Knowledge of REST APIs
    - Database experience (PostgreSQL preferred)
    - Familiarity with Git and version control
    - Strong problem-solving skills
    """
    
    # Example: match candidates (replace with actual resume paths)
    print("Resume Matcher initialized successfully!")
    print("Usage: matcher.match_candidates(job_description, resume_paths, top_n=10)")

