# Mohammad Rohaan — Portfolio

[![Live site](https://img.shields.io/badge/live-rohaan2802.github.io-6d5efc?style=flat-square)](https://rohaan2802.github.io/)
[![GitHub Pages](https://img.shields.io/badge/deploy-GitHub%20Pages-24292f?style=flat-square&logo=github)](https://pages.github.com/)
[![Node.js](https://img.shields.io/badge/node-%E2%89%A518-339933?style=flat-square&logo=nodedotjs&logoColor=white)](https://nodejs.org/)

Modern, fast, responsive personal portfolio and brand site for **Mohammad Rohaan** — BSCS student at FAST NUCES (Islamabad). Built as a static site for GitHub Pages with no build step, no framework, and a token-based CSS design system.

## 🚀 Live Demo
[https://rohaan2802.github.io/](https://rohaan2802.github.io/)

---

## Table of contents

- [Overview](#overview)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Site sections](#site-sections)
- [Featured projects](#featured-projects)
- [Getting started](#getting-started)
- [Local development](#local-development)
- [VS Code debugging](#vs-code-debugging)
- [Deployment](#deployment)
- [Updating content](#updating-content)
- [SEO & discoverability](#seo--discoverability)
- [Design system](#design-system)
- [Browser behavior](#browser-behavior)
- [Assets](#assets)
- [Contact & links](#contact--links)
- [License](#license)

---

## Overview

This repository hosts a single-page portfolio that presents software engineering, AI/ML, data science, a live AI voice agent, and systems work. The site prioritizes:

- **Clarity** — scannable sections (About, Work, Stack, Contact) with expandable project details
- **Speed** — vanilla HTML/CSS/JS, no bundler; cache-busted CSS via query string
- **Credibility** — structured data (JSON-LD), Open Graph/Twitter cards, resume PDF, and curated GitHub project links
- **Accessibility** — skip link, ARIA labels, keyboard nav (Escape closes menu), reduced-motion support

---

## Features

| Area | Details |
|------|---------|
| **Layout** | Responsive grid layouts from ~360px to desktop; sticky header; mobile hamburger nav |
| **Theming** | Dark-first design with automatic light mode via `prefers-color-scheme: light` |
| **Interactivity** | Collapsible mobile nav, smooth scroll, back-to-top button, `<details>` project expanders |
| **Email UX** | Desktop: `mailto:` links open Gmail compose; touch devices: native mail app |
| **SEO** | Meta description/keywords, canonical URL, JSON-LD (`WebSite` + `Person`), `sitemap.xml`, `robots.txt` |
| **PWA hints** | `manifest.json` with theme/background colors and app icons |
| **Dev tooling** | Node static server with smart port selection; VS Code F5 debug configs for Chrome/Edge |
| **GitHub Pages** | `.nojekyll` present so Jekyll does not interfere with static assets |

---

## Tech stack

| Layer | Technologies |
|-------|--------------|
| **Markup** | HTML5, semantic sections, inline JSON-LD |
| **Styles** | CSS custom properties (design tokens), CSS Grid/Flexbox, media queries |
| **Scripts** | Vanilla JavaScript (IIFE in `index.html`) — nav, scroll, footer year, Gmail compose |
| **Fonts & icons** | [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts), [Font Awesome 6.4](https://fontawesome.com/) (CDN) |
| **Local server** | Node.js 18+ (`scripts/dev-server.mjs`) — zero npm dependencies |
| **Hosting** | GitHub Pages (`rohaan2802.github.io` user site) |

No React, Vue, Tailwind, or build pipeline — edit files and deploy.

---

## Project structure

```
rohaan2802.github.io/
├── index.html              # Single-page site (content + inline JS)
├── style.css               # Design system + all component styles
├── manifest.json           # Web app manifest (PWA metadata)
├── package.json            # npm scripts for dev server only
├── robots.txt              # Crawler rules + sitemap reference
├── sitemap.xml             # Search engine URL index
├── google9aef6604bac35f6b.html  # Google Search Console verification
├── .nojekyll               # Disable Jekyll on GitHub Pages
├── images/
│   ├── icon.png            # Favicon
│   ├── portfolio_img.png   # Hero portrait + OG/Twitter image
│   ├── resume_img.png      # Resume-related imagery
│   └── linkedin_background.png
├── resume/
│   └── Mohammad_Rohaan_Resume.pdf
├── scripts/
│   ├── dev-server.mjs      # Static file server (dynamic port)
│   └── build-resume.py     # One-page resume PDF generator
└── .vscode/
    ├── launch.json         # Chrome/Edge debug + dev server task
    └── tasks.json          # Background npm dev task with SERVER_READY matcher
```

---

## Site sections

| Section | ID | Content |
|---------|-----|---------|
| **Hero** | — | Headline, availability, profile card, social links, CTA buttons |
| **About** | `#about` | What I do, hardware/robotics, career goals |
| **Featured projects** | `#projects` | Eight GitHub projects with tags, expandable “What I built”, and a live demo on the voice agent |
| **Skills** | `#skills` | Four stack cards: languages, AI/ML, software engineering, systems/embedded |
| **Contact** | `#contact` | Email, university email, phone, LinkedIn, GitHub, WhatsApp |

Primary navigation and footer live in `index.html`. All copy, project cards, and skill tags are edited there.

---

## Featured projects

Curated from [github.com/rohaan2802](https://github.com/rohaan2802):

| Project | Focus | Links |
|---------|-------|-------|
| AI Voice Cold-Calling Agent | Next.js, VAPI, Groq, Deepgram | [Live](https://web-rouge-xi-23.vercel.app) · [Code](https://github.com/rohaan2802/Cold-Calling-Agent) |
| Intelligent Reading Comprehension & Quiz Generator | NLP, scikit-learn, Streamlit | [AI_Quiz_Generator](https://github.com/rohaan2802/AI_Quiz_Generator) |
| Library Management System (LibraryMS) | Java 17, Spring Boot, MySQL | [LibraryMS](https://github.com/rohaan2802/LibraryMS) |
| Shuttlecock Detection for Robotic Collection | YOLOv8, computer vision, robotics | [ShuttleCock-Detection](https://github.com/rohaan2802/ShuttleCock-Detection) |
| Ivor Paine Memorial Hospital | SQL Server, PHP, ER/EER modeling | [HospitalMS](https://github.com/rohaan2802/HospitalMS) |
| K-means with Triangle Inequality | C++, OpenMP, parallel computing | [KMeanTriangleInequality](https://github.com/rohaan2802/KMeanTriangleInequality) |
| Git Lite | C++, DSA, version control internals | [GitLite_DSA_Project](https://github.com/rohaan2802/GitLite_DSA_Project) |
| Multi-Robot Path Planning | Python, time-expanded BFS, robotics | [Robot_Path_Plan](https://github.com/rohaan2802/Robot_Path_Plan) |

To add or reorder projects, edit the `.projects-grid` block in `index.html`.

---

## Getting started

### Requirements

- **[Node.js](https://nodejs.org/) 18+** — only needed for local preview (not for production hosting)
- Any modern browser (Chrome, Edge, Firefox, Safari)
- Optional: [VS Code](https://code.visualstudio.com/) or Cursor for F5 debugging

### Clone

```bash
git clone https://github.com/rohaan2802/rohaan2802.github.io.git
cd rohaan2802.github.io
```

---

## Local development

The dev server serves static files from the repo root with correct MIME types and path traversal protection.

```bash
npm run dev
# or
npm start
```

**What happens:**

1. Tries preferred ports in order: `8080`, `5500`, `3000`, `5173`, `8888`, `9000`
2. If a preferred port is busy, attempts to free it (Windows/macOS/Linux)
3. Falls back to scanning `3000–9999`, then OS-assigned ephemeral port
4. Prints `SERVER_READY:http://127.0.0.1:PORT/` when ready — open that URL

The server binds to `127.0.0.1` only. Press `Ctrl+C` to stop.

---

## VS Code debugging

Preconfigured launch targets in `.vscode/launch.json`:

| Configuration | Behavior |
|---------------|----------|
| **Debug Portfolio (Chrome)** | Starts dev server, opens Chrome at detected URL, attaches debugger |
| **Debug Portfolio (Edge)** | Same flow with Microsoft Edge |
| **Dev Server Only** | Runs `scripts/dev-server.mjs` in the integrated terminal |

**Quick start:** Open this folder → press **F5** → choose Chrome or Edge.

The background task watches for `SERVER_READY:` in terminal output (see `.vscode/tasks.json`) so the browser opens on the actual port even when 8080 is unavailable.

---

## Deployment

This repo is a **GitHub Pages user site** (`username.github.io`).

1. Push changes to the `main` branch on `origin`
2. GitHub Pages serves the root automatically (Settings → Pages → source: `main` / root)
3. `.nojekyll` ensures files and folders starting with `_` are not processed by Jekyll

**Production has no Node dependency** — GitHub serves `index.html`, `style.css`, images, and PDFs as static files.

After deploy, verify:

- [https://rohaan2802.github.io/](https://rohaan2802.github.io/)
- Resume link: `resume/Mohammad_Rohaan_Resume.pdf`
- [Google Search Console](https://search.google.com/search-console) (verification file included)

---

## Updating content

| What to change | Where |
|----------------|-------|
| Copy, projects, skills, contact info | `index.html` |
| Colors, spacing, layout, responsive rules | `style.css` (bump `?v=` on the CSS link in HTML to bust cache) |
| Resume PDF | Run `python scripts/build-resume.py` (writes `resume/Mohammad_Rohaan_Resume.pdf`) |
| Profile / OG image | Replace `images/portfolio_img.png` |
| Favicon | Replace `images/icon.png` |
| PWA name, colors, icons | `manifest.json` |
| Sitemap last modified date | `sitemap.xml` |

### Adding a project card

Copy an existing `<article class="project-card">` block in `#projects`, then update:

- Title, tags (`.tag` spans), short description
- `<details>` bullet list for deep-dive
- GitHub link in `.project-actions` (add `project-actions-dual` plus a Live demo button when a public URL exists)

### CSS cache busting

```html
<link rel="stylesheet" href="style.css?v=22" />
```

Increment `v=` after CSS changes so returning visitors get fresh styles.

---

## SEO & discoverability

| File | Purpose |
|------|---------|
| `index.html` `<head>` | Description, keywords, author, canonical, OG/Twitter meta |
| JSON-LD script | Schema.org `WebSite` and `Person` with LinkedIn/GitHub `sameAs` |
| `robots.txt` | Allows all crawlers; points to sitemap |
| `sitemap.xml` | Lists homepage URL and `lastmod` |
| `google9aef6604bac35f6b.html` | Google site ownership verification |
| `manifest.json` | App name, theme colors, standalone display |

---

## Design system

Defined in `style.css` via CSS custom properties:

| Token | Role |
|-------|------|
| `--bg`, `--text`, `--muted` | Surfaces and typography |
| `--accent`, `--accent-2`, `--accent-warm` | Brand purple, cyan, warm highlight |
| `--accent-gradient` | Hero accent text, back-to-top control |
| `--radius-sm/md/lg` | Corner radii (12px / 18px / 26px) |
| `--container` | Max content width (1120px) |
| `--header-h` | Sticky header height (72px) |

Light mode overrides apply automatically when the OS prefers light color scheme. Component classes include `.btn-primary`, `.btn-ghost`, `.card`, `.project-card`, `.tag`, `.site-nav`, etc.

---

## Browser behavior

**Mobile navigation:** Toggle button sets `data-open` on nav; Escape closes; link click closes menu.

**Back to top:** Appears after scrolling ~17% of viewport height (clamped 100–300px).

**Email links:** On `(hover: hover) and (pointer: fine)` devices, `mailto:` clicks are intercepted to open Gmail compose with pre-filled To/subject/body. Mobile/touch keeps standard `mailto:` behavior.

**Reduced motion:** Animations and transitions disabled when `prefers-reduced-motion: reduce`.

---

## Assets

| Path | Usage |
|------|-------|
| `images/portfolio_img.png` | Hero photo, Open Graph, Twitter card |
| `images/icon.png` | Favicon (`<link rel="icon">`) |
| `images/icon6.png` | Referenced in `manifest.json` for 192×192 and 512×512 PWA icons — ensure this file exists or update manifest paths |
| `images/resume_img.png` | Supplementary resume imagery |
| `images/linkedin_background.png` | LinkedIn-related asset |
| `resume/Mohammad_Rohaan_Resume.pdf` | Downloadable resume (linked from nav, hero, about) |

---

## Contact & links

| | |
|---|---|
| **Portfolio** | [rohaan2802.github.io](https://rohaan2802.github.io/) |
| **GitHub** | [github.com/rohaan2802](https://github.com/rohaan2802) |
| **LinkedIn** | [linkedin.com/in/m-rohaan-944a82320](https://www.linkedin.com/in/m-rohaan-944a82320/) |
| **Email** | m.rohaanarshad@gmail.com |
| **University** | FAST NUCES Islamabad — i222327@nu.edu.pk |

---

## License

© Mohammad Rohaan. Portfolio content, resume, and site design are personal property. Project source code for featured work lives in linked GitHub repositories under their respective licenses.

---

*Built for clarity, speed, and credibility.*
