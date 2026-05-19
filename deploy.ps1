# =========================================
# Deploy to Render.com Helper Script (Windows)
# =========================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🚀 Render.com Deployment Helper (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check git
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git not installed. Please install git first." -ForegroundColor Red
    exit 1
}

# Check if in git repo
$gitCheck = git rev-parse --git-dir 2>$null
if (!$gitCheck) {
    Write-Host "❌ Not in a git repository. Initialize with: git init" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Git repository detected" -ForegroundColor Green
Write-Host ""

# Step 1: Check model exists
if (!(Test-Path "serving_model/rfahrur6045-pipeline")) {
    Write-Host "❌ Error: serving_model/rfahrur6045-pipeline/ directory not found" -ForegroundColor Red
    Write-Host "   Make sure model is generated and in correct directory" -ForegroundColor Red
    exit 1
}

$modelVersions = @(Get-ChildItem -Path "serving_model/rfahrur6045-pipeline" -Directory)
if ($modelVersions.Count -eq 0) {
    Write-Host "❌ Error: No model versions found in serving_model/rfahrur6045-pipeline/" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found $($modelVersions.Count) model version(s)" -ForegroundColor Green
$latestVersion = $modelVersions[-1].Name
Write-Host "   Latest version: $latestVersion" -ForegroundColor Green
Write-Host ""

# Step 2: Check Dockerfile
if (!(Test-Path "serving/Dockerfile")) {
    Write-Host "❌ Error: serving/Dockerfile not found" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dockerfile found at serving/Dockerfile" -ForegroundColor Green
Write-Host ""

# Step 3: Check render.yaml
if (!(Test-Path "render.yaml")) {
    Write-Host "❌ Error: render.yaml not found" -ForegroundColor Red
    exit 1
}
Write-Host "✅ render.yaml found" -ForegroundColor Green
Write-Host ""

# Step 4: Git operations
Write-Host "📦 Preparing for deployment..." -ForegroundColor Yellow
git add .
git status --short | Select-Object -First 10

Write-Host ""
$confirm = Read-Host "✅ Commit and push? (y/n)"

if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    $commitMsg = Read-Host "📝 Commit message (default: 'Deploy model update')"
    if ([string]::IsNullOrWhiteSpace($commitMsg)) {
        $commitMsg = "Deploy model update"
    }
    
    git commit -m $commitMsg -ErrorAction SilentlyContinue
    git push origin main
    
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎯 Next steps:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://dashboard.render.com/" -ForegroundColor White
    Write-Host "2. Click: New + → Web Service" -ForegroundColor White
    Write-Host "3. Select: Public Git repository" -ForegroundColor White
    Write-Host "4. Enter: https://github.com/YOUR_USERNAME/YOUR_REPO" -ForegroundColor White
    Write-Host "5. Set Dockerfile Path: ./serving/Dockerfile" -ForegroundColor White
    Write-Host "6. Set Docker Context: ." -ForegroundColor White
    Write-Host "7. Click: Create Web Service" -ForegroundColor White
    Write-Host ""
    Write-Host "⏳ Render will build and deploy automatically!" -ForegroundColor Yellow
    Write-Host "📊 Check dashboard for progress and live URL" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit 1
}
