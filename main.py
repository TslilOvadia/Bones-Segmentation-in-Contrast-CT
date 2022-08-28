# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage.measurements as scm

class ImageSegmentation:

    def __init__(self):
        self.img = None
        self.connectivity_cmps = []
        self.result_by_mins = []
        self.structure = np.array([[0,1,1],[1,1,1],[1,1,0]])


    def SegmentationByTH(self,nifty_file, Imin, Imax):
        """
        This function is given as inputs a grayscale NIFTI file (.nii.gz) and two integers – the minimal and maximal thresholds. The function generates a segmentation NIFTI file of the same dimensions, with a binary segmentation – 1 for voxels between Imin and Imax, 0 otherwise. This segmentation NIFTI file should be saved under the name <nifty_file>_seg_<Imin>_<Imax>.nii.gz.
        The function returns 1 if successful, 0 otherwise. Preferably, raise descriptive errors when returning 0.

        :param nifty_file:
        :param Imin:
        :param Imax:
        :return:
        """
        MAX_VOXEL_VALUE = 65535
        MIN_VOXEL_VALUE = 0
        img = nib.load(nifty_file)
        img_data = img.get_fdata().astype(dtype=np.uint16)
        img_data[(img_data <= Imax) & (img_data > Imin)] = MAX_VOXEL_VALUE
        img_data[img_data < MAX_VOXEL_VALUE] = MIN_VOXEL_VALUE
        final_image = nib.Nifti1Image(img_data, img.affine)
        nib.save(final_image, f"out_seg_{Imin}_{Imax}.nii.gz.")
        self.img = img_data
        return img_data


    def SkeletonTHFinder(self,nifty_file):
        """
        This function iterates over 25 candidate Imin thresholds in the range of [150,500] (with intervals of 14).
        In each run, use the SegmentationByTH function you’ve implemented, and count the number of connectivity components
        in the resulting segmentation with the current Imin. Plot your results – number of connectivity components per Imin. Choose the Imin which is the first or second minima in the plot. Also, make sure to include that graph in your report.

        Next, you need to perform post-processing (morphological operations – clean out single pixels, close holes, etc.)
        until you are left with a single connectivity component.
        Finally, this function should save a segmentation NIFTI file called “<nifty_file>_SkeletonSegmentation.nii.gz” and
        return the Imin used for that.
        :return:
        """
        Imin_range = np.arange(150,514,14)
        structure = np.ones((3,3,3))
        for i_min in Imin_range:
            self.SegmentationByTH(nifty_file, i_min, 1300)
            labels ,cmp = scm.label(self.img, structure)
            self.connectivity_cmps.append(cmp)

        plt.plot(self.connectivity_cmps)
        plt.title("Number of connectivity components vs. Imin value")
        plt.xlabel("Imin Value")
        plt.ylabel("Number of Connectivity Components")
        plt.show()





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    imseg = ImageSegmentation()
    # imseg.SegmentationByTH("resources/Case1_CT.nii.gz", 200, 1300)
    imseg.SkeletonTHFinder("resources/Case1_CT.nii.gz")