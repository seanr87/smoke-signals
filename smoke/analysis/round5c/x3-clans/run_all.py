# Round 5c x3: runs the whole chain and saves each script's printed output. python -I -X utf8 run_all.py
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [('d1_scores.py', 'd1_output.txt', {}), ('d2_structure.py', 'd2_output.txt', {}), ('d2_structure.py', 'd2_output_el.txt', {'X3_CLOCK': 'el'}),
         ('d3_profiles.py', 'd3_output.txt', {}), ('x3_findings.py', 'x3_findings_output.txt', {})]
for script, log, env in STEPS:
    e = dict(os.environ); e.pop('X3_CLOCK', None); e.update(env)
    r = subprocess.run([sys.executable, '-I', '-X', 'utf8', os.path.join(HERE, script)], capture_output=True, text=True, encoding='utf-8', env=e, cwd=HERE)
    open(os.path.join(HERE, log), 'w', encoding='utf-8', newline='\n').write(r.stdout + r.stderr)
    print(script, env or '', 'exit', r.returncode)
    if r.returncode: sys.exit(r.returncode)
