// Main JavaScript for Resume Matcher Application

const API_BASE = '/api';
let uploadedFiles = [];

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateCharCount();
});

function initializeEventListeners() {
    // File input
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');
    
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Job description character count
    const jobTextarea = document.getElementById('jobDescription');
    jobTextarea.addEventListener('input', updateCharCount);
}

function updateCharCount() {
    const textarea = document.getElementById('jobDescription');
    const charCount = document.getElementById('charCount');
    charCount.textContent = textarea.value.length;
}

// File Upload Functions
function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    uploadFiles(files);
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');
    
    const files = Array.from(e.dataTransfer.files);
    const validFiles = files.filter(file => {
        const ext = file.name.split('.').pop().toLowerCase();
        return ['pdf', 'docx', 'doc', 'txt'].includes(ext);
    });
    
    if (validFiles.length !== files.length) {
        alert('Some files were skipped. Only PDF, DOCX, DOC, and TXT files are supported.');
    }
    
    uploadFiles(validFiles);
}

async function uploadFiles(files) {
    const uploadedFilesContainer = document.getElementById('uploadedFiles');
    
    for (const file of files) {
        if (file.size > 16 * 1024 * 1024) {
            alert(`File ${file.name} is too large. Maximum size is 16MB.`);
            continue;
        }
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
            
            if (data.success) {
                uploadedFiles.push({
                    filename: data.filename,
                    originalName: file.name,
                    size: file.size,
                    type: file.type
                });
                
                displayUploadedFile(data.filename, file.name, file.size);
            } else {
                alert(`Error uploading ${file.name}: ${data.error}`);
            }
        } catch (error) {
            console.error('Upload error:', error);
            alert(`Error uploading ${file.name}: ${error.message}`);
        }
    }
}

function displayUploadedFile(filename, originalName, size) {
    const uploadedFilesContainer = document.getElementById('uploadedFiles');
    
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    fileItem.id = `file-${filename}`;
    
    const fileIcon = getFileIcon(originalName);
    const fileSize = formatFileSize(size);
    
    fileItem.innerHTML = `
        <div class="file-info-item">
            <div class="file-icon">${fileIcon}</div>
            <div class="file-details">
                <h4>${originalName}</h4>
                <p>${fileSize}</p>
            </div>
        </div>
        <div class="file-actions">
            <button class="btn-icon view" onclick="viewFileDetails('${filename}')" title="View Details">
                <i class="fas fa-eye"></i>
            </button>
            <button class="btn-icon delete" onclick="removeFile('${filename}')" title="Remove">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    
    uploadedFilesContainer.appendChild(fileItem);
}

function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const icons = {
        'pdf': '<i class="fas fa-file-pdf"></i>',
        'docx': '<i class="fas fa-file-word"></i>',
        'doc': '<i class="fas fa-file-word"></i>',
        'txt': '<i class="fas fa-file-alt"></i>'
    };
    return icons[ext] || '<i class="fas fa-file"></i>';
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

async function removeFile(filename) {
    if (!confirm('Remove this file from the list?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/delete-file`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename })
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            uploadedFiles = uploadedFiles.filter(f => f.filename !== filename);
            const fileItem = document.getElementById(`file-${filename}`);
            if (fileItem) {
                fileItem.remove();
            }
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Delete error:', error);
        let errorMsg = 'Error removing file. ';
        if (error.message.includes('Failed to fetch') || error.message.includes('ERR_CONNECTION')) {
            errorMsg += 'Could not connect to server. Please make sure the Flask server is running.';
        } else {
            errorMsg += error.message;
        }
        alert(errorMsg);
    }
}

async function viewFileDetails(filename) {
    try {
        const response = await fetch(`${API_BASE}/parse-resume`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename })
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            showCandidateModal(data.data, filename);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Parse error:', error);
        let errorMsg = 'Error parsing resume. ';
        if (error.message.includes('Failed to fetch') || error.message.includes('ERR_CONNECTION')) {
            errorMsg += 'Could not connect to server. Please make sure the Flask server is running.';
        } else {
            errorMsg += error.message;
        }
        alert(errorMsg);
    }
}

