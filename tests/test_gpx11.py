# SPDX-FileCopyrightText: 2024-present Florian Demmer <fdemmer@gmail.com>
#
# SPDX-License-Identifier: MIT
import time

from contextlib import ContextDecorator
from datetime import datetime

import gpxpy
import pytz

from pydantic_core import Url
from pydantic_xml.errors import ParsingError

from pydantic_gpx.gpx11 import GPX, FixEnum, Metadata, Point, Route


class Timer(ContextDecorator):
    def __enter__(self):
        self.start = time.monotonic_ns()
        return self

    def __exit__(self, *args):
        self.end = time.monotonic_ns()

    def __str__(self):
        return f"{self.elapsed_ms / 1000:.4f}"

    @property
    def elapsed(self):
        try:
            return self.end - self.start
        except AttributeError as exc:
            raise NotImplementedError("Interval only available after exit!") from exc

    @property
    def elapsed_ms(self):
        return self.elapsed // 1_000_000


def test_gpxpy_examples(gpxpy_examples):
    for file in gpxpy_examples:
        # breakpoint()
        try:
            GPX.from_xml(file.read_bytes())
            print(f"parsed: {file}")
        except ParsingError:
            pass
            # print(f"error: {file}")


def test_benchmark(gpx11_large):
    with Timer() as t:
        for _ in range(10):
            gpx2 = gpxpy.parse(gpx11_large)
    print("gpxpy:", t)
    with Timer() as t:
        for _ in range(10):
            gpx1 = GPX.from_xml(gpx11_large)
    print("pydantic", t)


def test_attrs_dict(gpx11):
    assert isinstance(gpx11.attrs, dict)
    assert set(gpx11.attrs.keys()) == {"creator", "version"}
    assert gpx11.attrs["creator"] == "..."
    assert gpx11.attrs["version"] == "1.1"


def test_metadata(gpx11):
    assert isinstance(gpx11.metadata, Metadata)
    assert set(gpx11.metadata.model_dump().keys()) == {
        "author",
        "bounds",
        "copyright",
        "description",
        "extensions",
        "keywords",
        "link",
        "name",
        "time",
    }
    metadata = gpx11.metadata
    assert metadata.name == "example name"
    assert metadata.description == "example description"
    assert metadata.author.name == "author name"
    assert metadata.author.email.id == "aaa"
    assert metadata.author.email.domain == "bbb.com"
    assert str(metadata.author.email) == "aaa@bbb.com"
    # TODO fix pydantic append slash
    assert metadata.author.link.href == Url("http://link/")
    assert metadata.author.link.text == "link text"
    assert metadata.author.link.type == "link type"
    assert metadata.copyright.author == "gpxauth"
    assert metadata.copyright.year == "2013"
    assert metadata.copyright.license == "lic"
    assert metadata.link.href == Url("http://link2/")
    assert metadata.link.text == "link text2"
    assert metadata.link.type == "link type2"
    assert metadata.time == datetime(2013, 1, 1, 12, 0, 0)
    assert metadata.keywords == "example keywords"
    assert metadata.bounds.minlat == 1.2
    assert metadata.bounds.minlon == 3.4
    assert metadata.bounds.maxlat == 5.6
    assert metadata.bounds.maxlon == 7.8
    # TODO extensions don't work yet
    assert metadata.extensions == [{}]


def test_waypoints(gpx11):
    assert isinstance(gpx11.waypoints, list)
    assert len(gpx11.waypoints) == 2
    waypoint = gpx11.waypoints[0]
    assert isinstance(waypoint, Point)
    assert set(waypoint.model_dump().keys()) == {
        "ageofdgpsdata",
        "comment",
        "description",
        "dgpsid",
        "elevation",
        "extensions",
        "fix",
        "geoidheight",
        "hdop",
        "latitude",
        "link",
        "longitude",
        "magvar",
        "name",
        "pdop",
        "sat",
        "source",
        "symbol",
        "time",
        "type",
        "vdop",
    }
    assert waypoint.latitude == 12.3
    assert waypoint.longitude == 45.6
    assert waypoint.elevation == 75.1
    assert waypoint.time == datetime(2013, 1, 2, 2, 3, 0, tzinfo=pytz.utc)
    assert waypoint.magvar == 1.1
    assert waypoint.geoidheight == 2.0
    assert waypoint.name == "example name"
    assert waypoint.comment == "example cmt"
    assert waypoint.description == "example desc"
    assert waypoint.source == "example src"
    assert waypoint.link.href == Url("http://link3/")
    assert waypoint.link.text == "link text3"
    assert waypoint.link.type == "link type3"
    assert waypoint.symbol == "example sym"
    assert waypoint.type == "example type"
    assert waypoint.fix == FixEnum._2d
    assert waypoint.fix == "2d"
    assert waypoint.sat == 5
    assert waypoint.hdop == 6
    assert waypoint.vdop == 7
    assert waypoint.pdop == 8
    assert waypoint.ageofdgpsdata == 9
    assert waypoint.dgpsid == 45
    # TODO extensions don't work yet


def test_routes(gpx11):
    assert isinstance(gpx11.routes, list)
    assert len(gpx11.routes) == 2
    route = gpx11.routes[0]
    assert isinstance(route, Route)
    assert set(route.model_dump().keys()) == {
        "comment",
        "description",
        "extensions",
        "link",
        "name",
        "number",
        "points",
        "source",
        "type",
    }
    assert route.name == "example name"
    assert route.comment == "example cmt"
    assert route.description == "example desc"
    assert route.source == "example src"
    assert route.link.href == Url("http://link3/")
    assert route.link.text == "link text3"
    assert route.link.type == "link type3"
    assert route.number == 7
    assert route.type == "rte type"
    assert len(route.points) == 3
    point = route.points[0]
    assert isinstance(point, Point)
    assert set(point.model_dump().keys()) == {
        "ageofdgpsdata",
        "comment",
        "description",
        "dgpsid",
        "elevation",
        "extensions",
        "fix",
        "geoidheight",
        "hdop",
        "latitude",
        "link",
        "longitude",
        "magvar",
        "name",
        "pdop",
        "sat",
        "source",
        "symbol",
        "time",
        "type",
        "vdop",
    }
    assert point.latitude == 10
    assert point.longitude == 20
    assert point.elevation == 75.1
    assert point.time == datetime(2013, 1, 2, 2, 3, 3, tzinfo=pytz.utc)
    assert point.magvar == 1.2
    assert point.geoidheight == 2.1
    assert point.name == "example name r"
    assert point.comment == "example cmt r"
    assert point.description == "example desc r"
    assert point.source == "example src r"
    assert point.link.href == Url("http://linkrtept/")
    assert point.link.text == "rtept link"
    assert point.link.type == "rtept link type"
    assert point.symbol == "example sym r"
    assert point.type == "example type r"
    assert point.fix == FixEnum._3d
    assert point.fix == "3d"
    assert point.sat == 6
    assert point.hdop == 7
    assert point.vdop == 8
    assert point.pdop == 9
    assert point.ageofdgpsdata == 10
    assert point.dgpsid == 99
    # TODO extensions don't work yet
    assert point.extensions == [{}]
