resultFolder="../raeResults/2021"
python3 test_scripts/generate_test_script_reactive_actor.py --domain fetch --actor RAE --runs 1 --resultFolder ${resultFolder}
python3 test_scripts/generate_test_script_actor_with_planner.py --domain fetch --actor RAE --planner UPOM --runs 1 --utility efficiency --heuristic None --resultFolder ${resultFolder}