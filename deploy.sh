#!/bin/bash

# =========================================
# Deploy to Render.com Helper Script
# =========================================

set -e

echo "========================================="
echo "🚀 Render.com Deployment Helper"
echo "========================================="
echo ""

# Check git
if ! command -v git &> /dev/null; then
    echo "❌ Git not installed. Please install git first."
    exit 1
fi

# Check if in git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository. Initialize with: git init"
    exit 1
fi

echo "✅ Git repository detected"
echo ""

# Step 1: Check model exists
if [ ! -d "serving_model/rfahrur6045-pipeline" ]; then
    echo "❌ Error: serving_model/rfahrur6045-pipeline/ directory not found"
    echo "   Make sure model is generated and in correct directory"
    exit 1
fi

MODEL_VERSIONS=$(ls -d serving_model/rfahrur6045-pipeline/*/ 2>/dev/null | wc -l)
if [ "$MODEL_VERSIONS" -eq 0 ]; then
    echo "❌ Error: No model versions found in serving_model/rfahrur6045-pipeline/"
    exit 1
fi

echo "✅ Found $MODEL_VERSIONS model version(s)"
LATEST_VERSION=$(ls -td serving_model/rfahrur6045-pipeline/*/ | head -1 | xargs basename)
echo "   Latest version: $LATEST_VERSION"
echo ""

# Step 2: Check Dockerfile
if [ ! -f "serving/Dockerfile" ]; then
    echo "❌ Error: serving/Dockerfile not found"
    exit 1
fi
echo "✅ Dockerfile found at serving/Dockerfile"
echo ""

# Step 3: Check render.yaml
if [ ! -f "render.yaml" ]; then
    echo "❌ Error: render.yaml not found"
    exit 1
fi
echo "✅ render.yaml found"
echo ""

# Step 4: Git operations
echo "📦 Preparing for deployment..."
git add .
git status --short | head -10

echo ""
read -p "✅ Commit and push? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "📝 Commit message (default: 'Deploy model update'): " COMMIT_MSG
    COMMIT_MSG=${COMMIT_MSG:-"Deploy model update"}
    
    git commit -m "$COMMIT_MSG" || echo "⚠️  Nothing to commit"
    git push origin main
    
    echo ""
    echo "========================================="
    echo "✅ Code pushed to GitHub!"
    echo "========================================="
    echo ""
    echo "🎯 Next steps:"
    echo "1. Go to: https://dashboard.render.com/"
    echo "2. Click: New + → Web Service"
    echo "3. Select: Public Git repository"
    echo "4. Enter: https://github.com/YOUR_USERNAME/YOUR_REPO"
    echo "5. Set Dockerfile Path: ./serving/Dockerfile"
    echo "6. Set Docker Context: ."
    echo "7. Click: Create Web Service"
    echo ""
    echo "⏳ Render will build and deploy automatically!"
    echo "📊 Check dashboard for progress and live URL"
    echo ""
else
    echo "❌ Deployment cancelled"
    exit 1
fi
