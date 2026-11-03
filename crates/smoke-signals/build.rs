// Records the fork's commit so every output names the renderer revision. The
// variable is left unset when git is unavailable; the code reads it with
// `option_env!`.
fn main() {
    let rev = std::process::Command::new("git")
        .args(["rev-parse", "--short", "HEAD"])
        .output()
        .ok()
        .filter(|o| o.status.success())
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
        .filter(|s| !s.is_empty());
    if let Some(rev) = rev {
        println!("cargo:rustc-env=SMOKE_SIGNALS_GIT_REV={rev}");
    }
    println!("cargo:rerun-if-changed=../../.git/HEAD");
    println!("cargo:rerun-if-changed=../../.git/refs/heads");
}
