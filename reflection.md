# PawPal+ Project Reflection

## 1. System Design

### a. Initial design

- **UML Design**: My original conceptual design mapped a clear hierarchy linking users to their pets and tasks.
- **Classes**: I structured the system using `Owner` (top-level profile managing a list of pets), `Pet` (composition object holding a list of tasks), `Task` (the base data model containing priority, frequency, and time properties), and `Scheduler` (the "Brain" that isolates complex algorithmic logic away from the data models).

### b. Design changes

- **Design Change**: Yes, the initial codebase started as a single monolithic script (`pawpal_system.py`). I refactored it into a modular `core/` directory package (`owner.py`, `pet.py`, `task.py`, `scheduler.py`) to properly separate my Domain Logic from the Streamlit UI presentation logic in `app.py`.

---

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and priorities

- **Constraints**: My scheduler places extreme emphasis on evaluating `Priority` (High, Medium, Low), `Chronological Time`, and `Frequency/Date` mappings for recurring tasks.
- **Decision Logic**: Because a pet might have a critical "High Priority" task late in the evening (like Heartworm medication), I implemented a dual-sort function (`sort_by_priority_then_time`) making sure High severity items are surfaced explicitly first so they are never missed by the owner!

### b. Tradeoffs

- **Describe one tradeoff your scheduler makes:**
  Our `detect_conflicts` method only checks for _exact_ time matches instead of calculating overlapping duration windows (e.g., checking if an 08:00 task taking 45 minutes overlaps an 08:30 task).
- **Why is that tradeoff reasonable for this scenario?:**
  Calculating exact overlapping minutes can increase algorithmic complexity. By only checking exact start times, we keep the algorithm extremely fast `O(n log n)` relying on Python's `sorted` function. For a personal pet tracker, this is a perfect tradeoff since tasks are usually brief, and the user primarily just needs a gentle reminder about accidental double-booking.

---

## 3. AI Collaboration

### a. How you used AI

- **AI Tools**: I used **Gemini** and **Claude** extensively for architectural refactoring (splitting my single file into a python package), generating industry-standard QA tests via `pytest`, and debugging logic flaws in my object instantiation scripts.
- **Chat Organization**: Using separate chat threads for different phases in the LLM web interfaces (e.g., one chat for Phase 1 System Design, and a fresh chat for Phase 2 Core Implementation) was crucial. It prevented the AI's context window from getting cluttered with outdated monolithic code, ensuring it only focused on the specific modular task at hand.
- **Helpful Prompts**: Asking the AI "Why is this test failing?" when my recurrence logic returned the wrong `completed` boolean value proved incredibly valuable for surfacing logic bugs.

### b. Judgment and verification

- **Judgment Call**: I did not always accept AI architectural updates blindly. When an AI suggested rewriting my `scheduler.py` entirely, I opted to manually integrate just the master list sorting functions instead to ensure it perfectly matched my custom frequency filtering needs.
- **Evaluation**: I relied heavily on strict `pytest` suites adhering to the AAA (Arrange, Act, Assert) strategy. If a snippet from Gemini or Claude couldn't pass my standalone terminal assertions, I prompted the model with the exact terminal error traceback and forced it to refine the algorithm until it passed.

---

## 4. Testing and Verification

### a. What you tested

- **Behaviors Tested**: Chronological sorting, `timedelta` offset recurrence logic (verifying +1 day jumping), conflict matching array lists, and default data instantiation.
- **Importance**: Because my UI (`app.py`) updates reactively and passes complex `datetime` data directly from the user to the algorithms, these formal tests act as a safety net stopping bad user-driven data from crashing the app execution.

### b. Confidence

- **Confidence**: 5/5 stars (⭐⭐⭐⭐⭐). The algorithmic backend processes everything flawlessly.
- **Future Edge Cases**: Next iteration, I would implement robust automated tests to handle `Timezone` offsets and DST (Daylight Savings Time) transitions, which could temporarily throw off my timezone-agnostic `timedelta` loops.

---

## 5. Reflection

### a. What went well

- **Satisfaction**: I am wildly satisfied with the `core/` package modularity. Utilizing Python's `dataclass` capabilities and leveraging native `O(n log n)` TimSort integrations (via lambda keys) created an extremely clean backend!

### b. What you would improve

- **Improvements**: Relying on `pawpal_data.json` for serialization works, but it causes significant concurrent write hazards if a user has the app open on multiple screens. Next time, I'd integrate a true SQL backend (like `SQLite` or `PostgreSQL`) linked to a python ORM like SQLAlchemy for safe multi-session scaling.

### c. Key takeaway

- **Takeaway**: Acting as the "lead architect" taught me that AI is a powerful builder, but it still needs strong human direction. True professional software development requires extremely clear boundaries between application state and UI rendering! Pulling my core algorithms violently out of the Streamlit `app.py` script and putting them in their own file architecture allowed me to manage the AI effectively, rather than letting it turn the project into spaghetti code.

---

## 6. Stretch Goal: Multi-Model Prompt Comparison

- **The Test**: I chose a complex algorithmic task—writing the `handle_recurrence` logic using Python's `timedelta`—and asked for a solution from both **Gemini** and **Claude**.
- **The Result**: While both models wrote functional code, **Gemini** provided a more "Pythonic" solution because it **relied entirely on Python's built-in `datetime.timedelta` shifting without requiring external libraries, and it generated a much cleaner, self-documenting implementation returning a fully populated `Task` object ready for JSON serialization.**
