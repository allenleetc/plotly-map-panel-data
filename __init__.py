import os

import eta.core.web as etaw
import eta.core.utils as etau
import fiftyone as fo

def download_and_prepare(dataset_dir, split=None, **kwargs):
    """Downloads the dataset and prepares it for loading into FiftyOne.

    Args:
        dataset_dir: the directory in which to construct the dataset
        split (None): a specific split to download, if the dataset supports
            splits. The supported split values are defined by the dataset's
            YAML file
        **kwargs: optional keyword arguments that your dataset can define to
            configure what/how the download is performed

    Returns:
        a tuple of

        -   ``dataset_type``: a ``fiftyone.types.Dataset`` type that the
            dataset is stored in locally, or None if the dataset provides
            its own ``load_dataset()`` method
        -   ``num_samples``: the total number of downloaded samples for the
            dataset or split
        -   ``classes``: a list of classes in the dataset, or None if not
            applicable
    """

    scratch_dir = os.path.join(dataset_dir, "scratch")
    zip_path = os.path.join(scratch_dir, "dataset.zip")
    unzip_dir = dataset_dir
    uri = "https://drive.usercontent.google.com/download?id=1QR0JV0-rRAeLacTFTvG-SYfl6pgGvJEc"

    if not os.path.isfile(zip_path):
        etaw.download_file(uri, path=zip_path)
    if not os.path.isfile(os.path.join(unzip_dir, "metadata.json")):
        etau.extract_zip(zip_path, outdir=unzip_dir, delete_zip=False)
            

    dataset_type = fo.types.FiftyOneDataset

    # Indicate how many samples have been downloaded
    # May be less than the total size if partial downloads have been used
    num_samples = 99

    # Optionally report what classes exist in the dataset
    classes = None

    return dataset_type, num_samples, classes