// Matching Function
async function matchCandidates() {
    const jobDescription = document.getElementById('jobDescription').value.trim();
    const topN = parseInt(document.getElementById('topN').value);
    const minScore = parseInt(document.getElementById('minScore').value);
    
    if (!jobDescription) {
        alert('Please enter a job description first.');
        return;
    }
    
    if (uploadedFiles.length === 0) {
        alert('Please upload at least one resume.');
        return;
    }
    
    // Show loading
    const loading = document.getElementById('loading');
    const resultsContainer = document.getElementById('resultsContainer');
    const matchBtn = document.getElementById('matchBtn');
    
    loading.style.display = 'block';
    resultsContainer.innerHTML = '';
    matchBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/match`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                job_description: jobDescription,
                filenames: uploadedFiles.map(f => f.filename),
                top_n: topN,
                min_score: minScore
            })
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.results);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Match error:', error);
        let errorMsg = 'Error matching candidates. ';
        if (error.message.includes('Failed to fetch') || error.message.includes('ERR_CONNECTION')) {
            errorMsg += 'Could not connect to server. Please make sure the Flask server is running on http://localhost:5000';
        } else {
            errorMsg += error.message;
        }
        alert(errorMsg);
    } finally {
        loading.style.display = 'none';
        matchBtn.disabled = false;
    }
}

function displayResults(results) {
    const resultsContainer = document.getElementById('resultsContainer');
    
    // Store results globally
    currentResults = results;
    
    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search"></i>
                <p>No candidates matched the criteria. Try lowering the minimum score threshold.</p>
            </div>
        `;
        document.getElementById('resultsActions').style.display = 'none';
        document.getElementById('statsPanel').style.display = 'none';
        return;
    }
    
    // Show actions and stats
    document.getElementById('resultsActions').style.display = 'block';
    updateStatistics(results);
    updateSearchFilters(results);
    
    let html = `
        <div class="results-header" style="margin-bottom: 20px; padding: 15px; background: #f8fafc; border-radius: 8px;">
            <h3 style="margin-bottom: 5px;">Found ${results.length} Matching Candidate${results.length !== 1 ? 's' : ''}</h3>
            <p style="color: #64748b; font-size: 0.9rem;">Sorted by match score (highest first)</p>
        </div>
        <div class="results-grid">
    `;
    
    results.forEach((candidate, index) => {
        const rank = index + 1;
        const scoreColor = getScoreColor(candidate.match_score);
        
        html += `
            <div class="result-card" onclick="showCandidateModalFull(${JSON.stringify(candidate).replace(/"/g, '&quot;')})">
                <div class="card-header">
                    <div>
                        <div class="candidate-name">#${rank} ${candidate.name || 'Unknown'}</div>
                        <div class="candidate-email">${candidate.email || 'No email'}</div>
                    </div>
                    <div class="match-score">
                        <div class="score-value" style="color: ${scoreColor}">${candidate.match_score}%</div>
                        <div class="score-label">Match</div>
                    </div>
                </div>
                
                <div class="score-bar">
                    <div class="score-fill" style="width: ${candidate.match_score}%; background: ${scoreColor};"></div>
                </div>
                
                <div class="card-stats">
                    <div class="stat-item">
                        <div class="stat-value">${candidate.skills_match}%</div>
                        <div class="stat-label">Skills</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${candidate.skills?.length || 0}</div>
                        <div class="stat-label">Skills Found</div>
                    </div>
                </div>
                
                ${candidate.skills && candidate.skills.length > 0 ? `
                    <div class="skills-preview">
                        <h4>Key Skills</h4>
                        <div class="skills-tags">
                            ${candidate.skills.slice(0, 6).map(skill => 
                                `<span class="skill-tag">${skill}</span>`
                            ).join('')}
                            ${candidate.skills.length > 6 ? `<span class="skill-tag">+${candidate.skills.length - 6} more</span>` : ''}
                        </div>
                    </div>
                ` : ''}
                
                <button class="view-details-btn" onclick="event.stopPropagation(); showCandidateModalFull(${JSON.stringify(candidate).replace(/"/g, '&quot;')})">
                    <i class="fas fa-info-circle"></i> View Full Details
                </button>
            </div>
        `;
    });
    
    html += '</div>';
    resultsContainer.innerHTML = html;
    
    // Animate score bars
    setTimeout(() => {
        document.querySelectorAll('.score-fill').forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
    }, 100);
    
    // Initialize search/filter
    initializeSearchFilters();
}

