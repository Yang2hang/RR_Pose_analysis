import h5py
import pandas as pd
import numpy as np

def h5_preprocessing(imput_h5):
    '''
    Convert HDF5 file into a CSV file, then dropNA.
    '''
    with h5py.File(imput_h5, 'r') as f:
        tracks_matrix = f["tracks"][:].transpose()
        nodes = [n.decode() for n in f["node_names"][:]]

    def coordinate(node_index, x_or_y):
        """Generate coordinate arrays for x or y based on node index."""
        coordinates = np.array([])
        for i in range(tracks_matrix.shape[0]):
            if x_or_y == "x":
                coordinates = np.append(coordinates, tracks_matrix[i, node_index, 0, 0])
            elif x_or_y == "y":
                coordinates = np.append(coordinates, tracks_matrix[i, node_index, 1, 0])
        return coordinates

    ihead = 0
    ineck = 1
    itorso = 2
    itailhead = 3

    head_x_coordinates = coordinate(ihead, "x")
    head_y_coordinates = coordinate(ihead, "y")
    neck_x_coordinates = coordinate(ineck, "x")
    neck_y_coordinates = coordinate(ineck, "y")
    torso_x_coordinates = coordinate(itorso, "x")
    torso_y_coordinates = coordinate(itorso, "y")
    tailhead_x_coordinates = coordinate(itailhead, "x")
    tailhead_y_coordinates = coordinate(itailhead, "y")

    df = pd.DataFrame(
        {
            "Head x": head_x_coordinates,
            "Head y": head_y_coordinates,
            "Neck x": neck_x_coordinates,
            "Neck y": neck_y_coordinates,
            "Torso x": torso_x_coordinates,
            "Torso y": torso_y_coordinates,
            "Tailhead x": tailhead_x_coordinates,
            "Tailhead y": tailhead_y_coordinates,
        }
    )

    # Clean the DataFrame by removing rows with missing data
    df_clean = df.dropna()
    
    return df_clean
