# Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download spaCy English Model
```bash
python -m spacy download en_core_web_sm
```

That's it! You're ready to go.

## 🌐 Running the Web Application (Recommended)

### Start the Server
```bash
python run_app.py
```

### Open in Browser
Navigate to: **http://localhost:5000**

### Using the Web Interface
1. **Enter Job Description**: Paste or type the job requirements in the text area
2. **Upload Resumes**: 
   - Drag & drop PDF/DOCX files into the upload area, OR
   - Click to browse and select files
3. **Match Candidates**: Click "Find Best Matches" button
4. **View Results**: See ranked candidates with visual match scores
5. **View Details**: Click on any candidate card to see full profile

## Running the Demo (2 minutes)

### Option 1: Run the Demo Script
```bash
python demo_example.py
```

This will:
- Create sample resumes
- Match them against a sample job description
- Show ranked results
- Clean up demo files

### Option 2: Use with Your Own Data

#### Create a job description file (`job.txt`):
```
Python Developer Position

We need a Python developer with 3+ years experience.
Required: Python, Django, PostgreSQL, REST APIs
```

#### Prepare resume files:
- Place PDF, DOCX, or TXT resumes in a folder (e.g., `resumes/`)

#### Run the matcher:
```bash
python main.py --job job.txt --resumes resumes/ --top 5
```

## Example Output

```
MATCHING RESULTS
================================================================================

Top 5 Candidates:

1. John Smith
   Email: john.smith@email.com
   Match Score: 87.5%
   Skills Match: 80.0%
   File: resumes/john_smith.pdf

2. Emily Davis
   Email: emily.davis@email.com
   Match Score: 82.3%
   Skills Match: 75.0%
   File: resumes/emily_davis.docx
...
```

## Using in Python Code

```python
from resume_matcher import ResumeMatcher

# Initialize
matcher = ResumeMatcher()

# Match candidates
results = matcher.match_candidates(
    job_description="Your job description here...",
    resume_paths=['resume1.pdf', 'resume2.pdf'],
    top_n=10
)

# Process results
for candidate in results:
    print(f"{candidate['name']}: {candidate['match_score']}% match")
```

## Troubleshooting

### Issue: "spacy model not found"
**Solution**: Run `python -m spacy download en_core_web_sm`

### Issue: "Cannot read PDF"
**Solution**: Make sure PyPDF2 is installed: `pip install PyPDF2`

### Issue: "Cannot read DOCX"
**Solution**: Make sure python-docx is installed: `pip install python-docx`

### Issue: Low match scores
**Solution**: 
- Ensure job description is detailed
- Check that resumes contain relevant keywords
- Adjust `--min-score` threshold if needed

## Next Steps

1. **Read INTERVIEW_PREP.md** - Complete answers to interview questions
2. **Review README.md** - Full project documentation
3. **Customize the code** - Add your own features
4. **Test with real data** - Use actual resumes and job descriptions

## Tips for Interview Demo

1. **Prepare sample data**: Have 3-5 sample resumes ready
2. **Have a job description**: Prepare a realistic job posting
3. **Practice the demo**: Run `demo_example.py` a few times
4. **Know the numbers**: Be ready to explain match scores
5. **Show the code**: Be prepared to walk through key functions

Good luck with your interview! 🚀

