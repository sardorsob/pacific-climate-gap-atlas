# Workflow Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Initialize a context-first repository shell for the Pacific Adaptation Gap Atlas.

**Architecture:** Durable project context lives in `context/`; Python analysis code lives in `analysis/`; CLI orchestration lives in `scripts/`; the future GIS website lives in `app/`. Generated data and artifacts are separated from source research.

**Tech Stack:** Python, pandas/numpy/scikit-learn for analysis, React/Vite/TypeScript/MapLibre for the app, Markdown workflow docs.

---

### Task 1: Repository Control Plane

**Files:**
- Create/modify root metadata, config files, and `context/` workflow documents.

- [x] Create `.gitignore` that ignores local reference kits, raw/interim data, environments, build outputs, and run bundles.
- [x] Add root README and package metadata.
- [x] Add context-first workflow docs under `context/`.
- [x] Add data/model/index/app configuration files under `configs/`.

### Task 2: Analysis And App Scaffolds

**Files:**
- Create `analysis/`, `scripts/`, `app/`, `data/`, `artifacts/`, and `tests/` skeletons.

- [x] Create Python package boundaries for IO, preprocessing, features, modeling, evaluation, uncertainty, viz, and utils.
- [x] Create CLI script stubs that fail honestly until task-specific implementation.
- [x] Create React/Vite app shell with map-oriented layout placeholders.
- [x] Add `.gitkeep` and README files for generated data tiers.

### Task 3: Scaffold Verification

**Files:**
- Create validation scripts under `scripts/`.

- [x] Add required-artifact checker.
- [x] Add task-status checker.
- [x] Add lightweight secret scanner.
- [x] Run scaffold verification scripts.
- [x] Update `context/TASKS.md` scaffold QA notes.
- [x] Commit as `chore(scaffold): initialize workflow shell`.
