'''
The code in this module is basically a copy of
http://docs.astropy.org/en/stable/_modules/astropy/coordinates/builtin_frames/skyoffset.html

We are just not creating a metaclass and a factory but directly building the
corresponding class.
'''
import astropy.units as u
from astropy.coordinates.matrix_utilities import (
    rotation_matrix,
    matrix_product,
    matrix_transpose,
)
from astropy.coordinates import (
    frame_transform_graph,
    FunctionTransform,
    DynamicMatrixTransform,
    UnitSphericalRepresentation,
    BaseCoordinateFrame,
    CoordinateAttribute,
    TimeAttribute,
    EarthLocationAttribute,
    RepresentationMapping,
    QuantityAttribute,
)

from .horizon_frame import HorizonFrame


class NominalFrame(BaseCoordinateFrame):
    '''
    Nominal coordinate frame.

    A Frame using a UnitSphericalRepresentation.
    This is basically the same as a HorizonCoordinate, but the
    origin is at an arbitray position in the sky.
    This is what astropy calls a SkyOffsetCoordinate

    If the telescopes are in divergent pointing, this Frame can be
    used to transform to a common system.

    Attributes
    ----------

    origin: SkyCoord[HorizonFrame]
        Origin of this frame as a HorizonCoordinate
    obstime: Tiem
        Observation time
    location: EarthLocation
        Location of the telescope
    rotation: Angle
        rotation of the frame, 0 means x along azimuth, y along altitude
    '''
    frame_specific_representation_info = {
        UnitSphericalRepresentation: [
            RepresentationMapping('lon', 'x'),
            RepresentationMapping('lat', 'y'),
        ]
    }
    default_representation = UnitSphericalRepresentation

    origin = CoordinateAttribute(default=None, frame=HorizonFrame)
    rotation = QuantityAttribute(0, unit=u.deg)

    obstime = TimeAttribute(default=None)
    location = EarthLocationAttribute(default=None)


@frame_transform_graph.transform(FunctionTransform, NominalFrame, NominalFrame)
def skyoffset_to_skyoffset(from_telescope_coord, to_telescope_frame):
    """Transform between two skyoffset frames."""

    intermediate_from = from_telescope_coord.transform_to(
        from_telescope_coord.origin
    )
    intermediate_to = intermediate_from.transform_to(
        to_telescope_frame.origin
    )
    return intermediate_to.transform_to(to_telescope_frame)


@frame_transform_graph.transform(DynamicMatrixTransform, HorizonFrame, NominalFrame)
def reference_to_skyoffset(reference_frame, telescope_frame):
    """Convert a reference coordinate to an sky offset frame."""

    # Define rotation matrices along the position angle vector, and
    # relative to the origin.
    origin = telescope_frame.origin.spherical
    mat1 = rotation_matrix(-telescope_frame.rotation, 'x')
    mat2 = rotation_matrix(-origin.lat, 'y')
    mat3 = rotation_matrix(origin.lon, 'z')
    return matrix_product(mat1, mat2, mat3)


@frame_transform_graph.transform(DynamicMatrixTransform, NominalFrame, HorizonFrame)
def skyoffset_to_reference(skyoffset_coord, reference_frame):
    """Convert an sky offset frame coordinate to the reference frame"""

    # use the forward transform, but just invert it
    R = reference_to_skyoffset(reference_frame, skyoffset_coord)
    # transpose is the inverse because R is a rotation matrix
    return matrix_transpose(R)