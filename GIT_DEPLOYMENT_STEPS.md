# 🚀 Git & Streamlit Deployment - Quick Start

## Step 1: Initialize Git Repository

Run these commands in your terminal:

```bash
cd /Users/sadaf/Desktop/da/first

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Currency Crisis Analysis Dashboard"
```

## Step 2: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `Currency-Crisis-Dashboard` (or keep `Currency-Convertor`)
3. Description: `Interactive financial analytics dashboard analyzing USD/IRR exchange rates and crisis detection`
4. Set to **Public**
5. **DO NOT** initialize with README (we already have files)
6. Click "Create repository"

## Step 3: Connect to GitHub

After creating the repo, GitHub will show you commands. Run:

```bash
# Add GitHub as remote
git remote add origin https://github.com/sadaf-rad/Currency-Crisis-Dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io/
2. Click "Sign in" (use your GitHub account)
3. Click "New app"
4. Select:
   - **Repository**: `sadaf-rad/Currency-Crisis-Dashboard`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click "Deploy!"

Wait 2-3 minutes, and you'll get a live URL like:
`https://sadaf-rad-currency-crisis-dashboard.streamlit.app`

## Step 5: Verify Deployment

✅ Your dashboard should now be live and accessible to anyone!

---

## 🔄 Future Updates

Whenever you make changes:

```bash
git add .
git commit -m "Update: describe your changes"
git push origin main
```

Streamlit Cloud will automatically redeploy! 🎉

---

## 🐛 Troubleshooting

**Git errors?**
- Make sure you're in the right directory: `/Users/sadaf/Desktop/da/first`
- If "remote origin already exists": `git remote remove origin` then add again

**Streamlit deployment fails?**
- Check `requirements.txt` is in the repo
- Ensure `app.py` is in root directory
- Check Streamlit Cloud logs for errors

**Need to change repo name?**
```bash
git remote set-url origin https://github.com/sadaf-rad/NEW-REPO-NAME.git
```

---

Ready? Let's do it! 🚀
