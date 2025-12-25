#!/bin/bash
# Build script for Vercel deployment
# Downloads spaCy model if not present

echo "Building for Vercel..."

# Download spaCy English model
python -m spacy download en_core_web_sm || echo "Warning: Could not download spaCy model"

echo "Build complete!"

