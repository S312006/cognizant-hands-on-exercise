# Hands-On 7 [Advanced] — Migrations & Versioning with Alembic

All commands below assume you're in `Module3_DatabaseIntegration/Sharmi/orm/` in PowerShell,
with `models.py` already in this folder from Hands-On 6.

---

## Task 1: Set Up Alembic and Create a Baseline Migration

```powershell
pip install alembic --break-system-packages   # skip --break-system-packages if not needed
alembic init migrations
```

This creates `alembic.ini` and a `migrations/` folder.

**Edit `alembic.ini`** — find the line starting `sqlalchemy.url =` and replace with:
```ini
sqlalchemy.url = postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/college_db_orm
```

**Edit `migrations/env.py`** — near the top, after the existing imports, add:
```python
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Base
target_metadata = Base.metadata
```
Replace the existing `target_metadata = None` line with the one above.

**Generate and apply the baseline migration:**
```powershell
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
alembic current
```

Check `migrations/versions/<hash>_initial_schema.py` — confirm it has both an `upgrade()`
and `downgrade()` function populated with `op.create_table(...)` calls for all 5 tables.

---

## Task 2: Add and Apply Incremental Migrations

### Step 1 — add `is_active` to Student
If you commented it out earlier, uncomment this line in `models.py` under `Student`:
```python
is_active = Column(Boolean, default=True)
```

```powershell
alembic revision --autogenerate -m "add is_active to students"
alembic upgrade head
```
Open the new file in `migrations/versions/` and confirm:
```python
def upgrade():
    op.add_column('students', sa.Column('is_active', sa.Boolean(), nullable=True))

def downgrade():
    op.drop_column('students', 'is_active')
```

### Step 2 — add CourseSchedule table
If commented out, uncomment the `CourseSchedule` class and the `schedules` relationship
on `Course` in `models.py`.

```powershell
alembic revision --autogenerate -m "add course_schedules table"
alembic upgrade head
```

### Step 3 — view full history
```powershell
alembic history --verbose
```
Expected: 3 revisions listed (initial schema → is_active → course_schedules).

---

## Task 3: Rollback and Recovery

```powershell
# Note current head
alembic current

# Roll back one step - confirms is_active/course_schedules logic reverses cleanly
alembic downgrade -1

# Roll back everything to the very start
alembic downgrade base

# Re-apply everything
alembic upgrade head
alembic current
```

Verify in your SQL client (psql or pgAdmin) after each downgrade/upgrade:
```sql
\d students          -- is_active column should appear/disappear accordingly
\d course_schedules  -- table should appear/disappear accordingly
SELECT * FROM alembic_version;
```

---

## Bonus: Django Migrations equivalent (if using Django ORM instead)

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py migrate <app_name> <previous_migration_number>   # rollback example
```

---

## Submission checklist
- [ ] `migrations/` folder (Alembic-generated) with all 3 versioned revision files
- [ ] `alembic.ini` (with your DB URL, or a placeholder if pushing to GitHub publicly)
- [ ] Screenshot or `.txt` of `alembic history --verbose` output
- [ ] Confirmation notes: column/table present after upgrade, absent after downgrade
