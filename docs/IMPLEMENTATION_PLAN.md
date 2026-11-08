# CRM Application — Prioritized Modernization Plan

> This is a proposed plan based on static inspection of the supplied repository snapshot. It is not authorization to implement every change immediately. Preserve existing data and business behavior; validate each phase before proceeding.
>
> Public-repository rule: do not include business identity, product catalog, distributor names, branded form titles, or other commercially identifying content in public code, documentation, examples, screenshots, or commit messages. Keep such configuration in local, untracked configuration or a private deployment secret store.

## Guiding principles

1. Preserve the existing Flask + SQLAlchemy + MySQL + HTML/CSS/vanilla-JS architecture initially.
2. Do not rewrite the application before its behavior and data have been captured in tests.
3. Back up the database before any schema or data migration.
4. Make database changes additive and reversible where practical.
5. Keep business-specific labels and option lists configurable outside the public repository.
6. Never treat a successful static syntax check as proof of runtime correctness.
7. Work on a dedicated feature branch; do not modify or merge `main` during development.

## Owner decisions (confirmed)

- Deployment: one user on one computer; keep the application local-only by default.
- Identity rule: one form per identity document. The intended database rule is a unique combination of `tipo_documento` + `numero_documento`; confirm normalization/case/whitespace rules before adding the constraint.
- Configuration: use `.env` for secrets/runtime settings and an ignored `config/local.json` for private labels and form options.

## Phase 0 — Baseline, backup, and requirements confirmation

**Goal:** establish a safe baseline before changing behavior.

- Capture the current repository revision and a clean working-tree snapshot.
- Obtain a real database backup from the current installation, if one exists; test restoring it into a separate local database.
- Inventory actual customer/referral fields and which are actively used by the business workflow.
- Confirm whether document numbers are allowed to repeat across multiple forms. **Resolved: no; one form per identity document.**
- Confirm whether the form number must be sequential, whether gaps are acceptable, and whether deleted numbers may ever be reused (recommended: never reuse).
- Confirm which form-level fields currently shown in the UI must be stored, including configurable product/category and distributor selections.
- Identify whether the CRM is strictly single-user/local or will be accessed by multiple users/devices. **Resolved: one user on one computer.** Keep services loopback-bound; authentication can remain deferred while the application is strictly local and is not exposed to a LAN or public network.

**Acceptance:** written field inventory, business-rule checklist, backup file, and successful restore test. The owner decisions above are now recorded. A real database backup/restore test is still pending before any schema migration.

## Phase 1 — Remove public secrets and isolate private configuration

<badge>Implemented in this working copy — static checks only</badge>

**Priority:** Critical.

**Findings:** database credentials are hard-coded in backend source and Compose configuration; the same credential is used for application and root database access. Business-specific content appears in public-facing source, README, sample assets, and model naming.

**Proposed work:**

- Rotate any credential that has been committed to the public repository. Do not reuse the exposed value.
- Introduce environment-based configuration for database host, port, database, application username, and password. **Implemented:** `backend_api.py` now reads these settings from environment variables and refuses to start without `MYSQL_PASSWORD`.
- Use a least-privilege database account for the application; keep root credentials separate and out of the API container.
- Add `.env.example` with placeholders only; add `.env`, local business configuration, generated data, and backups to `.gitignore`. **Implemented:** `.env.example`, `.gitignore` rules, and generic `config/local.example.json` are present. A local ignored `config/local.json` was created from the existing form choices for this working copy only; do not commit or publish it.
- Move business-specific labels and option lists to a local configuration file that is not committed. Provide a generic example configuration with fictional values. **Implemented for form title, gift/distribution options, and the referral question label:** `web_server.py` exposes only an allowlisted presentation configuration through `/app-config`; `scripts/config.js` loads it and populates the form.
- Replace public README wording and screenshots with generic CRM language/assets. Review `form.html`, JavaScript labels, sample-data generator, SQL examples, diagrams, and image assets for identifying information. **Implemented:** README and tracked form/diagram labels are generic. The mockup image still requires a visual privacy review before being retained publicly.
- If credentials or private details were committed historically, decide whether to clean Git history after rotation and coordinate force-push with all repository collaborators. Rotation is mandatory even if history is rewritten.