function getScoreColor(score) {
    if (score >= 80) return '#10b981'; // Green
    if (score >= 60) return '#6366f1'; // Blue/Purple
    if (score >= 40) return '#f59e0b'; // Orange
    return '#ef4444'; // Red
}

// Modal Functions
function showCandidateModal(candidateData, filename) {
    const modal = document.getElementById('candidateModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <h2>${candidateData.name || 'Unknown Candidate'}</h2>
        <div class="modal-section">
            <h3>Contact Information</h3>
            <p><strong>Email:</strong> ${candidateData.email || 'Not provided'}</p>
            <p><strong>Phone:</strong> ${candidateData.phone || 'Not provided'}</p>
        </div>
        <div class="modal-section">
            <h3>Skills</h3>
            <div class="skills-tags">
                ${candidateData.skills && candidateData.skills.length > 0 
                    ? candidateData.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')
                    : '<p>No skills extracted</p>'}
            </div>
        </div>
        <div class="modal-section">
            <h3>Experience</h3>
            <p>${candidateData.experience || 'Not available'}</p>
        </div>
        <div class="modal-section">
            <h3>Education</h3>
            <p>${candidateData.education || 'Not available'}</p>
        </div>
    `;
    
    modal.style.display = 'block';
}

function showCandidateModalFull(candidate) {
    const modal = document.getElementById('candidateModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <h2>${candidate.name || 'Unknown Candidate'}</h2>
        <div style="margin-bottom: 20px;">
            <div style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; border-radius: 8px; font-size: 1.5rem; font-weight: 700;">
                ${candidate.match_score}% Match
            </div>
        </div>
        <div class="modal-section">
            <h3>Contact Information</h3>
            <p><strong>Email:</strong> ${candidate.email || 'Not provided'}</p>
        </div>
        <div class="modal-section">
            <h3>Match Statistics</h3>
            <p><strong>Skills Match:</strong> ${candidate.skills_match}%</p>
            <p><strong>Overall Match:</strong> ${candidate.match_score}%</p>
        </div>
        <div class="modal-section">
            <h3>Skills</h3>
            <div class="skills-tags">
                ${candidate.skills && candidate.skills.length > 0 
                    ? candidate.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')
                    : '<p>No skills found</p>'}
            </div>
        </div>
        ${candidate.experience ? `
            <div class="modal-section">
                <h3>Experience</h3>
                <p>${candidate.experience}</p>
            </div>
        ` : ''}
        ${candidate.education ? `
            <div class="modal-section">
                <h3>Education</h3>
                <p>${candidate.education}</p>
            </div>
        ` : ''}
    `;
    
    modal.style.display = 'block';
}

// closeModal function is now defined above with parameter support

// Close modal when clicking outside
window.onclick = function(event) {
    const modals = ['candidateModal', 'analyticsModal', 'comparisonModal'];
    modals.forEach(modalId => {
        const modal = document.getElementById(modalId);
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Store current results globally
let currentResults = [];

// Initialize search/filter event listeners after results are displayed
function initializeSearchFilters() {
    const searchInput = document.getElementById('searchInput');
    const filterScore = document.getElementById('filterScore');
    const sortBy = document.getElementById('sortBy');
    
    if (searchInput) searchInput.oninput = () => filterAndSearch();
    if (filterScore) filterScore.onchange = () => filterAndSearch();
    if (sortBy) sortBy.onchange = () => filterAndSearch();
}

// Statistics Functions
function updateStatistics(results) {
    if (results.length === 0) {
        document.getElementById('statsPanel').style.display = 'none';
        return;
    }
    
    document.getElementById('statsPanel').style.display = 'grid';
    
    const total = results.length;
    const avgScore = results.reduce((sum, r) => sum + r.match_score, 0) / total;
    const topScore = Math.max(...results.map(r => r.match_score));
    const totalSkills = new Set(results.flatMap(r => r.skills || [])).size;
    
    document.getElementById('statTotal').textContent = total;
    document.getElementById('statAvgScore').textContent = avgScore.toFixed(1) + '%';
    document.getElementById('statTopScore').textContent = topScore.toFixed(1) + '%';
    document.getElementById('statTotalSkills').textContent = totalSkills;
}

// Search and Filter Functions
function updateSearchFilters(results) {
    const compareSelect1 = document.getElementById('compareCandidate1');
    const compareSelect2 = document.getElementById('compareCandidate2');
    
    // Clear and populate comparison selects
    compareSelect1.innerHTML = '<option value="">Select first candidate...</option>';
    compareSelect2.innerHTML = '<option value="">Select second candidate...</option>';
    
    results.forEach((candidate, index) => {
        const option1 = document.createElement('option');
        option1.value = index;
        option1.textContent = `${candidate.name} (${candidate.match_score}%)`;
        compareSelect1.appendChild(option1);
        
        const option2 = document.createElement('option');
        option2.value = index;
        option2.textContent = `${candidate.name} (${candidate.match_score}%)`;
        compareSelect2.appendChild(option2);
    });
}

function filterAndSearch() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filterScore = parseInt(document.getElementById('filterScore').value) || 0;
    const sortBy = document.getElementById('sortBy').value;
    
    let filtered = currentResults.filter(candidate => {
        const matchesSearch = !searchTerm || 
            candidate.name.toLowerCase().includes(searchTerm) ||
            candidate.email.toLowerCase().includes(searchTerm) ||
            (candidate.skills || []).some(skill => skill.toLowerCase().includes(searchTerm));
        
        const matchesScore = candidate.match_score >= filterScore;
        
        return matchesSearch && matchesScore;
    });
    
    // Sort
    if (sortBy === 'name') {
        filtered.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
    } else if (sortBy === 'skills') {
        filtered.sort((a, b) => (b.skills?.length || 0) - (a.skills?.length || 0));
    } else {
        filtered.sort((a, b) => b.match_score - a.match_score);
    }
    
    // Re-display filtered results
    originalDisplayResults(filtered);
}

// Export Functions
async function exportToCSV() {
    if (currentResults.length === 0) {
        alert('No results to export');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ results: currentResults })
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Download CSV
            const blob = new Blob([data.csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            alert(`Exported ${currentResults.length} candidates to ${data.filename}`);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Export error:', error);
        alert(`Error exporting: ${error.message}`);
    }
}

// Analytics Functions
function showAnalytics() {
    if (currentResults.length === 0) {
        alert('No results to analyze');
        return;
    }
    
    const modal = document.getElementById('analyticsModal');
    const body = document.getElementById('analyticsBody');
    
    // Calculate analytics
    const scores = currentResults.map(r => r.match_score);
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
    const maxScore = Math.max(...scores);
    const minScore = Math.min(...scores);
    
    // Score distribution
    const excellent = scores.filter(s => s >= 80).length;
    const good = scores.filter(s => s >= 60 && s < 80).length;
    const fair = scores.filter(s => s >= 40 && s < 60).length;
    const poor = scores.filter(s => s < 40).length;
    
    // Skills analysis
    const allSkills = currentResults.flatMap(r => r.skills || []);
    const skillCounts = {};
    allSkills.forEach(skill => {
        skillCounts[skill] = (skillCounts[skill] || 0) + 1;
    });
    const topSkills = Object.entries(skillCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    
    body.innerHTML = `
        <div class="analytics-grid">
            <div class="chart-container">
                <div class="chart-title">Score Distribution</div>
                <div class="score-distribution">
                    <div class="dist-item">
                        <div class="dist-value" style="color: #10b981;">${excellent}</div>
                        <div class="dist-label">Excellent (80%+)</div>
                    </div>
                    <div class="dist-item">
                        <div class="dist-value" style="color: #6366f1;">${good}</div>
                        <div class="dist-label">Good (60-79%)</div>
                    </div>
                    <div class="dist-item">
                        <div class="dist-value" style="color: #f59e0b;">${fair}</div>
                        <div class="dist-label">Fair (40-59%)</div>
                    </div>
                    <div class="dist-item">
                        <div class="dist-value" style="color: #ef4444;">${poor}</div>
                        <div class="dist-label">Poor (<40%)</div>
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">Score Statistics</div>
                <div class="chart-bar">
                    <div class="chart-label">Average</div>
                    <div class="chart-bar-fill" style="width: ${avgScore}%;">${avgScore.toFixed(1)}%</div>
                </div>
                <div class="chart-bar">
                    <div class="chart-label">Highest</div>
                    <div class="chart-bar-fill" style="width: ${maxScore}%; background: linear-gradient(90deg, #10b981, #059669);">${maxScore.toFixed(1)}%</div>
                </div>
                <div class="chart-bar">
                    <div class="chart-label">Lowest</div>
                    <div class="chart-bar-fill" style="width: ${minScore}%; background: linear-gradient(90deg, #f59e0b, #d97706);">${minScore.toFixed(1)}%</div>
                </div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">Top Skills Found</div>
                ${topSkills.map(([skill, count]) => `
                    <div class="chart-bar">
                        <div class="chart-label">${skill}</div>
                        <div class="chart-bar-fill" style="width: ${(count / currentResults.length) * 100}%;">${count}</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    modal.style.display = 'block';
    
    // Animate bars
    setTimeout(() => {
        document.querySelectorAll('#analyticsBody .chart-bar-fill').forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
    }, 100);
}

// Comparison Functions
function showComparison() {
    const modal = document.getElementById('comparisonModal');
    modal.style.display = 'block';
}

function performComparison() {
    const index1 = parseInt(document.getElementById('compareCandidate1').value);
    const index2 = parseInt(document.getElementById('compareCandidate2').value);
    
    if (index1 === '' || index2 === '' || index1 === index2) {
        alert('Please select two different candidates to compare');
        return;
    }
    
    const candidate1 = currentResults[index1];
    const candidate2 = currentResults[index2];
    
    const body = document.getElementById('comparisonBody');
    
    const getComparisonBadge = (val1, val2, higherIsBetter = true) => {
        if (val1 > val2) return higherIsBetter ? 'badge-better' : 'badge-worse';
        if (val1 < val2) return higherIsBetter ? 'badge-worse' : 'badge-better';
        return 'badge-same';
    };
    
    body.innerHTML = `
        <table class="comparison-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>${candidate1.name}</th>
                    <th>${candidate2.name}</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Match Score</strong></td>
                    <td>
                        ${candidate1.match_score}%
                        <span class="comparison-badge ${getComparisonBadge(candidate1.match_score, candidate2.match_score)}">
                            ${candidate1.match_score > candidate2.match_score ? 'Better' : candidate1.match_score < candidate2.match_score ? 'Worse' : 'Same'}
                        </span>
                    </td>
                    <td>
                        ${candidate2.match_score}%
                        <span class="comparison-badge ${getComparisonBadge(candidate2.match_score, candidate1.match_score)}">
                            ${candidate2.match_score > candidate1.match_score ? 'Better' : candidate2.match_score < candidate1.match_score ? 'Worse' : 'Same'}
                        </span>
                    </td>
                </tr>
                <tr>
                    <td><strong>Skills Match</strong></td>
                    <td>${candidate1.skills_match}%</td>
                    <td>${candidate2.skills_match}%</td>
                </tr>
                <tr>
                    <td><strong>Skills Count</strong></td>
                    <td>
                        ${candidate1.skills?.length || 0}
                        <span class="comparison-badge ${getComparisonBadge(candidate1.skills?.length || 0, candidate2.skills?.length || 0)}">
                            ${candidate1.skills?.length > candidate2.skills?.length ? 'More' : candidate1.skills?.length < candidate2.skills?.length ? 'Less' : 'Same'}
                        </span>
                    </td>
                    <td>${candidate2.skills?.length || 0}</td>
                </tr>
                <tr>
                    <td><strong>Email</strong></td>
                    <td>${candidate1.email || 'N/A'}</td>
                    <td>${candidate2.email || 'N/A'}</td>
                </tr>
                <tr>
                    <td><strong>Skills</strong></td>
                    <td>
                        <div class="skills-tags">
                            ${(candidate1.skills || []).slice(0, 10).map(s => `<span class="skill-tag">${s}</span>`).join('')}
                        </div>
                    </td>
                    <td>
                        <div class="skills-tags">
                            ${(candidate2.skills || []).slice(0, 10).map(s => `<span class="skill-tag">${s}</span>`).join('')}
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    `;
}

function closeModal(modalId = 'candidateModal') {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

