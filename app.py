"""
Flask Web Application for AI-Powered Resume Screening
"""

from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from pathlib import Path
import json
import traceback

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
# Use /tmp for Vercel (serverless) or 'uploads' for local development
UPLOAD_FOLDER = '/tmp/uploads' if os.environ.get('VERCEL') else 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
MAX_FILE_SIZE = 4 * 1024 * 1024  # 4MB (Vercel limit is 4.5MB for serverless)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize matcher (lazy loading)
matcher = None

def get_matcher():
    """Lazy load matcher to avoid loading on startup."""
    global matcher
    if matcher is None:
        try:
            from resume_matcher import ResumeMatcher
            matcher = ResumeMatcher()
        except Exception as e:
            app.logger.error(f'Error initializing matcher: {str(e)}')
            raise
    return matcher

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Return favicon to prevent 404 errors."""
    return Response(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🧠</text></svg>',
        mimetype='image/svg+xml'
    )

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'File uploaded successfully'
        })
    
    return jsonify({'error': 'Invalid file type. Allowed: PDF, DOCX, DOC, TXT'}), 400

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    """Parse a single resume and return extracted data."""
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': 'Filename required'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        try:
            from resume_matcher import ResumeMatcher
            matcher = get_matcher()
            candidate = matcher.parser.parse_resume(filepath)
            
            # Return structured data
            return jsonify({
                'success': True,
                'data': {
                    'name': candidate.get('name', 'Unknown'),
                    'email': candidate.get('email', ''),
                    'phone': candidate.get('phone', ''),
                    'skills': candidate.get('skills', []),
                    'experience': candidate.get('experience', '')[:500],  # Limit length
                    'education': candidate.get('education', ''),
                    'keywords': candidate.get('keywords', [])[:20]  # Top 20 keywords
                }
            })
        except ImportError as e:
            return jsonify({'error': f'Module import error: {str(e)}'}), 500
        except Exception as e:
            app.logger.error(f'Parse error: {str(e)}\n{traceback.format_exc()}')
            return jsonify({'error': f'Error parsing resume: {str(e)}'}), 500
    except Exception as e:
        app.logger.error(f'Request error: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': f'Request error: {str(e)}'}), 500

@app.route('/api/match', methods=['POST'])
def match_candidates():
    """Match candidates to job description."""
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        job_description = data.get('job_description', '')
        filenames = data.get('filenames', [])
        top_n = data.get('top_n', 10)
        min_score = data.get('min_score', 0) / 100.0  # Convert to 0-1
        
        if not job_description:
            return jsonify({'error': 'Job description required'}), 400
        
        if not filenames:
            return jsonify({'error': 'At least one resume required'}), 400
        
        # Build full file paths
        resume_paths = [
            os.path.join(app.config['UPLOAD_FOLDER'], fname)
            for fname in filenames
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        ]
        
        if not resume_paths:
            return jsonify({'error': 'No valid resume files found'}), 400
        
        try:
            from resume_matcher import ResumeMatcher
            matcher = get_matcher()
            results = matcher.match_candidates(
                job_description=job_description,
                resume_paths=resume_paths,
                top_n=top_n,
                min_score=min_score
            )
            
            # Format results for frontend
            formatted_results = []
            for result in results:
                candidate_data = result.get('candidate_data', {})
                formatted_results.append({
                    'name': result.get('name', 'Unknown'),
                    'email': result.get('email', ''),
                    'match_score': result.get('match_score', 0),
                    'skills_match': round(result.get('skills_match', 0) * 100, 1),
                    'skills': candidate_data.get('skills', []),
                    'experience': candidate_data.get('experience', '')[:300],
                    'education': candidate_data.get('education', '')[:200],
                    'filename': os.path.basename(result.get('file_path', ''))
                })
            
            return jsonify({
                'success': True,
                'results': formatted_results,
                'total_matched': len(formatted_results)
            })
        except ImportError as e:
            return jsonify({'error': f'Module import error: {str(e)}'}), 500
        except Exception as e:
            app.logger.error(f'Match error: {str(e)}\n{traceback.format_exc()}')
            return jsonify({'error': f'Error matching candidates: {str(e)}'}), 500
    except Exception as e:
        app.logger.error(f'Request error: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': f'Request error: {str(e)}'}), 500

@app.route('/api/delete-file', methods=['POST'])
def delete_file():
    """Delete uploaded file."""
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': 'Filename required'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return jsonify({'success': True, 'message': 'File deleted'})
            except Exception as e:
                app.logger.error(f'Delete error: {str(e)}')
                return jsonify({'error': str(e)}), 500
        
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        app.logger.error(f'Request error: {str(e)}')
        return jsonify({'error': f'Request error: {str(e)}'}), 500

@app.route('/api/export', methods=['POST'])
def export_results():
    """Export results to CSV format."""
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        results = data.get('results', [])
        
        if not results:
            return jsonify({'error': 'No results to export'}), 400
        
        # Generate CSV
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'Rank', 'Name', 'Email', 'Match Score (%)', 'Skills Match (%)', 
            'Skills Count', 'Skills', 'Experience Preview', 'Education Preview'
        ])
        
        # Data rows
        for i, result in enumerate(results, 1):
            writer.writerow([
                i,
                result.get('name', 'Unknown'),
                result.get('email', ''),
                result.get('match_score', 0),
                result.get('skills_match', 0),
                len(result.get('skills', [])),
                ', '.join(result.get('skills', [])),
                result.get('experience', '')[:100],
                result.get('education', '')[:100]
            ])
        
        csv_string = output.getvalue()
        output.close()
        
        return jsonify({
            'success': True,
            'csv': csv_string,
            'filename': f'resume_matches_{uuid.uuid4().hex[:8]}.csv'
        })
    except Exception as e:
        app.logger.error(f'Export error: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': f'Export error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'Resume Matcher API'})

if __name__ == '__main__':
    print("Starting Resume Matching Web Application...")
    print("Open http://localhost:5000 in your browser")
    try:
        app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

