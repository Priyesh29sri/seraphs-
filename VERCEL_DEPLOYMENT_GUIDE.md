# Seraphs 2.0 - Vercel Deployment Guide

## 📋 Overview

This guide will walk you through deploying the Seraphs 2.0 frontend to Vercel, a modern hosting platform optimized for React/Vite applications.

---

## 🎯 Prerequisites

Before deploying, ensure you have:
- ✅ GitHub account (to push code)
- ✅ Vercel account (free tier available at vercel.com)
- ✅ Git installed and configured
- ✅ All frontend code committed to GitHub

---

## 📝 Step-by-Step Deployment Process

### Step 1: Prepare the Frontend for Production

1. **Build the production bundle** (optional - Vercel will do this automatically):
   ```bash
   cd /Users/priyeshsrivastava/Seraphs/frontend
   npm run build
   ```

2. **Verify the build works locally**:
   ```bash
   npm run preview
   ```
   This will serve the production build at `http://localhost:4173`

---

### Step 2: Push Code to GitHub

1. **Initialize Git repository** (if not already done):
   ```bash
   cd /Users/priyeshsrivastava/Seraphs
   git init
   ```

2. **Add all files**:
   ```bash
   git add .
   ```

3. **Commit changes**:
   ```bash
   git commit -m "feat: Complete Seraphs 2.0 frontend with all 12 agents"
   ```

4. **Create GitHub repository**:
   - Go to https://github.com/new
   - Repository name: `seraphs` (or your preferred name)
   - Make it Public or Private
   - Don't initialize with README (we already have one)
   - Click "Create repository"

5. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/seraphs.git
   git branch -M main
   git push -u origin main
   ```

---

### Step 3: Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel**:
   - Visit https://vercel.com
   - Click "Sign Up" or "Log In"
   - Sign in with GitHub

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Select your GitHub repository: `seraphs`
   - Click "Import"

3. **Configure Project**:
   - **Framework Preset**: Vite (should auto-detect)
   - **Root Directory**: `frontend` (IMPORTANT!)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. **Environment Variables** (if needed):
   - Click "Environment Variables"
   - Add any required variables (e.g., API URLs)
   - Example:
     ```
     VITE_API_URL=https://your-backend-api.com
     ```

5. **Deploy**:
   - Click "Deploy"
   - Wait 1-2 minutes for deployment to complete
   - You'll get a URL like: `https://seraphs-xxx.vercel.app`

#### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from frontend directory**:
   ```bash
   cd /Users/priyeshsrivastava/Seraphs/frontend
   vercel
   ```

4. **Follow the prompts**:
   - Set up and deploy? `Y`
   - Which scope? (select your account)
   - Link to existing project? `N`
   - Project name? `seraphs`
   - In which directory is your code? `./`
   - Want to override settings? `N`

5. **Deploy to production**:
   ```bash
   vercel --prod
   ```

---

### Step 4: Configure Custom Domain (Optional)

1. **In Vercel Dashboard**:
   - Go to your project
   - Click "Settings" → "Domains"
   - Add your custom domain
   - Follow DNS configuration instructions

---

### Step 5: Configure Backend API URL

Since your backend runs on `http://localhost:8000`, you'll need to:

**Option 1: Deploy Backend Separately**
- Deploy your FastAPI backend to Railway, Render, or Fly.io
- Update the frontend API URL in `vercel.json` or environment variables

**Option 2: Use Vercel Serverless Functions**
- Convert your backend to Vercel serverless functions
- Place in `/api` directory

**Option 3: Keep Backend Local (Development Only)**
- Frontend will work but won't fetch live data
- Good for showcasing UI/UX

---

## 🔧 Vercel Configuration File

Create `vercel.json` in the frontend directory:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

This ensures proper routing for React Router.

---

## 🚀 Post-Deployment Checklist

After deployment, verify:
- ✅ Landing page loads correctly
- ✅ Dashboard displays all sections
- ✅ All 12 agent pages are accessible
- ✅ Navigation works (React Router)
- ✅ Real-Time Monitoring section displays
- ✅ Whobee robot renders
- ✅ Mobile responsiveness

---

## 🐛 Troubleshooting

### Issue: 404 on page refresh
**Solution**: Add `vercel.json` with rewrites (see above)

### Issue: Build fails
**Solution**: 
- Check `package.json` has all dependencies
- Ensure `vite.config.ts` is correct
- Check build logs in Vercel dashboard

### Issue: Environment variables not working
**Solution**: 
- Prefix with `VITE_` (e.g., `VITE_API_URL`)
- Redeploy after adding variables

### Issue: API calls failing
**Solution**: 
- Update API URL from `localhost:8000` to production backend
- Enable CORS on backend
- Check network tab in browser DevTools

---

## 📊 Deployment Summary

| Item | Value |
|------|-------|
| **Platform** | Vercel |
| **Framework** | Vite + React + TypeScript |
| **Build Time** | ~1-2 minutes |
| **Cost** | Free (Hobby tier) |
| **Custom Domain** | Supported |
| **SSL** | Automatic (HTTPS) |
| **CDN** | Global edge network |

---

## 🎯 Quick Deploy Commands

```bash
# 1. Build locally (optional)
cd /Users/priyeshsrivastava/Seraphs/frontend
npm run build

# 2. Push to GitHub
cd /Users/priyeshsrivastava/Seraphs
git add .
git commit -m "feat: Production-ready Seraphs 2.0"
git push origin main

# 3. Deploy to Vercel (if using CLI)
cd frontend
vercel --prod
```

---

## ✅ Expected Result

After successful deployment:
- **Production URL**: `https://seraphs-xxx.vercel.app`
- **Dashboard**: `https://seraphs-xxx.vercel.app/dashboard`
- **Agents**: `https://seraphs-xxx.vercel.app/agents`
- **Individual Agents**: `https://seraphs-xxx.vercel.app/agent/1` through `/agent/12`

---

## 🔗 Useful Links

- Vercel Dashboard: https://vercel.com/dashboard
- Vercel Documentation: https://vercel.com/docs
- Vite Deployment Guide: https://vitejs.dev/guide/static-deploy.html
- GitHub: https://github.com

---

**Ready to deploy!** 🚀
