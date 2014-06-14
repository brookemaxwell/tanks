./bin/bzrflag --world=maps/empty.bzw --friendly-fire --max-shots=3 --default-tanks=10 --default-posnoise=3 --red-port=50100 --green-port=50101  --time-limit=240 --respawn-time=240 --default-true-positive=.97 --default-true-negative=.9 --occgrid-width=100 --no-report-obstacles $@ &
sleep 2 
python bzagents/combined_efforts/agent.py localhost 50100 &
python bzagents/combined_efforts/agent.py localhost 50101

sleep 10


