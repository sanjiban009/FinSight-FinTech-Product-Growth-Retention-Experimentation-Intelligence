# GitHub upload & GitHub Pages — step by step

The project is already a complete static website, with locally bundled JavaScript and data. **No framework, paid hosting, API keys, server, SQL database or build step is required.**

### A. Create your repository

1. Visit https://github.com/new while logged in.
2. Repository name: `fintech-product-growth-intelligence` (recommended).
3. Description: `FinSight — 7-page interactive FinTech product growth, retention, A/B testing & churn prediction dashboard | HTML, Plotly, Excel, Python`.
4. Set **Public**. Click **Create repository**.
5. Choose **Add file → Upload files**.
6. **Unzip** the downloaded package locally. Upload the extracted **contents** of the `fintech_product_intelligence` folder, **not the parent folder itself**. `index.html` must be in the repository root next to `README.md`.
7. Upload the entire `assets`, `data`, `docs`, `screenshots` and `tools` folders, plus root files. Use **Commit changes**.
8. Inspect the repository root to confirm `index.html` and `assets/vendor/plotly.min.js` are visible. The Plotly file is roughly 4.8 MB; GitHub's normal web upload supports files this size.

### B. Turn on GitHub Pages

1. Open the repository **Settings**.
2. Choose **Pages** in the left navigation (under Code and automation on most layouts).
3. Under **Build and deployment**, select **Deploy from a branch**.
4. For Branch select **main** and folder **/(root)**. Press **Save**.
5. Once GitHub shows a published site URL, open it and click every page. It should look like the included screenshots.
6. Expected URL pattern *only after successful deployment*: `https://sanjiban009.github.io/fintech-product-growth-intelligence/`. **This is a predicted pattern, not a verified live deployment.**
7. If you see 404, verify your repository's Pages settings, correct branch, file placement and actual GitHub deployment status.

### C. Add to your profile and LinkedIn

- Repo **About** → Website: paste the successfully published GitHub Pages link.
- Repo About topics: `fintech`, `business-intelligence`, `product-analytics`, `customer-retention`, `ab-testing`, `cohort-analysis`, `plotly`, `javascript`, `machine-learning`, `portfolio`.
- Add the live site and repository to LinkedIn's **Featured** section, alongside the LinkedIn carousel post.
- Use `docs/LINKEDIN_POST.txt`, then replace the marked placeholders with real published links.

### D. Test after deployment

- [ ] Executive KPIs load and are legible.
- [ ] Selecting FY 2025–26 changes the sign-up and trade measures.
- [ ] Region / channel / device / segment dropdowns work.
- [ ] Clicking geographic and channel bar charts updates the global filters.
- [ ] All 7 pages show charts and metrics.
- [ ] A/B test for FY 2024–25 correctly shows zero exposed users (test begins FY 2026–27).
- [ ] Filtered user CSV can be downloaded.
- [ ] Footer doesn't imply affiliation with CoinDCX.

### Troubleshooting

- **Broken graphs:** preserve the original `assets/vendor/plotly.min.js` path.
- **Data not showing:** preserve `data/dashboard-data.js`, which is loaded through a `<script>` tag, not a network fetch.
- **404 / blank page:** ensure `index.html` is in the root of the selected Pages branch/folder.
- **Slow upload:** use GitHub Desktop or `git` command line if the web browser struggles with many data files.
- **Readme image broken:** ensure `screenshots/01_executive_linkedin.jpg` is uploaded.

Do not describe deployment as live until GitHub displays a working Pages URL.
