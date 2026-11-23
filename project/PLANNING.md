# Pacman Project: Planning & Progress Tracker

> Template: replace the `TODO` values with real information.
> Start: **Fri 2026-11-20 at 14:00**. No weekend work. Deadline: **Thu 2026-11-26** (5 working days).

## 1. Overview

| | |
|---|---|
| **Project** | Pacman (42 school) |
| **Deadline** | Thu 26/11, end of day (TODO: exact time) |
| **Availability (each)** | Fri 20/11 14:00-19:00 (5h) · Mon 23 → Thu 26/11 09:00-17:00 (8h/day) · **37h total** |
| **Planned workload** | A ≈ 36h · B ≈ 36h (≈ 1h of slack each) |
| **Team** | **A**: TODO name (experienced) · **B**: TODO name (learning) |
| **Stack** | Python, Pygame-CE, JSON, external maze-generation package |
| **Repo** | TODO link |

### Working principle

Tasks are **deliberately split unevenly**. B takes self-contained, lower-risk modules where she can learn a skill end to end (JSON, simple Pygame screens, small game elements). A takes the modules on the critical path (maze integration, movement, ghosts, rendering, main loop) and reviews B's work. Each of B's tasks is paired with a short review/pairing session so she learns from the feedback.

---

## 2. Work breakdown

Difficulty: 🟢 easy · 🟡 medium · 🔴 hard. Estimates are in working hours.

### Configuration (skill: JSON)

| ID | Task | Owner | Diff. | Est. | Depends on |
|----|------|:-----:|:-----:|:----:|------------|
| C1 | Read and validate the JSON config file (error handling) | B | 🟢 | 4h | - |
| C2 | Integrate the maze package and convert its output into the game map | A | 🟡 | 2h | C1, G4 |

### Scores (skill: JSON)

| ID | Task | Owner | Diff. | Est. | Depends on |
|----|------|:-----:|:-----:|:----:|------------|
| S1 | Save scores to a file | B | 🟢 | 3h | C1 |
| S2 | Load / sort / display best scores | B | 🟢 | 2h | S1 |

### Game (skill: Pygame)

| ID | Task | Owner | Diff. | Est. | Depends on |
|----|------|:-----:|:-----:|:----:|------------|
| Ga | Discover Pygame (A) | A | 🟢 | 6h | X1 |
| Gb | Discover Pygame (B) | B | 🟡 | 6h | S1 |
| G0 | Main game loop | A | 🟢 | 1h | Ga |
| G1 | Player entity + input handling + movement/collisions | A | 🟡 | 3h | G0, C2 |
| G2 | Ghost entities + movement/AI | A | 🔴 | 3h | G1 |
| G3 | Pacgums and other minor elements (bonuses, etc.) | B | 🟡 | 6h | Gb |
| G4 | Rendering (maze, entities, HUD) | A | 🟡 | 6h | G0 |

### App / Main program (skill: Pygame)

| ID | Task | Owner | Diff. | Est. | Depends on |
|----|------|:-----:|:-----:|:----:|------------|
| M1 | App state machine (menu → game → end → retry/exit) | A | 🟡 | 6h | G4 |
| M2 | Main menu | B | 🟡 | 6h | M1 (work against a stub until it lands) |
| M3 | Victory / game-over screen | B | 🟡 | 3h | M2, S2 |

### Cross-cutting

| ID | Task | Owner | Diff. | Est. | Depends on |
|----|------|:-----:|:-----:|:----:|------------|
| X1 | Repo setup, Makefile, structure, linting (flake8/mypy) | A | 🟢 | 3h | - |
| X2 | Integration, bug fixing, playtesting | A + B | 🟡 | 4h | all |
| X3 | README, docstrings, final checks, evaluation prep | A + B | 🟢 | 2h | X2 |

---

## 3. Planned timeline

Rendered natively on GitHub / GitLab / most Markdown viewers (Mermaid).
Tasks tagged `crit` are on the critical path. Tasks that span two days are split in two bars (1/2, 2/2).

