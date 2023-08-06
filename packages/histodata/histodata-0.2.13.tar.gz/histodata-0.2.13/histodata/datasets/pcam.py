from typing import Callable
from typing import Optional as O
from typing import Sequence
from typing import Union as U

from h5py import File
from torch.utils.data import Dataset
from torchvision.transforms import Compose

# TODO change to HistoDataset API


def pcam_patches(
    root: str, # '/data/ldap/histopathologic/original_read_only/PCAM_extracted'
    transformation: O[U[Callable, Sequence[Callable]]] = None,
    #   pre_transformation: O[U[Callable, Sequence[Callable]]] = None, # pretrans not possible yet
    subset: O[str] = "train",
) -> Dataset:
    """
    Creates the PCAM dataset and returns it as type HistoDataset, which inherits from torch.utils.data.Dataset.

    Data and further information can be found at https://humanunsupervised.github.io/humanunsupervised.com/pcam/pcam-cancer-detection.html

    Arguments:
        root: Absolute path to the dataset files.
        transformation: A callable or a list of callable transformations.
        subset: Which part of the dataset should be used.
                One of {"train", "validation", "test"}

    Returns:
        torch.utils.data.Dataset:
            The dataset that loads the pcam patches. You can use this
            as normal pytorch dataset. If you call it, the data will
            be returned as dictionary with structure:
            dict['images': torch.Tensor, 'labels': torch.Tensor].
    """
    if subset:
        subset = subset.lower()
    if subset.startswith("tr"):
        imgs_hdf5_filepath = root + "/camelyonpatch_level_2_split_train_x.h5"
        labels_hdf5_filepath = root + "/camelyonpatch_level_2_split_train_y.h5"
        return PCAM(
            imgs_hdf5_filepath=imgs_hdf5_filepath,
            labels_hdf5_filepath=labels_hdf5_filepath,
            transform=transformation,
        )
    elif subset.startswith("val"):
        imgs_hdf5_filepath = root + "/camelyonpatch_level_2_split_valid_x.h5"
        labels_hdf5_filepath = root + "/camelyonpatch_level_2_split_test_y.h5"
        return PCAM(
            imgs_hdf5_filepath=imgs_hdf5_filepath,
            labels_hdf5_filepath=labels_hdf5_filepath,
            transform=transformation,
        )
    elif subset.startswith("te"):
        imgs_hdf5_filepath = root + "/camelyonpatch_level_2_split_valid_x.h5"
        labels_hdf5_filepath = root + "/camelyonpatch_level_2_split_test_y.h5"
        return PCAM(
            imgs_hdf5_filepath=imgs_hdf5_filepath,
            labels_hdf5_filepath=labels_hdf5_filepath,
            transform=transformation,
        )
    # TODO use case not possible yet
    # elif subset == 'all':
    #     pass
    else:
        raise NotImplementedError(
            'The parameter "subset" needs to be one of ["train", "validation", "test"].'
        )


class PCAM(Dataset):
    """
    Creates the PCAM dataset and returns it as type HistoDataset, which inherits from torch.utils.data.Dataset.

    Data and further information can be found at https://humanunsupervised.github.io/humanunsupervised.com/pcam/pcam-cancer-detection.html
    """

    def __init__(
        self,
        imgs_hdf5_filepath: str,
        labels_hdf5_filepath: str,
        imgs_key: str = "x",
        labels_key: str = "y",
        transform: O[Compose] = None,
    ):
        """
        Initializes dataset.
        """

        self.imgs_hdf5_filepath = imgs_hdf5_filepath
        self.labels_hdf5_filepath = labels_hdf5_filepath
        self.imgs_key = imgs_key
        self.labels_key = labels_key

        self.transform = transform

    def __len__(self):
        """
        Returns length of dataset
        """
        with File(self.labels_hdf5_filepath, "r") as db:
            lens = len(db[self.labels_key])

        return lens

    def __getitem__(self, idx: int) -> dict:
        """
        TODO
        """

        # get images
        with File(self.imgs_hdf5_filepath, "r") as db:
            image = db[self.imgs_key][idx]
        # get labels
        with File(self.labels_hdf5_filepath, "r") as db:
            label = db[self.labels_key][idx][0][0][0]  # TODO make it nice

        # transform data
        if self.transform:
            image = self.transform(image)

        return {"data": image, "feature": label}
