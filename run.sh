#./bin/bzrflag --world=maps/twoteams.bzw --friendly-fire --red-port=50100 --green-port=50101 $@ &
#./bin/bzrflag --world=maps/four_ls.bzw --friendly-fire --red-port=50100 --green-port=50101 --purple-port=50102 --blue-port=50103 $@ &
./bin/bzrflag --world=maps/four_ls.bzw --friendly-fire --default-true-positive=.97 --default-true-negative=.9 --occgrid-width=100 --no-report-obstacles --red-port=50100 --green-port=50101 --purple-port=50102 --blue-port=50103 $@ &
sleep 2 
#python bzagents/dumb_agent.py localhost 50100 &
#python bzagents/pf_agent.py localhost 50100 &
python bzagents/pf_agent_occ.py localhost 50101
#python ~cs470s/bzrflag/bots/compiled/blind.py agent0.pyc localhost 50101 #&
#python bots/compiled/blind.py agent1 localhost 50101 &
#python bots/compiled/blind.py agent1 localhost 50102 &
#python bots/compiled/blind.py agent1 localhost 50103 &

sleep 30


