import os
from typing import Callable
from typing import Optional as O
from typing import Sequence
from typing import Union as U
import numpy as np

from ..base import data_readers, df_creators, df_manipulators
from ..base.histo_dataset import HistoDataset


import os

from ..base import data_readers, df_creators, df_manipulators
from ..base.histo_dataset import HistoDataset


def midog_classification_patches(
    root,  # '/data/ldap/histopathologic/original_read_only/MIDOG'
    transformation=None,
    pre_transformation=None,
    subset="all",
    splitting_seed=69,
    splitting_trainings_percentage=0.8,
    scanner_to_use=None,
    seed=None,
    patch_size=None,
):
    manipulators_to_use = []
    
    if subset == "train":
        manipulators_to_use.append(
            df_manipulators.RandomFilterByColumnValue(
                "image_id", splitting_trainings_percentage, mode=0, seed=splitting_seed
            )
        )
    elif subset == "valid":
        manipulators_to_use.extend(
            [
                df_manipulators.RandomFilterByColumnValue(
                    "image_id", splitting_trainings_percentage, mode=1, seed=splitting_seed
                ),
                df_manipulators.RandomFilterByColumnValue(
                    "image_id", 0.5, mode=0, seed=splitting_seed + 10000
                ),
            ]
        )
    elif subset == "test":
        manipulators_to_use.extend(
            [
                df_manipulators.RandomFilterByColumnValue(
                    "image_id", splitting_trainings_percentage, mode=1, seed=splitting_seed
                ),
                df_manipulators.RandomFilterByColumnValue(
                    "image_id", 0.5, mode=1, seed=splitting_seed + 10000
                ),
            ]
        )
    elif subset == "all":
        pass
    else:
        raise NotImplementedError(
            'The parameter "subset" needs to be one of ["train", "valid", "test", "all"].'
        )
        
    if scanner_to_use is not None:
        if isinstance(scanner_to_use, int):
            allowed_values = np.arange(50)+1+50*scanner_to_use
        elif isinstance(scanner_to_use, list):
            allowed_values = []
            for s in scanner_to_use:
                allowed_values.extend(np.arange(50)+1+50*s)
        else:
            raise NotImplementedError(
                'The parameter "scanner_to_use" needs to be None, an integer or a list.'
            )
        manipulators_to_use.append(df_manipulators.ColumnFilter('image_id', allowed_values))
            
    manipulators_to_use.append(df_manipulators.BoundingBoxToCenterCoordinates('bbox'))
    
    data_reader = data_readers.ReadFromImageFile(
            "images/{image_id:03d}.tiff", return_image_size=patch_size
        )
    
    ds = HistoDataset(
        df_creators.CreateDFFromJSON('MIDOG.json', 'annotations'),
        root,
        df_manipulators=manipulators_to_use,
        data_readers=data_reader,
        feature_readers=data_readers.ReadValueFromCSV(
            r"{category_id}", encoded_values=[1, 2]
        ),
        seed=seed,
        pre_transfs=pre_transformation,
        da_transfs=transformation,
    )
    return ds

