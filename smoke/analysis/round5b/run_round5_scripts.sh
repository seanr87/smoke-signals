#!/usr/bin/env bash
# Reruns every round 5 script on the batch named in batch.json. Logs to rerun.log.
cd "$(dirname "$0")"
run() { ( cd "$1" && shift && for f in "$@"; do echo "== $PWD/$f"; python -I -X utf8 "$f" > "/tmp/r5b-$f.out" 2>&1 || { echo "FAILED $f"; tail -5 "/tmp/r5b-$f.out"; }; done ) }
run part-a a1.py a2.py a3.py a4.py merge.py
run part-c1 c1_caps.py c1_danger.py
run part-c4 c4_spots.py c4_wide.py
run part-c5 c5_sg.py c5_hs.py c5_lp.py c5_lp_daring.py c5_rest.py c5_merge.py c5_tables.py c5_figs.py
run part-d d1_scores.py d2_structure.py d3_profiles.py
run part-b ships.py figures.py show.py
run verify verify_main.py verify_bd.py verify_c5.py
echo DONE
