#./bin/bzrflag --world=maps/twoteams.bzw --friendly-fire --red-port=50100 --green-port=50101 $@ &
#./bin/bzrflag --world=maps/four_ls.bzw --friendly-fire --red-port=50100 --green-port=50101 --purple-port=50102 --blue-port=50103 $@ &
./bin/bzrflag --world=maps/empty_world.bzw --friendly-fire  --red-tanks=1   --green-tanks=1 --default-posnoise=5 --red-port=50100 --green-port=50101  $@ &
sleep 2 
#python bzagents/dumb_agent.py localhost 50100 &
#python bzagents/pf_agent.py localhost 50100 &
python bzagents/kalman/targeting_agent.py localhost 50100 &
python bzagents/kalman/pigeon.py localhost 50101

#python bots/compiled/blind.py agent1 localhost 50101 &
#python bots/compiled/blind.py agent1 localhost 50102 &
#python bots/compiled/blind.py agent1 localhost 50103 &

sleep 30


