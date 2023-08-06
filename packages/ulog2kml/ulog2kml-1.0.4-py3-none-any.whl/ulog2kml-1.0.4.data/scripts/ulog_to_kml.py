#!python
"""
Convert a ULog file into a time-aware KML file
"""

from __future__ import print_function

import argparse
from datetime import datetime, timedelta
import simplekml # pylint: disable=import-error

from ulog2kml.ulog import ULog

#pylint: disable=too-many-locals, invalid-name, consider-using-enumerate, too-many-arguments
#pylint: disable=unused-variable

MINIMUM_INTERVAL_SECS = 2


# TODO: print flight distance and time

def main():
    """Command line interface"""

    parser = argparse.ArgumentParser(description='Convert ULog to time-aware KML')
    parser.add_argument('filename', metavar='file.ulg', help='ULog input file')
    parser.add_argument('start_datetime', type=lambda s: datetime.strptime(s, '%Y-%m-%d_%H:%M'), help='Enter the start time like 2021-01-15_06:19')
    parser.add_argument('-o', '--output', dest='output_filename',
                        help="output filename", default='track.kml')

    args = parser.parse_args()
    ulog_filename = args.filename
    start_datetime = args.start_datetime
    kml_filename = args.output_filename

    _create_kml(ulog_filename, kml_filename, start_datetime)


def _create_kml(ulog_filename, kml_filename, start_datetime):
    
    ulog = ULog(ulog_filename)
    gps_data = next((x for x in ulog.data_list if x.name == 'vehicle_gps_position'), None)

    longitudes = gps_data.data['lon']
    latitudes = gps_data.data['lat']
    altitudes = gps_data.data['alt']
    timestamps = gps_data.data['timestamp']

    longitude_type = [f.type_str for f in gps_data.field_data if f.field_name == 'lon']
    if len(longitude_type) > 0 and longitude_type[0] == 'int32_t':
        longitudes = longitudes / 1e7 # to degrees
        latitudes = latitudes / 1e7
        altitudes = altitudes / 1e3 # to meters

    kml = simplekml.Kml()
    datetimes = list()
    coords = list()

    # these must be ascending...
    last_timestamp = 0
    for i in range(len(longitudes)):
        cur_timestamp = timestamps[i]

        if (cur_timestamp - last_timestamp)/1e6 > MINIMUM_INTERVAL_SECS: # assume timestamp is in [us]
            seconds_diff = (cur_timestamp - timestamps[0])/1e6
            cur_datetime = start_datetime + timedelta(seconds=seconds_diff)
            datetimes.append(_get_ge_datetime_string(cur_datetime))
            coords.append((longitudes[i], latitudes[i], altitudes[i]))
            last_timestamp = cur_timestamp

    # create the track
    track = kml.newgxtrack(name="Flight Track")
    track.altitudemode = simplekml.AltitudeMode.absolute
    track.newwhen(datetimes) 
    track.newgxcoord(coords)

    # style the track
    track.stylemap.normalstyle.iconstyle.icon.href = 'https://earth.google.com/images/kml-icons/track-directional/track-0.png'
    track.stylemap.normalstyle.iconstyle.icon.scale = 1.2
    track.stylemap.normalstyle.linestyle.color = '99ffac59'
    track.stylemap.normalstyle.linestyle.width = 6
    track.stylemap.highlightstyle.iconstyle.icon.href = 'https://earth.google.com/images/kml-icons/track-directional/track-0.png'
    track.stylemap.highlightstyle.iconstyle.icon.scale = 1.4
    track.stylemap.highlightstyle.linestyle.color = '99ffac59'
    track.stylemap.highlightstyle.linestyle.width = 8

    kml.save(kml_filename)      


def _get_ge_datetime_string(datetime_obj):
    return datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')


if __name__ == "__main__":
    main()
