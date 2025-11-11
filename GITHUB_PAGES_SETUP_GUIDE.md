# 📄 GitHub Pages Resume Landing Page Setup Guide

## Overview
This guide shows you how to use GitHub Pages to render your README.md as a professional landing page for your resume.

---

## 🎯 What is GitHub Pages?

GitHub Pages is a free hosting service that turns your GitHub repository into a live website. For a repository named `username.github.io`, GitHub automatically publishes it at `https://username.github.io`.

---

## ✅ Step-by-Step Instructions

### **Step 1: Verify Repository Name**

Your repository **must** be named: `avaluev.github.io`

✓ **Your repo is correctly named!**

---

### **Step 2: Enable GitHub Pages**

1. Go to your repository: https://github.com/avaluev/avaluev.github.io
2. Click **Settings** (top navigation bar)
3. Scroll down to **Pages** section (left sidebar)
4. Under **Source**, select:
   - **Branch:** `master` (or `main`)
   - **Folder:** `/ (root)`
5. Click **Save**

GitHub will automatically deploy your site within 1-2 minutes.

---

### **Step 3: Choose Your Landing Page Strategy**

You have **two options**:

#### **Option A: Use README.md as Landing Page** (Simple, Markdown-based)

**Pros:**
- ✅ Simple - no HTML/CSS needed
- ✅ Easy to update - edit README.md directly
- ✅ GitHub auto-converts Markdown to HTML

**Cons:**
- ⚠️ Basic styling (GitHub default theme)
- ⚠️ Limited customization

**How to implement:**
1. Rename or delete `index.html` (if you want README to be default)
2. Make sure your `README.md` is well-formatted
3. Optionally add Jekyll theme (see Step 4)
4. Push changes to GitHub
5. Your resume will be live at: https://avaluev.github.io

**Current status:** ✅ Your README.md already contains excellent resume content!

---

#### **Option B: Use Custom HTML Landing Page** (Professional, Fully Customizable)

**Pros:**
- ✅ Professional design with custom CSS
- ✅ Full control over layout
- ✅ Can include animations, interactive elements
- ✅ Better SEO and meta tags

**Cons:**
- ⚠️ Requires HTML/CSS knowledge
- ⚠️ More maintenance

**How to implement:**
1. Keep your existing `index.html` file
2. Update `index.html` with resume content from README.md
3. Customize CSS in `/css/scrolling-nav.css`
4. Push changes to GitHub
5. Your resume will be live at: https://avaluev.github.io

**Current status:** ✅ You already have `index.html` with Bootstrap styling!

---

### **Step 4: Add Jekyll Theme** (Optional - For README.md approach)

Jekyll is a static site generator that makes your README.md look professional.

1. Create or edit `_config.yml` in your repository root:

```yaml
title: Alex Valuev - Senior AI Product Manager
description: Healthcare AI • FinTech • MedTech | 11+ years building AI systems
author: Aleksandr Valuev
email: valuev.alexandr@gmail.com
url: https://avaluev.github.io

# Theme
theme: jekyll-theme-minimal
# OR other themes:
# theme: jekyll-theme-cayman
# theme: jekyll-theme-architect
# theme: jekyll-theme-slate

# Social links
linkedin_username: valuev
github_username: avaluev

# Google Analytics (optional)
google_analytics: UA-XXXXXXXXX-X

# Plugins
plugins:
  - jekyll-seo-tag
  - jekyll-feed
```

2. **Available GitHub-supported themes:**
   - `jekyll-theme-minimal` - Clean, simple
   - `jekyll-theme-cayman` - Modern header banner
   - `jekyll-theme-slate` - Dark theme
   - `jekyll-theme-architect` - Professional with header
   - `jekyll-theme-dinky` - Compact sidebar
   - `jekyll-theme-merlot` - Simple typography
   - `jekyll-theme-midnight` - Dark with sidebar
   - `jekyll-theme-modernist` - Tech-focused
   - `jekyll-theme-tactile` - Clean with navigation
   - `jekyll-theme-time-machine` - Retro sci-fi

3. Preview themes: https://pages.github.com/themes/

---

### **Step 5: Verify Your Site is Live**

1. Wait 1-2 minutes after pushing changes
2. Visit: https://avaluev.github.io
3. Check for errors in Settings → Pages

**Troubleshooting:**
- If you see 404: Check that GitHub Pages is enabled in Settings
- If old version shows: Clear browser cache (Ctrl+Shift+R)
- If build fails: Check Settings → Pages for error messages

---

## 🎨 Recommended Approach for Your Resume

Based on your current setup, I recommend:

### **Hybrid Approach: README.md + Custom Domain Landing**

1. **Keep `README.md`** for GitHub visitors (developers, recruiters browsing your repo)
2. **Keep `index.html`** as your primary landing page (professional design)
3. **Update `index.html`** to pull content from README.md structure