**Files changed:** `backend_api.py`, `web_server.py`, `docker-compose.yml`, `form.html`, `scripts/form.js`, new `scripts/config.js`, `README.md`, `.gitignore`, `.env.example`, `config/local.example.json`, and the Draw.io diagram. `config/local.json` is local-only and ignored by Git.

**Checks completed:** Python syntax compilation; JavaScript syntax checks; static search for the exposed credential and known business-specific strings in the public source snapshot. Docker Compose validation, Flask runtime/config endpoint tests, MySQL connection, browser behavior, and credential rotation remain pending because Docker/MySQL and the Python Flask dependencies are not available in this execution environment. The API and web ports now bind to loopback; MySQL is not published to the host; debug is off by default; the web catch-all file route was removed and explicit HTML routes retained.

**Risk:** changing model field names or removing legacy columns can break existing databases. Do not rename/drop them in this phase.

## Phase 2 — Reliable Docker lifecycle and persistent database

<badge>Partially implemented in Phase 1</badge>

**Priority:** Critical.

**Findings:** MySQL has no named volume; startup ordering does not wait for database readiness; dependencies are installed on each container start; Flask debug mode is enabled; host ports are broadly published.

**Proposed work:**

- Add a named MySQL data volume and document that `docker compose down -v` deletes data. **Implemented:** named `mysql_data` volume and warning in README.
- Add a MySQL health check and make dependent services wait for healthy status. **Implemented:** MySQL healthcheck and API `depends_on: condition: service_healthy`.
- Build small application images with pinned dependencies rather than installing packages at every startup.
- Use explicit absolute entrypoint paths and ensure shell scripts have executable permissions.
- Disable debug mode by default; use a production WSGI server for non-development use. **Debug disabled by default; production WSGI server remains pending.**
- Bind services to the minimum required interfaces and expose only the web entry point by default. Keep database/API ports internal unless an explicit development profile requires them. **Implemented as loopback-only host bindings; MySQL has no host port.**
- Configure the API URL from deployment configuration rather than hard-coding `localhost` in browser JavaScript.
- Document startup, shutdown, upgrade, backup, and restore commands.

**Files likely affected:** `docker-compose.yml`, both entrypoint scripts, new Dockerfiles, `requirements.txt`, frontend API configuration, README.

**Tests:** fresh `docker compose up --build`; API readiness after MySQL initialization; restart retains data; backup/restore round-trip; no debug mode in production profile.

**Risk:** changing service names, network addresses, or volume names can affect existing installations. Preserve compatible names where possible and back up first.

## Phase 3 — Database schema, migrations, and integrity

**Priority:** Critical.

**Findings:** application tables are created through `db.create_all()` at API startup; there is no migration history. Customer department/city IDs and referral department/city IDs are not foreign keys. Document uniqueness is not enforced despite the duplicate-document error message. Required model constraints and API validation are inconsistent.

**Proposed work:**

- Introduce Flask-Migrate/Alembic and create an initial baseline migration that matches the current schema exactly.
- Verify the baseline against a copy of an existing database before applying it to production data.
- Add foreign keys for customer and referral location references after auditing and repairing invalid legacy IDs.
- Add explicit ORM relationships and define deletion behavior deliberately (cascade or explicit service-layer deletion, not both accidentally).
- Decide document uniqueness from actual business rules; add a unique constraint only if confirmed.
- Make form ID generation database-owned and concurrency-safe. Do not accept a client-provided primary key. Preserve existing IDs during migration and never reuse deleted IDs.
- Validate dates strictly; invalid dates should return a clear 400 rather than silently becoming NULL.
- Align API required-field validation with database nullability and browser requirements.
- Preserve the legacy branded column initially; design a staged compatibility migration to a generic configurable representation only after the data mapping is agreed.

**Files likely affected:** `backend_api.py`, new migrations directory, database migration docs, tests.

**Tests:** migration on empty DB; migration on a representative copy; FK validation; invalid input cases; concurrent ID allocation; delete behavior; rollback on failed migration.

**Risk:** high. Schema constraints can reject legacy rows. Produce a data-quality report and backup before enforcing constraints.

## Phase 4 — Atomic customer + referral API

**Priority:** Critical.

**Findings:** the browser creates the customer in one request and each referral in a separate request. Each request commits independently, so partial forms are possible. Referral insertion uses `Referido(**data)` and accepts caller-supplied model fields.

