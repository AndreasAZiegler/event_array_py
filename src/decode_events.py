import rosbag
from event_array_py import Decoder

topic = '/event_camera/events'
bag = rosbag.Bag('evk1_events_run_4.bag')
output_file = 'evk1_events_run_4.csv'
decoder = Decoder()

with open(output_file, 'w') as csv_file:
    for topic, msg, t in bag.read_messages(topics=topic):
        decoder.decode_bytes(msg.encoding, msg.width, msg.height,
                             msg.time_base, msg.events)
        cd_events = decoder.get_cd_events()
        """
        print(cd_events)
        trig_events = decoder.get_ext_trig_events()
        print(trig_events)
        """

        for event in cd_events:
            x, y, p = event[0], event[1], event[2]
            # Since event cameras have us resolution, we save the timestamps in micro seconds
            # we do it here the same way
            t = float(msg.header.stamp.to_nsec() / (10**3))
            print("t: " + str(t) + ", x: " + str(x) + ", y: " + str(y) +
                  ", p: " + str(p))
            csv_file.write("%d,%d,%d,%f\n" % (x, y, p, t))
