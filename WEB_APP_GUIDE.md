# Web Application User Guide

## 🎨 Features Overview

### 1. **Modern, Professional Interface**
   - Clean, intuitive design
   - Gradient backgrounds and smooth animations
   - Responsive layout (works on desktop, tablet, and mobile)
   - Professional color scheme

### 2. **Easy File Upload**
   - **Drag & Drop**: Simply drag resume files into the upload area
   - **Click to Browse**: Traditional file picker also available
   - **Multiple Files**: Upload multiple resumes at once
   - **File Management**: View and remove uploaded files
   - **Supported Formats**: PDF, DOCX, DOC, TXT

### 3. **Job Description Input**
   - Large text area for pasting job descriptions
   - Character counter
   - Auto-saves as you type

### 4. **Visual Results Display**
   - **Match Score Cards**: Each candidate shown in a beautiful card
   - **Color-Coded Scores**: 
     - 🟢 Green (80%+): Excellent match
     - 🔵 Blue/Purple (60-79%): Good match
     - 🟠 Orange (40-59%): Moderate match
     - 🔴 Red (<40%): Low match
   - **Progress Bars**: Visual representation of match percentage
   - **Skills Display**: Shows matched skills as tags
   - **Statistics**: Skills match percentage and count

### 5. **Detailed Candidate Profiles**
   - Click any candidate card to view full details
   - Modal popup with complete information:
     - Contact details
     - All extracted skills
     - Experience summary
     - Education details
     - Match breakdown

### 6. **Customizable Matching**
   - **Top N Results**: Choose how many candidates to show (5, 10, 20, 50)
   - **Minimum Score**: Filter out low-scoring candidates
   - Real-time processing feedback

## 📱 How to Use

### Step 1: Enter Job Description
1. Scroll to the "Enter Job Description" section
2. Paste or type the job requirements
3. Include:
   - Required skills
   - Experience level
   - Education requirements
   - Any other relevant details

**Tip**: The more detailed the job description, the better the matching!

### Step 2: Upload Resumes
1. Go to the "Upload Candidate Resumes" section
2. **Option A - Drag & Drop**:
   - Drag resume files from your computer
   - Drop them into the upload area
3. **Option B - Browse**:
   - Click "browse files" or click the upload area
   - Select files from file picker
4. Uploaded files will appear below with:
   - File icon
   - File name
   - File size
   - View and delete buttons

**Supported Formats**:
- PDF (`.pdf`)
- Word Documents (`.docx`, `.doc`)
- Text Files (`.txt`)

**File Size Limit**: 16MB per file

### Step 3: Configure Matching
1. **Top Results**: Select how many top candidates to show
2. **Min Score**: Set minimum match percentage (0-100%)
   - 0% = Show all candidates
   - 50% = Only show candidates with 50%+ match
   - 80% = Only show excellent matches

### Step 4: Find Matches
1. Click the **"Find Best Matches"** button
2. Wait for processing (you'll see a loading indicator)
3. Results will appear automatically

### Step 5: Review Results
1. **Browse Cards**: Scroll through candidate cards
2. **Match Scores**: See percentage match at a glance
3. **Skills**: View matched skills for each candidate
4. **View Details**: Click any card or "View Full Details" button
5. **Sort**: Results are automatically sorted by match score (highest first)

## 🎯 Understanding Match Scores

### Score Breakdown
- **Overall Match Score**: Combined score based on:
  - Skills match (40% weight)
  - Experience match (30% weight)
  - Semantic similarity (30% weight)

### What Makes a Good Match?
- **High Skills Match**: Candidate has most/all required skills
- **Relevant Experience**: Experience aligns with job requirements
- **Semantic Match**: Resume content is contextually similar to job description

### Score Interpretation
- **90-100%**: Excellent match - Strong candidate
- **70-89%**: Good match - Worth interviewing
- **50-69%**: Moderate match - May have potential
- **Below 50%**: Low match - Likely not a good fit

## 💡 Tips for Best Results

1. **Detailed Job Description**: Include specific skills, technologies, and requirements
2. **Multiple Resumes**: Upload 10+ resumes for better comparison
3. **Adjust Thresholds**: Start with 0% min score, then increase to filter
4. **Review Top Matches**: Focus on candidates with 70%+ match scores
5. **Check Details**: Always review full candidate profiles before making decisions

## 🔧 Troubleshooting

### Files Not Uploading
- Check file size (must be < 16MB)
- Verify file format (PDF, DOCX, DOC, TXT only)
- Try refreshing the page

### Low Match Scores
- Ensure job description is detailed
- Check that resumes contain relevant keywords
- Lower the minimum score threshold
- Some resumes may genuinely not be a good fit

### Processing Takes Too Long
- Large files or many files may take longer
- Normal processing time: 5-30 seconds
- If stuck, refresh and try again

### Results Not Showing
- Check that job description is entered
- Verify at least one resume is uploaded
- Check browser console for errors (F12)

## 🚀 Advanced Features

### Batch Processing
- Upload multiple resumes at once
- Process all candidates simultaneously
- Compare all candidates side-by-side

### Export Results (Coming Soon)
- Export to CSV/Excel
- Save match reports
- Share results with team

## 📊 Example Workflow

1. **Recruiter receives 50 resumes** for a Python Developer position
2. **Copies job description** from job posting
3. **Uploads all 50 resumes** via drag & drop (takes 2 minutes)
4. **Clicks "Find Best Matches"** (processes in 20 seconds)
5. **Reviews top 10 candidates** with 75%+ match scores
6. **Clicks on top 3 candidates** to view full profiles
7. **Schedules interviews** with best matches
8. **Time saved**: 4 hours of manual screening → 5 minutes with AI

## 🎓 Best Practices

1. **Start Broad**: Begin with 0% minimum score to see all candidates
2. **Narrow Down**: Increase minimum score to focus on best matches
3. **Review Details**: Always check full profiles, don't rely only on scores
4. **Combine with Human Judgment**: Use AI as a tool, not a replacement
5. **Iterate**: Adjust job description and try again if needed

---

**Need Help?** Check the main README.md or INTERVIEW_PREP.md for technical details.

