# 🧹 Repository Cleanup Guide

## Overview
This guide provides step-by-step instructions for cleaning up your `avaluev.github.io` repository, keeping only:
- `README.md` (your resume)
- `autonomous-ai-team/` folder (your AI project)

---

## ⚠️ IMPORTANT: Backup First!

Before making any destructive changes, **create a backup**:

```bash
# Clone your repo to a backup location
git clone https://github.com/avaluev/avaluev.github.io.git avaluev.github.io-backup
```

---

## 📋 Current Repository Structure

Your repository currently contains:

```
avaluev.github.io/
├── README.md                    ✅ KEEP
├── autonomous-ai-team/          ✅ KEEP
├── index.html                   ❌ REMOVE
├── LICENSE                      ⚠️  DECIDE (recommended: keep)
├── CNAME                        ⚠️  DECIDE (keep if using custom domain)
├── _config.yml                  ⚠️  DECIDE (keep for Jekyll theme)
├── package.json                 ❌ REMOVE
├── package-lock.json            ❌ REMOVE
├── gulpfile.js                  ❌ REMOVE
├── browserconfig.xml            ❌ REMOVE
├── site.webmanifest             ❌ REMOVE
├── favicon files (*.png, *.ico) ❌ REMOVE
├── apple-touch-icon.png         ❌ REMOVE
├── safari-pinned-tab.svg        ❌ REMOVE
├── css/                         ❌ REMOVE
├── js/                          ❌ REMOVE
└── vendor/                      ❌ REMOVE
```

---

## 🎯 Cleanup Strategy

### **Option A: Manual Cleanup via GitHub Web Interface** (Safest for beginners)

#### **Step 1: Navigate to Repository**
1. Go to: https://github.com/avaluev/avaluev.github.io
2. Make sure you're on the `master` (or `main`) branch

#### **Step 2: Delete Files One by One**

For each file to remove:
1. Click on the file (e.g., `index.html`)
2. Click the **trash icon** (🗑️) in the top right
3. Scroll down and enter commit message: `chore: Remove unnecessary file`
4. Click **Commit changes**

**Files to delete:**
- `index.html`
- `package.json`
- `package-lock.json`
- `gulpfile.js`
- `browserconfig.xml`
- `site.webmanifest`
- All favicon files: `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`
- `android-chrome-192x192.png`
- `android-chrome-512x512.png`
- `apple-touch-icon.png`
- `mstile-150x150.png`
- `safari-pinned-tab.svg`

#### **Step 3: Delete Folders**

For each folder:
1. Navigate into the folder (e.g., `css/`)
2. Delete all files inside
3. GitHub will auto-delete empty folders

**Folders to delete:**
- `css/`
- `js/`
- `vendor/`

#### **Step 4: Review Remaining Files**

After cleanup, your repository should only have:
```
avaluev.github.io/
├── README.md
├── autonomous-ai-team/
├── LICENSE (optional)
├── CNAME (if using custom domain)
└── _config.yml (if using Jekyll)
```

---

### **Option B: Cleanup via Git Command Line** (Faster, recommended)

#### **Step 1: Clone Repository**

```bash
# Clone your repository
git clone https://github.com/avaluev/avaluev.github.io.git
cd avaluev.github.io

# Verify you're on the correct branch
git branch
```

#### **Step 2: Remove Files**

```bash
# Remove individual files
git rm index.html
git rm package.json
git rm package-lock.json
git rm gulpfile.js
git rm browserconfig.xml
git rm site.webmanifest
git rm favicon.ico
git rm favicon-16x16.png
git rm favicon-32x32.png
git rm android-chrome-192x192.png
git rm android-chrome-512x512.png
git rm apple-touch-icon.png
git rm mstile-150x150.png
git rm safari-pinned-tab.svg

# Remove folders
git rm -r css/
git rm -r js/
git rm -r vendor/

# Review what will be deleted
git status
```

#### **Step 3: Commit and Push**

```bash
# Commit the changes
git commit -m "chore: Clean up repository - keep only README.md and autonomous-ai-team"

# Push to GitHub
git push origin master
# OR if your default branch is 'main':
# git push origin main
```

#### **Step 4: Verify on GitHub**

Visit https://github.com/avaluev/avaluev.github.io and confirm files are deleted.

---

### **Option C: Advanced - Interactive Cleanup with Script** (Most control)

Create a cleanup script for selective deletion:

```bash
#!/bin/bash
# cleanup.sh

echo "🧹 Repository Cleanup Script"
echo "=============================="
echo ""
echo "This will DELETE the following:"
echo "  - index.html"
echo "  - package.json, package-lock.json"
echo "  - gulpfile.js"
echo "  - All favicon files"
echo "  - css/, js/, vendor/ folders"
echo ""
echo "This will KEEP:"
echo "  ✅ README.md"
echo "  ✅ autonomous-ai-team/"
echo "  ✅ LICENSE"
echo "  ✅ CNAME (if exists)"
echo "  ✅ _config.yml (if exists)"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing files..."

    # Remove files
    git rm index.html
    git rm package.json package-lock.json
    git rm gulpfile.js
    git rm browserconfig.xml site.webmanifest
    git rm favicon*.png favicon*.ico
    git rm android-chrome-*.png
    git rm apple-touch-icon.png
    git rm mstile-*.png
    git rm safari-pinned-tab.svg

    # Remove directories
    git rm -r css/ js/ vendor/

    echo "✅ Files staged for deletion"
    echo ""
    echo "📊 Status:"
    git status
    echo ""
    echo "To commit and push:"
    echo "  git commit -m 'chore: Clean up repository'"
    echo "  git push origin master"
else
    echo "❌ Cleanup cancelled"
fi
```

