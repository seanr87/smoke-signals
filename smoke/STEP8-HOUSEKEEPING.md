# Housekeeping: main merged, round 6 archived and taken off the live site

Date: 17 Nov 2026. Nothing was deleted from git history; the local round 6 build stays at `smoke-site-r6/` (ignored).

## 1. Merge

- `main` was an ancestor of `full-field`, so the merge is a fast-forward: `main` now points at 04fff418, the same commit as `full-field` (84 commits of Smoke Signals work on top of the upstream main 9ab23880). Pushed to origin.
- `smoke/analysis/` (another session's work) was untracked before and after; it is in no commit.
- On main: `cargo test -p smoke-signals`: 26 tests pass (24 unit, determinism, the GF G1 H-SR golden test). `sanity.py` on the published batch `output/20261117-122135`: 341 runs, 0 failures, 1,547 smokes, ledger median 0.997, no run above 1.25; section 7 (enemies tables) clean; reference diff against the round 1 batch unchanged (8 of 217 rows, the torpedo-credit rows of STEP 7).
- Main builds the live site: the build from main has 6,679 files, 324 MB. Outside `r6/` it matches the live branch before this publish (ff524ff) file for file and byte for byte, except `smoke/about.html`, which carries the new round 6 line. The live site's `r6/` part was 1,190 files, 267 MB; the main build replaces it with the one redirect page.

## 2. Round 6 archived

- Tag `site-r6-archive` on gh-pages ff524ff (the last build holding `/r6/`), pushed. `git checkout site-r6-archive` in a gh-pages checkout republishes it any time.
- Tag `r6` on a25b039a (the "Round 6" source commit that built the r6 site; its data batch `output/20261104-180332` ran one commit earlier, at 30da0c1f), pushed.
- The site never linked to `/r6/` (hub, About and footers were checked); the About page now says: "Round 6 (H-SR, RESIN, PN only) is archived at git tag site-r6-archive."
- `/r6/index.html` is a one-line page that redirects to the hub and names the tag. Deep links under `/r6/` fall to `404.html`, which sends them under `smoke/`.
- `publish_site.py --keep-history` commits the build on top of the remote gh-pages instead of replacing the branch (no force push), so this removal is a normal commit and the tagged build stays in the branch's history.

## 3. Sizes and live check

| | Files | Size |
|---|---|---|
| gh-pages before (ff524ff, with `/r6/`) | 7,868 | 590 MB |
| gh-pages after | 6,679 | 324 MB |

Live (gh-pages 87ce26c, a normal commit on top of ff524ff, 13:16 EST): the hub, Smoke Signals home, clans, the H-SR clan page, games, maps, smokes, about, two smoke pages, smokes.json, two map path files, site.js, a root stub and 404.html all return 200 with the same byte size as the main build; the branch holds 6,679 files, 324 MB, the same as the build, none missing or differing. `/r6/` returns the 303-byte redirect page (meta refresh to the hub, naming the tag).

## 4. Conventions for future analyses

Added as section 14 of `smoke/DESIGN.md`: all analysis code stays in this repository, one folder or crate per analysis; each analysis publishes its site to its own GitHub Pages repository (under the 1 GB limit) and the hub links to them; replays, frames and batch outputs stay out of git, with data zips attached to GitHub releases from now on; published sites are tagged before anything is taken down.

## Commits

On `main` (and `full-field`, kept equal): 04fff418 (About line, `/r6/` redirect, publisher keep-history mode, conventions note), this report.
