from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic_xml import BaseXmlModel, attr, element
from typing_extensions import TypedDict

from pydantic import ConfigDict, HttpUrl, NonNegativeInt, confloat


NSMAP = {
    "": "http://www.topografix.com/GPX/1/1",
    "gpxx": "http://www.garmin.com/xmlschemas/GpxExtensions/v3",
    "gpxtpx": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class FixEnum(str, Enum):
    _none = "none"
    _2d = "2d"
    _3d = "3d"
    _dgps = "dgps"
    _pps = "pps"


class Link(BaseXmlModel, nsmap=NSMAP):
    href: HttpUrl = attr()
    text: Optional[str] = element(default=None)
    type: Optional[str] = element(default=None)


class Author(BaseXmlModel, nsmap=NSMAP):
    name: Optional[str] = element(default=None)
    email: Optional[dict[str, str]] = element(default=None)
    link: Optional[Link] = element(default=None)


class Copyright(BaseXmlModel, nsmap=NSMAP):
    author: str = attr()
    year: Optional[str] = element(default=None)
    license: Optional[HttpUrl] = element(default=None)


class Bounds(BaseXmlModel, nsmap=NSMAP):
    minlat: float = attr()
    minlon: float = attr()
    maxlat: float = attr()
    maxlon: float = attr()


class Point(BaseXmlModel, nsmap=NSMAP):
    lat: confloat(ge=-90, le=90) = attr()
    lon: confloat(ge=-180, le=180) = attr()
    ele: Optional[float] = element(default=None)
    time: Optional[datetime] = element(default=None)
    geoidheight: Optional[float] = element(default=None)
    name: Optional[str] = element(default=None)
    comment: Optional[str] = element(tag="cmt", default=None)
    description: Optional[str] = element(tag="desc", default=None)
    source: Optional[str] = element(tag="src", default=None)
    link: Optional[Link] = element(default=None)
    sym: Optional[str] = element(default=None)
    type: Optional[str] = element(default=None)
    fix: Optional[FixEnum] = element(default=None)
    sat: Optional[NonNegativeInt] = element(default=None)
    hdop: Optional[float] = element(default=None)
    vdop: Optional[float] = element(default=None)
    pdop: Optional[float] = element(default=None)
    ageofdgpsdata: Optional[float] = element(default=None)


class TrackSegment(BaseXmlModel, nsmap=NSMAP):
    coordinates: Optional[list[Point]] = element("trkpt", default=None)


class Track(BaseXmlModel, nsmap=NSMAP):
    name: Optional[str] = element(default=None)
    comment: Optional[str] = element(tag="cmt", default=None)
    description: Optional[str] = element(tag="desc", default=None)
    source: Optional[str] = element(tag="src", default=None)
    link: Optional[Link] = element(default=None)
    number: Optional[NonNegativeInt] = element(default=None)
    type: Optional[str] = element(default=None)
    segments: Optional[list[TrackSegment]] = element(
        tag="trkseg",
        default=None,
    )


class Route(BaseXmlModel, nsmap=NSMAP):
    name: Optional[str] = element(default=None)
    comment: Optional[str] = element(tag="cmt", default=None)
    description: Optional[str] = element(tag="desc", default=None)
    source: Optional[str] = element(tag="src", default=None)
    link: Optional[Link] = element(default=None)
    number: Optional[NonNegativeInt] = element(default=None)
    type: Optional[str] = element(default=None)
    coordinates: Optional[list[Point]] = element("rtept", default=None)


class Attributes(TypedDict):
    version: str
    creator: str


class Metadata(BaseXmlModel, nsmap=NSMAP):
    name: Optional[str] = element(default=None)
    description: Optional[str] = element(tag="desc", default=None)
    author: Optional[Author] = element(default=None)
    copyright: Optional[Copyright] = element(default=None)
    link: Optional[Link] = element(default=None)
    time: Optional[datetime] = element(default=None)
    keywords: Optional[str] = element(default=None)
    bounds: Optional[Bounds] = element(default=None)


class GPX(BaseXmlModel, tag="gpx", nsmap=NSMAP):
    model_config = ConfigDict(extra="ignore", strict=False)

    attrs: Attributes

    metadata: Optional[Metadata] = element("metadata", default=None)
    waypoints: Optional[list[Point]] = element("wpt", default=None)
    routes: Optional[list[Route]] = element("rte", default=None)
    tracks: Optional[list[Track]] = element("trk", default=None)