```mermaid
gantt
    title Planned timeline (Fri 20/11 14:00 to Thu 26/11)
    dateFormat YYYY-MM-DD HH:mm
    axisFormat %a %d/%m
    excludes weekends

    section A (experienced)
    X1 Repo Makefile structure           :x1, 2026-11-20 14:00, 3h
    Ga Discover Pygame (1/2)             :ga1, 2026-11-20 17:00, 2h
    Ga Discover Pygame (2/2)             :ga2, 2026-11-23 09:00, 4h
    G0 Main game loop                    :g0, 2026-11-23 13:00, 1h
    G4 Rendering (1/2)                   :g4a, 2026-11-23 14:00, 3h
    G4 Rendering (2/2)                   :g4b, 2026-11-24 09:00, 3h
    C2 Maze integration                  :crit, c2, 2026-11-24 12:00, 2h
    M1 App state machine (1/2)           :crit, m1a, 2026-11-24 14:00, 3h
    M1 App state machine (2/2)           :crit, m1b, 2026-11-25 09:00, 3h
    G1 Player + movement                 :crit, g1, 2026-11-25 12:00, 3h
    G2 Ghosts (1/2)                      :g2a, 2026-11-25 15:00, 2h
    G2 Ghosts (2/2)                      :g2b, 2026-11-26 09:00, 1h

    section B (learning)
    C1 Read JSON config                  :c1, 2026-11-20 14:00, 4h
    S1 Save scores (1/2)                 :s1a, 2026-11-20 18:00, 1h
    S1 Save scores (2/2)                 :s1b, 2026-11-23 09:00, 2h
    Gb Discover Pygame                   :gb, 2026-11-23 11:00, 6h
    G3 Pacgums and minor elements        :g3, 2026-11-24 09:00, 6h
    S2 Load / display scores             :s2, 2026-11-24 15:00, 2h
    M2 Menu                              :m2, 2026-11-25 09:00, 6h
    M3 Victory / game-over (1/2)         :m3a, 2026-11-25 15:00, 2h
    M3 Victory / game-over (2/2)         :m3b, 2026-11-26 09:00, 1h

    section Both
    X2 Integration and playtesting       :crit, x2, 2026-11-26 10:00, 4h
    X3 README and final checks           :x3, 2026-11-26 14:00, 2h
```

*Weekend (Sat 21 / Sun 22) is skipped. Daily windows are in section 1.*

---

## 4. Real progress

Status: ⬜ not started · 🟦 in progress · ✅ done · ⚠️ late · ❌ blocked

| ID | Owner | Planned end | Actual end | Status | Δ (h) | Notes / blockers |
|----|:-----:|:-----------:|:----------:|:------:|:-----:|------------------|
| X1 | A | Fri 20/11 17:00 | Fri 20/11 14:00 | ✅ | | |
| C1 | B | Fri 20/11 18:00 | Mon 23/11 17:00 | ✅ | | |
| S1 | B | Mon 23/11 11:00 | TODO | ✅ | | |
| Ga | A | Mon 23/11 13:00 | TODO | ⬜ | | |
| G0 | A | Mon 23/11 14:00 | TODO | ⬜ | | |
| Gb | B | Mon 23/11 17:00 | TODO | ⬜ | | |
| G4 | A | Tue 24/11 12:00 | TODO | ⬜ | | |
| C2 | A | Tue 24/11 14:00 | TODO | ⬜ | | |
| G3 | B | Tue 24/11 15:00 | TODO | ⬜ | | |
| S2 | B | Tue 24/11 17:00 | TODO | ⬜ | | |
| M1 | A | Wed 25/11 12:00 | TODO | ⬜ | | |
| M2 | B | Wed 25/11 15:00 | TODO | ⬜ | | |
| G1 | A | Wed 25/11 15:00 | TODO | ⬜ | | |
| G2 | A | Thu 26/11 10:00 | TODO | ⬜ | | |
| M3 | B | Thu 26/11 10:00 | TODO | ⬜ | | |
| X2 | A+B | Thu 26/11 14:00 | TODO | ⬜ | | |
| X3 | A+B | Thu 26/11 16:00 | TODO | ⬜ | | |

**Δ (h)** = actual end − planned end, in working hours (positive = late, negative = early).

---

## 5. Risks

| Risk | Impact | Likelihood | Mitigation |
|------|:------:|:----------:|------------|
| Other student's maze package has a poor API / bugs | 🔴 | TODO | Read its docs on Day 1; wrap it in a small adapter class |
| Only ~1h of slack each: any delay hits the deadline | 🔴 | TODO | Cut in this order: ghost AI → random movement, menu → bare minimum, bonuses (G3) → pacgums only |

---

## 6. Definition of done

- [ ] Game runs from `make run` with the config file
- [ ] All subject requirements are covered (TODO: check against the subject)
- [ ] `make lint` passes
- [ ] No crash on invalid config / missing score file
- [ ] README and docstrings complete
- [ ] Both members can explain every part of the code (evaluation!)
