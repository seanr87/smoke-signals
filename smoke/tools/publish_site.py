"""Publish the built site to GitHub Pages from a branch that holds only the site.

Usage:
  python -I smoke/tools/publish_site.py --site smoke-site --work <empty scratch folder>
         [--remote https://github.com/seanr87/smoke-signals.git] [--branch gh-pages]

By default every publish replaces the branch with one fresh commit, so the
branch never grows a history of old builds. With --keep-history the build is
committed on top of the branch as it is on the remote (a normal commit, no
force push), so earlier builds stay reachable.
The site must already contain .nojekyll (build_site.py writes it).
"""
import argparse
import datetime
import os
import shutil
import stat
import subprocess
import sys


def run(args, cwd):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"{' '.join(args)}\n{r.stdout}{r.stderr}")
    return r.stdout.strip()


def clear_read_only(func, path, _exc):
    """Git marks its object files read-only, which blocks their removal on Windows."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="smoke-site")
    ap.add_argument("--work", required=True, help="short scratch path for the throwaway repository (Windows limits paths to 260 characters); created if missing, emptied first")
    ap.add_argument("--remote", default="https://github.com/seanr87/smoke-signals.git")
    ap.add_argument("--branch", default="gh-pages")
    ap.add_argument("--label", default="")
    ap.add_argument("--keep-history", action="store_true", help="commit on top of the remote branch instead of replacing it")
    args = ap.parse_args()
    site = os.path.abspath(args.site)
    if not os.path.exists(os.path.join(site, "index.html")):
        sys.exit(f"no index.html in {site}; build the site first")
    work = os.path.abspath(args.work)
    if os.path.exists(work):
        shutil.rmtree(work, onexc=clear_read_only)
    name = run(["git", "config", "user.name"], cwd=os.getcwd()) or "Smoke Signals"
    email = run(["git", "config", "user.email"], cwd=os.getcwd()) or "smoke-signals@localhost"
    if args.keep_history:
        os.makedirs(work)
        run(["git", "init", "-q", "-b", args.branch], cwd=work)
        run(["git", "config", "core.longpaths", "true"], cwd=work)
        run(["git", "fetch", "-q", "--depth", "1", args.remote, args.branch], cwd=work)
        run(["git", "reset", "-q", "--hard", "FETCH_HEAD"], cwd=work)
        for entry in os.listdir(work):
            if entry == ".git":
                continue
            path = os.path.join(work, entry)
            if os.path.isdir(path):
                shutil.rmtree(path, onexc=clear_read_only)
            else:
                os.remove(path)
        shutil.copytree(site, work, dirs_exist_ok=True)
    else:
        shutil.copytree(site, work)
        run(["git", "init", "-q", "-b", args.branch], cwd=work)
        run(["git", "config", "core.longpaths", "true"], cwd=work)
    open(os.path.join(work, ".nojekyll"), "a").close()
    run(["git", "config", "user.name", name], cwd=work)
    run(["git", "config", "user.email", email], cwd=work)
    run(["git", "add", "-A"], cwd=work)
    stamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    msg = f"Site build {stamp}" + (f": {args.label}" if args.label else "")
    run(["git", "commit", "-q", "-m", msg], cwd=work)
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(site) for f in fs)
    if args.keep_history:
        print(f"pushing {total / 1e6:.0f} MB to {args.remote} {args.branch} (a commit on top of the branch)")
        run(["git", "push", "-q", args.remote, f"HEAD:refs/heads/{args.branch}"], cwd=work)
    else:
        print(f"pushing {total / 1e6:.0f} MB to {args.remote} {args.branch} (one commit, replacing the branch)")
        run(["git", "push", "-q", "--force", args.remote, f"HEAD:refs/heads/{args.branch}"], cwd=work)
    print("pushed:", msg)


if __name__ == "__main__":
    main()
