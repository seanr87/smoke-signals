"""Publish the built site to GitHub Pages from a branch that holds only the site.

Usage:
  python -I smoke/tools/publish_site.py --site smoke-site --work <empty scratch folder>
         [--remote https://github.com/seanr87/smoke-signals.git] [--branch gh-pages]

Every publish replaces the branch with one fresh commit, so the branch never
grows a history of old builds and the code history stays on its own branches.
The site must already contain .nojekyll (build_site.py writes it).
"""
import argparse
import datetime
import os
import shutil
import subprocess
import sys


def run(args, cwd):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"{' '.join(args)}\n{r.stdout}{r.stderr}")
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="smoke-site")
    ap.add_argument("--work", required=True, help="scratch folder for the throwaway repository; created if missing, emptied first")
    ap.add_argument("--remote", default="https://github.com/seanr87/smoke-signals.git")
    ap.add_argument("--branch", default="gh-pages")
    ap.add_argument("--label", default="")
    args = ap.parse_args()
    site = os.path.abspath(args.site)
    if not os.path.exists(os.path.join(site, "index.html")):
        sys.exit(f"no index.html in {site}; build the site first")
    work = os.path.abspath(args.work)
    if os.path.exists(work):
        shutil.rmtree(work)
    shutil.copytree(site, work)
    open(os.path.join(work, ".nojekyll"), "a").close()
    name = run(["git", "config", "user.name"], cwd=os.getcwd()) or "Smoke Signals"
    email = run(["git", "config", "user.email"], cwd=os.getcwd()) or "smoke-signals@localhost"
    run(["git", "init", "-q", "-b", args.branch], cwd=work)
    run(["git", "config", "user.name", name], cwd=work)
    run(["git", "config", "user.email", email], cwd=work)
    run(["git", "add", "-A"], cwd=work)
    stamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    msg = f"Site build {stamp}" + (f": {args.label}" if args.label else "")
    run(["git", "commit", "-q", "-m", msg], cwd=work)
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(site) for f in fs)
    print(f"pushing {total / 1e6:.0f} MB to {args.remote} {args.branch} (one commit, replacing the branch)")
    run(["git", "push", "-q", "--force", args.remote, f"HEAD:refs/heads/{args.branch}"], cwd=work)
    print("pushed:", msg)


if __name__ == "__main__":
    main()
