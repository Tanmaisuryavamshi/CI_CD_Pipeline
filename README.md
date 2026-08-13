# Shopping Cart Demo — Jenkins + Pytest + Allure

A small, realistic Python module (`src/cart.py`) with a full pytest suite
(`tests/test_cart.py`) annotated for Allure — built to demo a CI test
pipeline in Jenkins.

## What it tests

- Adding items (success, unknown SKU, out-of-stock, invalid quantity)
- Discount codes (valid codes, invalid code)
- Checkout (empty cart error, correct total with discount, stock deduction, cart reset)
- Removing items (partial removal, full removal, item not in cart)

16 tests across 4 features/stories, with severities (BLOCKER, CRITICAL,
NORMAL, MINOR) and `allure.step()` breakdowns — this gives the Allure
report real structure to show off (categories, severity chart, timeline).

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate       # venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run tests, generate both JUnit and Allure raw results
pytest tests/ --junitxml=report.xml --alluredir=allure-results

# Generate and open the HTML Allure report (requires Allure commandline)
allure serve allure-results
```

If you don't have the Allure commandline tool locally:
- macOS: `brew install allure`
- Others: download from https://github.com/allure-framework/allure2/releases

## Run in Jenkins

1. Push this folder to a Git repo.
2. In Jenkins: **Manage Jenkins → Plugins** → install **Allure Jenkins Plugin**.
3. **Manage Jenkins → Tools** → add an **Allure Commandline** installation
   (check "Install automatically" — no manual setup needed).
4. **New Item → Pipeline → Pipeline script from SCM**, point at the repo,
   script path `Jenkinsfile`.
5. Click **Build Now**.
6. On the build/job page, you'll see:
   - **Test Result** (JUnit trend graph)
   - **Allure Report** (detailed HTML report — features, severities, steps, timeline)

## Demo tips

- Break one test on purpose before the demo (e.g. change `0.10` to `0.15`
  in the SAVE10 assertion) and show the red build + the failure detail in
  Allure, then fix it and show it go green — much more convincing live
  than an all-green run from the start.
- Point out the **Categories** and **Severity** tabs in the Allure report —
  that's the part that usually impresses non-technical stakeholders most.
