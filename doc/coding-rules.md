# AI Coding Constitution

**Purpose:**  
Ensure all generated code is maintainable, non-duplicative, backward-compatible, and fully tested without removing or breaking existing functionality.

---

## 1. Code Structure
- Each page/module in its own `.py` file.  
- Keep files between **1,000–2,000 lines max**. Split if larger.  
- No unused imports, variables, or dead code.  
- Avoid code duplication — reuse existing code whenever possible.  

---

## 2. Change Safety
- **Never remove existing functionality** unless explicitly approved.  
- Maintain **backward compatibility** for changed methods.  
- Add features without breaking current behavior.  

---

## 3. Testing Rules
- All new/modified code must include or update **unit tests**.  
- Store all tests under `/test_program`, mirroring source structure.  
- After changes, **all tests must pass** — no regressions allowed.  
- Minimum test coverage: **80%**.  

---

## 4. Documentation & Readability
- Use concise docstrings for all public classes and methods.  
- Comment *why* logic exists, not just *what* it does.  
- Add file header with:  

# Version: X.Y
# Last Modified: YYYY-MM-DD
# Changes: <summary>

- Apply consistent formatting (e.g., `black` or `autopep8`).  

---

## 5. Code Generation Process
- Show **diff of changes** before overwriting existing files.  
- Only create new files if absolutely required.  
- No unnecessary dependencies — all new packages must be approved.  
- Handle exceptions gracefully — log errors, never silently ignore them.  

---

## 6. Quality Enforcement
Before finalizing code:
1. Check for duplicate classes, methods, or functions.  
2. Verify all old and new tests pass.  
3. Ensure code meets naming, formatting, and docstring requirements.  
4. Confirm file sizes remain within limits.  


## 7. UI & Data Standards
- All UI elements must use consistent styles, fonts, and components across all pages/modules.
- Do not hardcode information in code or UI; all displayed data must come from the database or be calculated using approved, industry-standard methods.
- Ensure calculations and business logic follow recognized industry standards and are documented.

