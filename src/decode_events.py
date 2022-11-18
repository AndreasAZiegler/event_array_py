import rosbag
from event_array_py import Decoder

topic = '/event_camera/events'
bag = rosbag.Bag('evk1_events_run_4.bag')
output_file = 'evk1_events_run_4.csv'
decoder = Decoder()

for topic, msg, t in bag.read_messages(topics=topic):
    decoder.decode_bytes(msg.encoding, msg.width, msg.height,
	                     msg.time_base, msg.events)
    cd_events = decoder.get_cd_events()
    """
    print(cd_events)
    trig_events = decoder.get_ext_trig_events()
    print(trig_events)
    """

    with open(output_file, 'w') as csv_file:
        for event in cd_events:
            x, y, p = event[0], event[1], event[2]
            # Since the ball detection saves the timestamps in milli seconds
            # we do it here the same way
            t = msg.header.stamp.to_nsec() / (10**6)
            csv_file.write("%d,%d,%d,%d\n" % (x, y, p, t))
