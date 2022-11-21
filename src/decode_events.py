import rosbag
from event_array_py import Decoder

topic = '/event_camera/events'
bag = rosbag.Bag('evk1_events_run_3.bag')
output_file = 'evk1_events_run_3.csv'
decoder = Decoder()

number_of_events = 0
number_of_pos_events = 0
number_of_neg_events = 0
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
            number_of_events += 1
            if p > 0:
                number_of_pos_events += 1
            else:
                number_of_neg_events += 1

print("Number of events: " + str(number_of_events))
print("Number of pos events: " + str(number_of_pos_events))
print("Number of neg events: " + str(number_of_neg_events))