**Why this works:**
- ✅ Professional landing page at https://avaluev.github.io
- ✅ Clean resume in README.md for GitHub profile
- ✅ SEO-optimized HTML page
- ✅ Easy to maintain (update README, sync to HTML as needed)

---

## 🔧 Quick Customization Tips

### **For README.md Approach:**

1. **Add a profile photo:**
```markdown
<div align="center">
  <img src="profile.jpg" alt="Alex Valuev" width="200" style="border-radius: 50%;">
</div>
```

2. **Add custom CSS (Jekyll):**
Create `assets/css/style.scss`:
```scss
---
---

@import "{{ site.theme }}";

header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.markdown-body {
  font-family: 'Inter', sans-serif;
  max-width: 800px;
  margin: 0 auto;
}
```

3. **Add meta tags for SEO:**
Create `_includes/head-custom.html`:
```html
<meta property="og:title" content="Alex Valuev - Senior AI Product Manager">
<meta property="og:description" content="11+ years building AI systems in Healthcare, FinTech, MedTech">
<meta property="og:image" content="https://avaluev.github.io/profile.jpg">
<meta property="og:url" content="https://avaluev.github.io">
<meta name="twitter:card" content="summary_large_image">
```

---

### **For HTML Approach:**

Your existing `index.html` already has Bootstrap and custom CSS. To sync it with your README:

1. **Update the HTML content sections with resume data**
2. **Ensure mobile responsiveness** (already handled by Bootstrap)
3. **Add structured data for SEO:**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Aleksandr Valuev",
  "jobTitle": "Senior AI Product Manager",
  "email": "valuev.alexandr@gmail.com",
  "url": "https://avaluev.github.io",
  "sameAs": [
    "https://linkedin.com/in/valuev",
    "https://github.com/avaluev"
  ]
}
</script>
```

---

## 🚀 Custom Domain (Optional)

If you want to use a custom domain (e.g., `alexvaluev.com`):

1. **Buy a domain** (Namecheap, Google Domains, Cloudflare)

2. **Add DNS records:**
   - Type: `A`, Host: `@`, Value: `185.199.108.153`
   - Type: `A`, Host: `@`, Value: `185.199.109.153`
   - Type: `A`, Host: `@`, Value: `185.199.110.153`
   - Type: `A`, Host: `@`, Value: `185.199.111.153`
   - Type: `CNAME`, Host: `www`, Value: `avaluev.github.io`

3. **Configure GitHub:**
   - Settings → Pages → Custom domain
   - Enter: `alexvaluev.com`
   - Check "Enforce HTTPS"

4. **Create `CNAME` file in repo root:**
```
alexvaluev.com
```

---

## 📊 Analytics & Monitoring

### **Add Google Analytics:**

1. Get tracking ID from https://analytics.google.com
2. **For Jekyll (_config.yml):**
```yaml
google_analytics: G-XXXXXXXXXX
```

3. **For HTML (in `<head>`):**
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## ✅ Final Checklist

- [ ] GitHub Pages enabled in Settings
- [ ] Branch selected (master/main)
- [ ] README.md or index.html updated with resume
- [ ] _config.yml configured (if using Jekyll)
- [ ] Site accessible at https://avaluev.github.io
- [ ] Mobile responsive (test on phone)
- [ ] Links working (LinkedIn, email, etc.)
- [ ] Meta tags for SEO added
- [ ] Analytics configured (optional)
- [ ] Custom domain configured (optional)

---

## 🎯 Next Steps

1. **Choose your approach** (README.md vs HTML vs Hybrid)
2. **Enable GitHub Pages** in Settings
3. **Test your site** at https://avaluev.github.io
4. **Share your link** on LinkedIn, resume, email signature
5. **Monitor traffic** with Google Analytics

---

## 🆘 Common Issues

### Issue: "404 - There isn't a GitHub Pages site here"
**Solution:**
- Check Settings → Pages is enabled
- Verify branch name (master vs main)
- Wait 2-3 minutes for deployment

### Issue: "Changes not showing"
**Solution:**
- Clear browser cache (Ctrl+Shift+R)
- Check commit was pushed to correct branch
- Verify GitHub Actions build succeeded (Actions tab)

### Issue: "Styling not loading"
**Solution:**
- Check file paths are relative (not absolute)
- Verify CSS files exist in repo
- Check browser console for errors (F12)

---

## 📚 Resources

- **GitHub Pages Docs:** https://docs.github.com/en/pages
- **Jekyll Themes:** https://pages.github.com/themes/
- **Jekyll Docs:** https://jekyllrb.com/docs/
- **Markdown Guide:** https://www.markdownguide.org/

---

**🎉 Your resume will be live at: https://avaluev.github.io**

Good luck with your job search! Your comprehensive resume is excellent and should help you land your next role.
