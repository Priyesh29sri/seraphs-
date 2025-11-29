#!/bin/bash

echo "🚀 Seraphs 2.0 - Complete Production Deployment"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "${BLUE}Step 1: Checking prerequisites...${NC}"
command -v git >/dev/null 2>&1 || { echo "❌ Git is required but not installed."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed."; exit 1; }
echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

# Step 2: Commit all changes
echo -e "${BLUE}Step 2: Committing changes to Git...${NC}"
git add .
git commit -m "feat: Production deployment - Complete Seraphs 2.0 with Cardano integration" || echo "No changes to commit"
echo -e "${GREEN}✅ Changes committed${NC}"
echo ""

# Step 3: Push to GitHub
echo -e "${BLUE}Step 3: Pushing to GitHub...${NC}"
echo -e "${YELLOW}⚠️  You need to set up GitHub remote first:${NC}"
echo "   1. Create a new repository at https://github.com/new"
echo "   2. Run: git remote add origin https://github.com/YOUR_USERNAME/seraphs.git"
echo "   3. Run: git push -u origin main"
echo ""
read -p "Press Enter when you've pushed to GitHub..."
echo -e "${GREEN}✅ Code pushed to GitHub${NC}"
echo ""

# Step 4: Deploy Backend to Railway
echo -e "${BLUE}Step 4: Deploying Backend to Railway...${NC}"
echo -e "${YELLOW}⚠️  Manual steps required:${NC}"
echo "   1. Go to https://railway.app"
echo "   2. Sign in with GitHub"
echo "   3. Click 'New Project' → 'Deploy from GitHub repo'"
echo "   4. Select your 'seraphs' repository"
echo "   5. Add these environment variables:"
echo ""
echo "      DATABASE_URL=<Railway will provide PostgreSQL>"
echo "      NEO4J_URI=<from Neo4j Aura>"
echo "      NEO4J_USER=neo4j"
echo "      NEO4J_PASSWORD=<your password>"
echo "      REDIS_URL=<from Upstash>"
echo "      BLOCKFROST_API_KEY=<from Blockfrost.io>"
echo "      BLOCKFROST_NETWORK=mainnet"
echo "      GEMINI_API_KEY=<your key>"
echo "      ANTHROPIC_API_KEY=<your key>"
echo "      OPENAI_API_KEY=<your key>"
echo ""
read -p "Press Enter when backend is deployed..."
echo -e "${GREEN}✅ Backend deployed${NC}"
echo ""

# Step 5: Deploy Frontend to Vercel
echo -e "${BLUE}Step 5: Deploying Frontend to Vercel...${NC}"
cd frontend
echo -e "${YELLOW}⚠️  Manual steps required:${NC}"
echo "   1. Go to https://vercel.com"
echo "   2. Sign in with GitHub"
echo "   3. Click 'Add New' → 'Project'"
echo "   4. Import your 'seraphs' repository"
echo "   5. Set Root Directory to: frontend"
echo "   6. Add environment variable:"
echo "      VITE_API_URL=<your Railway backend URL>"
echo "   7. Click 'Deploy'"
echo ""
read -p "Press Enter when frontend is deployed..."
cd ..
echo -e "${GREEN}✅ Frontend deployed${NC}"
echo ""

# Step 6: Test deployment
echo -e "${BLUE}Step 6: Testing deployment...${NC}"
echo "Please test these URLs:"
echo "   Frontend: https://seraphs.vercel.app"
echo "   Backend API: https://your-app.railway.app/api/health"
echo "   Dashboard: https://seraphs.vercel.app/dashboard"
echo ""
read -p "Press Enter when testing is complete..."
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""

echo "🎉 Seraphs 2.0 is now live!"
echo "================================================"
echo "Frontend: https://seraphs.vercel.app"
echo "Backend: https://your-app.railway.app"
echo "Cardano: Mainnet (via Blockfrost)"
echo ""
echo "Next steps:"
echo "1. Configure custom domain (optional)"
echo "2. Set up monitoring dashboards"
echo "3. Enable Cardano transaction monitoring"
echo "4. Test all 12 agents end-to-end"