**Proposed work:**

- Add a single endpoint such as `POST /api/forms` accepting `{ customer: {...}, referrals: [...] }`.
- Validate the complete payload before writing.
- Use explicit allowlists for customer and referral fields; never pass arbitrary request dictionaries into ORM constructors.
- Insert the customer, obtain its server-generated ID, insert all referrals, and commit once inside a transaction.
- Roll back the whole operation if any referral fails.
- Return the created form ID and a stable response schema.
- Add structured error responses without exposing SQL, stack traces, credentials, or raw database exception text.
- Keep old endpoints temporarily if compatibility is needed; deprecate only after the frontend is migrated.

**Files likely affected:** `backend_api.py`, `scripts/api.js`, `scripts/form.js`.

**Tests:** valid form with zero/one/many referrals; failure on referral N leaves no partial customer or referral rows; invalid field rejected; caller cannot set IDs or reassign referral to another customer.

**Risk:** moderate. Existing API consumers are unknown; search the repository and confirm no external clients before removing legacy routes.

## Phase 5 — Dynamic referral form correctness and validation

**Priority:** High.

**Findings:** submission assumes referral IDs are contiguous from 1 to the current count. Removing a middle block causes lookup failures or mismatched data. A department-change callback references the mutable global referral counter, so changing an earlier block can update the city dropdown of the most recently added block. The submit button is `type="button"`, so native form validation is not automatically triggered. Referral fields are not marked required even though the API requires several of them.

**Proposed work:**

- Treat each `.referido` DOM element as the source of truth; iterate actual elements rather than reconstructing IDs from 1 to count.
- Assign each block a stable unique client-side key and capture it in event listeners.
- Keep each referral's department/city dependency scoped to its own block.
- Use a single serialization function that reads fields within each block.
- Add explicit validation for each referral and show errors next to the relevant fields.
- Trigger form validation before sending; prevent duplicate submissions while a request is in progress.
- Preserve current options and field meanings through configuration and regression tests.
- Clarify whether the per-referral Save/Edit buttons are intended as local UI controls or should be removed in favor of normal form editing. They currently do not save to the server.

**Files likely affected:** `form.html`, `scripts/form.js`, `scripts/api.js`, `styles/styles.css`.

**Tests:** add three referrals; remove first/middle/last; edit values; change department in each block; submit after arbitrary removals; verify every referral remains associated with correct customer.

**Risk:** moderate. Existing HTML field names may be consumed by external scripts not present in the archive; preserve or map them during transition.

## Phase 6 — Search, detail, update, and deletion

**Priority:** High.

**Findings:** no GET `/clientes` route exists despite frontend fallback; search only supports exact document lookup; details are read-only; there are no PUT/PATCH endpoints. The details modal interpolates stored values into `innerHTML`, creating a stored-XSS risk.

**Proposed work:**

- Add a paginated list endpoint with safe filters and sorting.
- Add search by document and optionally customer name/form number after confirming expected workflow.
- Add a dedicated edit page or edit mode that loads an existing form and persists customer + referral changes transactionally.
- Define referral update semantics explicitly (update existing, add new, remove omitted IDs only after explicit confirmation).
- Keep delete confirmation and return clear conflict/not-found responses.
- Replace untrusted `innerHTML` interpolation with DOM creation and `textContent` (or a rigorously escaped template strategy).
- Show human-readable department/city names instead of raw IDs in detail views.

**Files likely affected:** `backend_api.py`, `scripts/api.js`, `scripts/formlist.js`, `formlist.html`, `form.html`, new edit template if needed.

**Tests:** list empty/populated; exact/partial search; update customer; add/edit/remove referrals; verify no unrelated referral changes; malicious HTML payload renders as text; delete with/without referrals.

**Risk:** high for update semantics. Agree on whether a form's identifier is immutable and whether changing document number is allowed.

## Phase 7 — Authentication, authorization, and privacy controls

**Priority:** Critical before network exposure; scope depends on single-user vs multi-user use.

**Findings:** no authentication or authorization protects pages or API routes; CORS is globally permissive; all users can read/delete records if they can reach the API.

**Proposed work:**

