"""
Gplates module for use with the gplates library.
"""
import pygplates


def getPresentDayPoint(feature_file, rotation_file, latitude,
                       longitude, reconstruction_time):
    """Function takes a valid latitude and longitude from a specified time in
    the past, and returns the present day latitude and longitude of that
    point.

    Parameters
    ----------
    feature_file : FeatureCollection
        pyGplates feature collection needed to track point.
    rotation_file : FeatureCollection
        pyGplates feature collection needed to track point.
    latitude : float
        past latitude.
    longitude : float
        past longitude.
    reconstruction_time : int
        past time in Ma.

    Returns
    -------
    tuple :
        lat and long labelled tuple
    """
    features = pygplates.FeatureCollection.read(feature_file)
    rotation_model = pygplates.FeatureCollection.read(rotation_file)
    point = pygplates.PointOnSphere(latitude, longitude)
    # Reconstruct the features to specified time.
    reconstructed_features = []
    pygplates.reconstruct(features, rotation_model, reconstructed_features,
                          reconstruction_time, group_with_feature=True,
                          anchor_plate_id=0)
    # The minimum distance to all features and the nearest feature.
    min_distance_to_all_features = None
    nearest_feature = None
    # Iterate over all reconstructed features.
    for feature, feature_reconstructed_geometries in reconstructed_features:
        # Iterate over all reconstructed geometries of the current feature.
        for feature_reconstructed_geometry in feature_reconstructed_geometries:
            # Get the minimum distance from point to the current
            # reconstructed geometry.
            min_dist_to_feature = pygplates.GeometryOnSphere.distance(point,
                feature_reconstructed_geometry.get_reconstructed_geometry(),  # noqa
                min_distance_to_all_features,  # noqa: E128
                geometry2_is_solid=True)  # noqa: E128
        # If the current geometry is nearer than all previous geometries then
        # its associated feature is the nearest feature so far.
        if min_dist_to_feature is not None:
            min_dist_to_all_features = min_dist_to_feature
            nearest_feature = feature

    if min_dist_to_all_features != 0:
        raise ValueError("Latitude and Longitude must be within a valid "
                         "feature at reconstruction time")
    else:
        reconstruction_plate_id = nearest_feature.get_reconstruction_plate_id()
        # Create the feature to track
        tracked_point = pygplates.Feature.create_reconstructable_feature(
            pygplates.FeatureType.gpml_unclassified_feature,
            point,
            name="Tracked Point",
            reconstruction_plate_id=reconstruction_plate_id)
        pygplates.reverse_reconstruct(tracked_point,
                                      rotation_model,
                                      reconstruction_time)
        geometry = tracked_point.get_geometry(lambda property: True,
                                              pygplates.PropertyReturn.all)

        return geometry[0].to_lat_lon_point()
