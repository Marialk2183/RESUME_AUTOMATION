"""
Command-line interface for the Resume Matching System
"""

import argparse
import json
from pathlib import Path
from resume_matcher import ResumeMatcher


def main():
    parser = argparse.ArgumentParser(
        description='AI-Powered Resume Screening and Candidate Matching'
    )
    parser.add_argument(
        '--job',
        type=str,
        required=True,
        help='Job description text or path to job description file'
    )
    parser.add_argument(
        '--resumes',
        type=str,
        required=True,
        help='Path to resume file or directory containing resumes'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=10,
        help='Number of top candidates to return (default: 10)'
    )
    parser.add_argument(
        '--min-score',
        type=float,
        default=0.0,
        help='Minimum match score threshold (0-100, default: 0)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path for JSON results (optional)'
    )
    
    args = parser.parse_args()
    
    # Initialize matcher
    print("Initializing Resume Matcher...")
    matcher = ResumeMatcher()
    
    # Get job description
    job_path = Path(args.job)
    if job_path.is_file():
        with open(job_path, 'r', encoding='utf-8') as f:
            job_description = f.read()
    else:
        job_description = args.job
    
    # Get resume paths
    resume_path = Path(args.resumes)
    resume_paths = []
    
    if resume_path.is_file():
        resume_paths = [str(resume_path)]
    elif resume_path.is_dir():
        # Find all resume files in directory
        extensions = ['.pdf', '.docx', '.doc', '.txt']
        for ext in extensions:
            resume_paths.extend(resume_path.glob(f'*{ext}'))
        resume_paths = [str(p) for p in resume_paths]
    else:
        print(f"Error: {args.resumes} is not a valid file or directory")
        return
    
    if not resume_paths:
        print(f"No resume files found in {args.resumes}")
        return
    
    print(f"\nFound {len(resume_paths)} resume(s)")
    print(f"Matching candidates to job description...\n")
    
    # Match candidates
    results = matcher.match_candidates(
        job_description=job_description,
        resume_paths=resume_paths,
        top_n=args.top,
        min_score=args.min_score / 100.0
    )
    
    # Display results
    print("=" * 80)
    print("MATCHING RESULTS")
    print("=" * 80)
    print(f"\nTop {len(results)} Candidates:\n")
    
    for i, candidate in enumerate(results, 1):
        print(f"{i}. {candidate['name']}")
        print(f"   Email: {candidate['email']}")
        print(f"   Match Score: {candidate['match_score']}%")
        print(f"   Skills Match: {candidate['skills_match']*100:.1f}%")
        print(f"   File: {candidate['file_path']}")
        print()
    
    # Save to file if requested
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()