**Usage:**
```bash
chmod +x cleanup.sh
./cleanup.sh
```

---

## 🤔 What About These Files?

### **LICENSE**
**Recommendation: KEEP**
- Defines how others can use your code
- Professional appearance
- Required for open source projects

### **CNAME**
**Recommendation: KEEP if using custom domain, otherwise DELETE**
- Only needed if you have a custom domain (e.g., `alexvaluev.com`)
- Check contents: `cat CNAME`
- Delete if not using custom domain

### **_config.yml**
**Recommendation: KEEP if using Jekyll theme, otherwise DELETE**
- Configures Jekyll theme for GitHub Pages
- If you want README.md to have professional styling, keep it
- If you're not using Jekyll, delete it

---

## 📁 What About .git Folder?

**⚠️ NEVER DELETE `.git/` folder!**

This folder contains your entire Git history. Deleting it will:
- ❌ Break your repository
- ❌ Lose all commit history
- ❌ Disconnect from GitHub

---

## 🎯 Recommended Final Structure

After cleanup, your repository should look like this:

```
avaluev.github.io/
├── .git/                          # Git folder (NEVER delete)
├── .gitignore                     # Git ignore rules (optional)
├── README.md                      # Your resume ✅
├── LICENSE                        # Open source license ✅
├── CNAME                          # Custom domain (if using) ⚠️
├── _config.yml                    # Jekyll config (if using) ⚠️
└── autonomous-ai-team/            # Your AI project ✅
    ├── README.md
    ├── ARCHITECTURE.md
    ├── QUICKSTART.md
    ├── requirements.txt
    ├── main.py
    ├── .env.example
    ├── src/
    ├── docker/
    ├── scripts/
    └── config/
```

---

## 🚀 Post-Cleanup Steps

### **1. Update GitHub Pages Settings**

If you deleted `index.html` and want README.md as landing page:

1. Go to: Settings → Pages
2. Verify source is set to: **master** (or **main**) branch, **/ (root)**
3. Optionally set a Jekyll theme in `_config.yml`

### **2. Update Repository Description**

1. Go to repository homepage
2. Click **⚙️ Settings** next to "About"
3. Update description:
   ```
   Senior AI Product Manager Resume & Autonomous AI Multi-Agent System
   ```
4. Add topics (tags):
   - `resume`
   - `ai-agents`
   - `claude`
   - `fastapi`
   - `portfolio`

### **3. Create Repository README** (Optional)

If you want a different README for the repository root (separate from your resume), create a landing README:

```markdown
# 👋 Welcome to Alex Valuev's Portfolio

## 📄 Resume
View my full resume and professional experience: [README.md](README.md)

## 🤖 Projects

### Autonomous AI Dream Team
A sophisticated multi-agent AI system powered by Claude Sonnet 4.5.

📂 [View Project](autonomous-ai-team/)

## 🔗 Links
- 💼 [LinkedIn](https://linkedin.com/in/valuev)
- 📧 [Email](mailto:valuev.alexandr@gmail.com)
- 🎓 [Career Coaching](https://t.me/itcareertech)
```

---

## ✅ Cleanup Checklist

- [ ] Backed up repository (cloned to local)
- [ ] Removed unnecessary HTML/CSS/JS files
- [ ] Removed npm/node files (package.json, etc.)
- [ ] Removed favicon files
- [ ] Removed vendor libraries (Bootstrap, jQuery)
- [ ] Kept README.md
- [ ] Kept autonomous-ai-team folder
- [ ] Kept LICENSE (optional)
- [ ] Kept CNAME (if using custom domain)
- [ ] Kept _config.yml (if using Jekyll)
- [ ] Verified on GitHub that files are deleted
- [ ] Tested GitHub Pages still works
- [ ] Updated repository description

---

## 🔄 Reverting Changes (If Needed)

If you made a mistake, you can revert:

### **Revert last commit:**
```bash
git revert HEAD
git push origin master
```

### **Restore specific file:**
```bash
# Find the commit before deletion
git log --oneline

# Restore file from that commit
git checkout <commit-hash> -- index.html
git commit -m "Restore index.html"
git push origin master
```

### **Restore entire repository:**
```bash
# Use your backup
cd avaluev.github.io-backup
git push --force origin master
```

---

## 🆘 Troubleshooting

### Issue: "GitHub Pages broken after cleanup"
**Solution:**
- Ensure `README.md` still exists
- Check Settings → Pages is enabled
- Wait 2-3 minutes for rebuild
- If using Jekyll, verify `_config.yml` is valid

### Issue: "Can't delete file - 'Protected branch'"
**Solution:**
- Settings → Branches → Branch protection rules
- Temporarily disable protection
- Delete files
- Re-enable protection

### Issue: "Deleted wrong file"
**Solution:**
- See "Reverting Changes" section above
- Or restore from backup

---

## 📞 Need Help?

If you encounter issues:
1. Check GitHub repository Actions tab for build errors
2. Review commit history for what was deleted
3. Use backup to restore if needed

---

**🎉 After cleanup, your repository will be clean, professional, and focused on what matters: your resume and AI project!**
