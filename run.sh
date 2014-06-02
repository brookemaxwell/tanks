./bin/bzrflag --world=maps/empty_world.bzw --friendly-fire  --red-tanks=1   --green-tanks=1 --default-posnoise=5 --red-port=50100 --green-port=50101  $@ &
sleep 2 
#python bzagents/dumb_agent.py localhost 50100 &
python bzagents/kalman/wild_pigeon.py localhost 50101 &
python bzagents/kalman/targeting_agent.py localhost 50100

sleep 30