- Confirm intended deployment boundary. A strictly local single-user installation still needs network exposure minimized; multi-device/multi-user access requires authentication.
- Add login/session management or a suitable identity provider if multi-user.
- Protect all read/write endpoints, especially DELETE and update routes.
- Restrict CORS to known origins, or remove CORS if the browser UI and API are served from the same origin.
- Add CSRF protection for cookie-authenticated state-changing requests.
- Avoid logging customer PII; define retention, backup encryption, and access controls.
- Provide an explicit warning that the app is not safe to expose publicly until authentication and HTTPS are configured.

**Files likely affected:** backend app factory/config, API routes, frontend, Compose/reverse proxy, README.

**Tests:** unauthenticated requests denied; authorized role can perform allowed actions; unauthorized delete denied; CORS rejects untrusted origins; CSRF test where applicable.

## Phase 8 — Dashboard, UX, and accessibility

**Priority:** Medium.

**Findings:** home/welcome pages are static and duplicated; navigation labels/language are inconsistent; UI is not responsive enough for small screens; form and list states have limited feedback.

**Proposed work:**

- Replace duplicated welcome/home pages with one dashboard.
- Add useful summary counts only after the underlying list/query APIs exist.
- Standardize Spanish language, navigation, labels, validation, loading, empty, and error states.
- Improve responsive layout, keyboard navigation, label associations, and focus visibility.
- Keep the UI simple and fast; avoid adding a frontend framework unless requirements justify it.

**Files likely affected:** HTML templates, CSS, frontend scripts.

**Tests:** desktop/mobile viewport checks; keyboard-only flow; screen-reader label checks; empty/loading/error state checks.

## Phase 9 — Automated testing and maintainability

**Priority:** High, introduced incrementally from earlier phases.

**Proposed work:**

- Add pytest and Flask test-client tests for validation and API behavior.
- Use a disposable MySQL test service or a compatible test database strategy; do not test destructive migrations against the user's live database.
- Add JavaScript unit tests for referral serialization and DOM behavior where practical.
- Add CI for Python linting, tests, dependency/security checks, and Docker build.
- Pin and review dependencies. Remove unused packages only after confirming usage.
- Add structured logging and health/readiness endpoints.

**Files likely affected:** `requirements.txt`, test directory, CI workflow, app configuration.

**Tests:** CI green from a clean checkout; repeatable integration tests; no tests that rely on production credentials/data.

## Recommended implementation order

1. Phase 0 — baseline and data backup.
2. Phase 1 — rotate secrets and isolate business-specific configuration.
3. Phase 2 — persistent and reliable Docker lifecycle.
4. Phase 3 — migration baseline and database integrity.
5. Phase 4 — atomic form API.
6. Phase 5 — dynamic form correctness.
7. Phase 6 — search, update, and delete hardening.
8. Phase 7 — authentication and privacy controls before any non-local exposure.
9. Phase 8 — dashboard and UX.
10. Phase 9 — complete test/CI coverage across all phases.

## Remaining decisions / confirmations

- Confirm whether `tipo_documento` + normalized `numero_documento` is the intended uniqueness key (assumed from the one-form-per-document decision). No unique DB constraint has been added yet.
- Confirm whether form IDs may contain gaps. Recommended: database-generated unique increasing IDs; never reuse deleted IDs; gaps are acceptable.
- Confirm how the two currently UI-only fields (configured option selections) should be persisted. They are still not stored in the existing customer table and have not been silently discarded or added to the schema.
- Confirm the local database backup and successful restore before schema changes.
- Rotate credentials previously committed to public Git history. Source cleanup does not remove old commits; coordinate any history rewrite separately.
- Which fields shown in the current form must be persisted, especially the business-configurable selection fields?
- Should a referral be mandatory, or can a customer/form be saved with zero referrals?
- When editing a form, should removed referrals be physically deleted or marked inactive for audit/history?
- Should local configuration be a `.env` file, a separate ignored JSON/YAML file, or both?

## Explicit non-goals for the first implementation pass

- Replacing Flask with another backend framework.
- Replacing MySQL without a demonstrated need.
- Introducing React/Vue or another frontend framework by default.
- Renaming or deleting legacy database columns before a migration and data mapping are agreed.
- Exposing the app to the public internet before authentication, HTTPS, and backup/restore are addressed.
