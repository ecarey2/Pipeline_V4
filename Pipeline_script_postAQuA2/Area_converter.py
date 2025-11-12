import scipy.io
import numpy as np

from scipy.io import loadmat
import uiModule


#mat_data = uiModule.area_mat()
#print(mat_data.keys())

def compute_area_from_mat_region1(mat_path, pixel_size_microns=1.62):
    # Load .mat file
    mat_data = scipy.io.loadmat(mat_path[0])

    # Access bd0{1,1}{1,2} → Python: bd0[0, 0][0][1]
    bd0 = mat_data["bd0"]
    pixel_indices = bd0[0, 0][0][1]  # This should be a (N, 1) array

    # Compute area
    num_pixels = pixel_indices.shape[0]
    area_um2 = num_pixels * (pixel_size_microns ** 2)

    print(f"Number of pixels: {num_pixels}")
    print(f"Area: {area_um2:.2f} μm²")

    return num_pixels, area_um2

def compute_area_from_mat_region2(mat_path, pixel_size_microns=1.62):
    # Load .mat file
    mat_data = scipy.io.loadmat(mat_path[0])

    # Access bd0{1,1}{1,2} → Python: bd0[0, 0][0][1]
    bd0 = mat_data["bd0"]
    pixel_indices = bd0[0, 1][0][1]  # This should be a (N, 1) array

    # Compute area
    num_pixels = pixel_indices.shape[0]
    area_um2 = num_pixels * (pixel_size_microns ** 2)

    print(f"Number of pixels region2: {num_pixels}")
    print(f"Area region2: {area_um2:.2f} μm²")

    return num_pixels, area_um2

# work on this 6-6-2025
def compute_area_from_mat_region3(mat_path, pixel_size_microns=1.62):
        # Load .mat file
    mat_data = scipy.io.loadmat(mat_path[0])

    # Access bd0{1,1}{1,2} → Python: bd0[0, 0][0][1]
    bd0 = mat_data["bd0"]
    pixel_indices = bd0[0, 2][0][1]  # This should be a (N, 1) array

    # Compute area
    num_pixels = pixel_indices.shape[0]
    area_um3 = num_pixels * (pixel_size_microns ** 2)

    print(f"Number of pixels region3: {num_pixels}")
    print(f"Area region3: {area_um3:.2f} μm²")

    return num_pixels, area_um3

def compute_area_from_mat_region4(mat_path, pixel_size_microns=1.62):
    #this is if the region is region 5 to be used
    # Load .mat file
    mat_data = scipy.io.loadmat(mat_path[0])

    # Access bd0{1,1}{1,2} → Python: bd0[0, 0][0][1]
    bd0 = mat_data["bd0"]
    pixel_indices = bd0[0, 4][0][1]  # This should be a (N, 1) array

    # Compute area
    num_pixels = pixel_indices.shape[0]
    area_um4 = num_pixels * (pixel_size_microns ** 2)

    print(f"Number of pixels region4: {num_pixels}")
    print(f"Area region4: {area_um4:.2f} μm²")

    return num_pixels, area_um4


