# Push to GitHub (Windows)

1. Install Git from https://git-scm.com/downloads and verify with `git --version`.
2. In PowerShell, enter the project folder.
3. Verify `.env` is ignored: `git check-ignore .env`.
4. Run:
```powershell
git init
git add .
git status
git commit -m "Build financial risk analysis and rule-based alert system"
git branch -M main
```
5. Create an empty GitHub repository named `financial-risk-fraud-detection`, without adding a README or `.gitignore`.
6. Connect and push:
```powershell
git remote add origin https://github.com/YOUR-USERNAME/financial-risk-fraud-detection.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your username. Later updates:
```powershell
git add .
git commit -m "Describe your change"
git push
```
Never commit `.env`, credentials, database files, or real financial data.
