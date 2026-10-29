# Automated Time Tracking & Data Validation System

A static case-study website documenting the n8n, JavaScript, and Google Workspace timesheet workflow. It has no build step or runtime dependencies.

## Local preview

From this project directory, run:

```powershell
python -m http.server 4173 --directory public
```

Then open `http://localhost:4173`.

The generated deployment site lives in `public/`. The source Excel workbook stays in the project root and is excluded from the static site.

## Vercel

Import the repository in Vercel and set the project root to this directory. Set the output directory to `public`; no build command or environment variables are needed. The `.vercelignore` file limits deployment to that directory.

Alternatively, install the Vercel CLI and run `vercel --prod` from this directory. Review the files selected for deployment before publishing.

## Rebuild image copies

If source screenshots change, run `python build_site.py`. The script copies original screenshots and creates web-sized previews under `public/assets/images/`, including the approved sanitized Gmail notification screenshot.
