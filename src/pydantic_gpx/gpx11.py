from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic_xml import BaseXmlModel, attr, element
from typing_extensions import TypedDict

from pydantic import ConfigDict, HttpUrl, NonNegativeInt, confloat, conint


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


class Email(BaseXmlModel, nsmap=NSMAP):
    id: str = attr()
    domain: str = attr()

    def __str__(self) -> str:
        return f"{self.id}@{self.domain}"


class Author(BaseXmlModel, nsmap=NSMAP):
    name: Optional[str] = element(default=None)
    email: Optional[Email] = element(default=None)
    link: Optional[Link] = element(default=None)


# TODO find example to test
class Copyright(BaseXmlModel, nsmap=NSMAP):
    author: str = attr()
    year: Optional[str] = element(default=None)
    # TODO actually validate xsd:anyURI
    license: Optional[str] = element(default=None)


class Bounds(BaseXmlModel, nsmap=NSMAP):
    minlat: float = attr()
    minlon: float = attr()
    maxlat: float = attr()
    maxlon: float = attr()


class Point(BaseXmlModel, nsmap=NSMAP):
    latitude: confloat(ge=-90, le=90) = attr("lat")
    longitude: confloat(ge=-180, le=180) = attr("lon")
    elevation: Optional[float] = element(tag="ele", default=None)
    time: Optional[datetime] = element(default=None)
    magvar: Optional[confloat(ge=0, le=360)] = element(default=None)
    geoidheight: Optional[float] = element(default=None)
    name: Optional[str] = element(default=None)
    comment: Optional[str] = element(tag="cmt", default=None)
    description: Optional[str] = element(tag="desc", default=None)
    source: Optional[str] = element(tag="src", default=None)
    link: Optional[Link] = element(default=None)
    symbol: Optional[str] = element(tag="sym", default=None)
    type: Optional[str] = element(default=None)
    fix: Optional[FixEnum] = element(default=None)
    sat: Optional[NonNegativeInt] = element(default=None)
    hdop: Optional[float] = element(default=None)
    vdop: Optional[float] = element(default=None)
    pdop: Optional[float] = element(default=None)
    ageofdgpsdata: Optional[float] = element(default=None)
    dgpsid: Optional[conint(ge=0, le=1023)] = element(default=None)
    # TODO how to make this work? namespace?
    extensions: Optional[list[dict[str, str]]] = element(default=None)


class TrackSegment(BaseXmlModel, nsmap=NSMAP):
    points: Optional[list[Point]] = element("trkpt", default=None)
    # TODO how to make this work? namespace?
    extensions: Optional[list[dict[str, str]]] = element(default=None)

    # @field_serializer('points')
    # def encode_coordinates(self, value: list[Point]) -> list[CoordinateTuple]:
    #     return [
    #         (d['lon'], d['lat'], d.get('ele'))
    #         if d.get('ele') else (d['lon'], d['lat'])
    #         for d in [v.dict() for v in value]
    #     ]


class RouteTrackMixin:
    name: Optional[str] = element(default=None)
    comment: Optional[str] = element(tag="cmt", default=None)
    description: Optional[str] = element(tag="desc", default=None)
    source: Optional[str] = element(tag="src", default=None)
    link: Optional[Link] = element(default=None)
    number: Optional[NonNegativeInt] = element(default=None)  # TODO find example to test
    type: Optional[str] = element(default=None)
    extensions: Optional[list[dict[str, str]]] = element(
        default=None,
    )  # TODO how to make this work? namespace?


class Track(RouteTrackMixin, BaseXmlModel, nsmap=NSMAP):
    segments: Optional[list[TrackSegment]] = element(tag="trkseg", default=None)
    # TODO not sure i _want_ segment optional even tough the spec defines it as such
    # TODO also, i cannot really save more than one segment :(

    # @field_serializer('segments')
    # def encode_segment(self, value: list[TrackSegment]) -> list[list[CoordinateTuple]]:
    #     return [
    #         d['points']
    #         for d in [v.dict() for v in value]
    #     ]


class Route(RouteTrackMixin, BaseXmlModel, nsmap=NSMAP):
    points: Optional[list[Point]] = element("rtept", default=None)

    # @field_serializer('points')
    # def coordinates_tuples(self, value: list[Point]) -> list[CoordinateTuple]:
    # def coordinates_tuples(self) -> list[CoordinateTuple]:
    #     return [
    #         (d['lon'], d['lat'], d.get('ele'))
    #         if d.get('ele') else (d['lon'], d['lat'])
    #         for d in [v.dict() for v in self.points]
    #     ]


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
    # TODO how to make this work? namespace?
    extensions: Optional[list[dict[str, str]]] = element(default=None)


class GPX(BaseXmlModel, tag="gpx", nsmap=NSMAP):
    model_config = ConfigDict(extra="ignore", strict=False)

    # three variations of getting the attribs on gpx element into fields
    attrs: Attributes
    # properties: Dict[str, str]
    # version: str = attr()
    # creator: str = attr()

    metadata: Optional[Metadata] = element("metadata", default=None)
    waypoints: Optional[list[Point]] = element("wpt", default=None)
    routes: Optional[list[Route]] = element("rte", default=None)
    tracks: Optional[list[Track]] = element("trk", default=None)
