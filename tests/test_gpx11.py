# SPDX-FileCopyrightText: 2024-present Florian Demmer <fdemmer@gmail.com>
#
# SPDX-License-Identifier: MIT

from datetime import datetime

import pytz

from pydantic_gpx.gpx11 import Metadata, Point


def test_attrs_dict(gpx11):
    assert isinstance(gpx11.attrs, dict)
    assert set(gpx11.attrs.keys()) == {"creator", "version"}
    assert gpx11.attrs["creator"] == "Wikipedia"
    assert gpx11.attrs["version"] == "1.1"


def test_metadata(gpx11):
    assert isinstance(gpx11.metadata, Metadata)
    assert set(gpx11.metadata.model_dump().keys()) == {
        "link",
        "description",
        "keywords",
        "copyright",
        "time",
        "name",
        "author",
        "bounds",
    }
    metadata = gpx11.metadata
    assert metadata.name == "Data name"
    assert (
        metadata.description == "Valid GPX example without special characters"
    )
    assert metadata.author.name == "Author name"
    assert metadata.author.email is None
    assert metadata.author.link is None
    assert metadata.copyright is None
    assert metadata.link is None
    assert metadata.time is None
    assert metadata.keywords is None
    assert metadata.bounds is None


def test_waypoints(gpx11):
    assert isinstance(gpx11.waypoints, list)
    assert len(gpx11.waypoints) == 3
    waypoint = gpx11.waypoints[0]
    assert isinstance(waypoint, Point)
    assert set(waypoint.model_dump().keys()) == {
        "ele",
        "sym",
        "lon",
        "source",
        "type",
        "fix",
        "name",
        "comment",
        "link",
        "hdop",
        "lat",
        "sat",
        "vdop",
        "pdop",
        "ageofdgpsdata",
        "geoidheight",
        "description",
        "time",
    }
    assert waypoint.lat == 52.518611
    assert waypoint.lon == 13.376111
    assert waypoint.ele == 35.0
    assert waypoint.time == datetime(2011, 12, 31, 23, 59, 59, tzinfo=pytz.utc)
    assert waypoint.geoidheight is None
    assert waypoint.name == "Reichstag (Berlin)"
    assert waypoint.comment is None
    assert waypoint.description is None
    assert waypoint.source is None
    assert waypoint.link is None
    assert waypoint.sym == "City"
    assert waypoint.type is None
    assert waypoint.fix is None
    assert waypoint.sat is None
    assert waypoint.hdop is None
    assert waypoint.vdop is None
    assert waypoint.pdop is None
    assert waypoint.ageofdgpsdata is None
