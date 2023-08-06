import pytest
from datawidgets.all import *


@pytest.fixture()
def img_paths():
    rootdir = Path(__file__).parent.parent / "sample_data"
    return [
        rootdir / "4JHZORY1.jpg",
        rootdir / "BR67C7LL.jpg",
        rootdir / "D82RT0FM.jpg",
        rootdir / "JH4AQJD3.jpg",
    ]


@pytest.fixture()
def df(img_paths):
    # fmt: off
    path1, path2, path3, path4 = img_paths
    row1 = [path1, ["exterior", "street"],  "group-shot",   "medium-long", "warm"]
    row2 = [path2, ["interior"],            "clean-single", "closeup",     "cool"]
    row3 = [path3, ["exterior", "beach"],   "clean-single", "medium",      "cool"]
    row4 = [path4, ["interior", "room"],    "clean-single", "closeup",     "warm"]
    # fmt: on

    df = pd.DataFrame(
        data=[row1, row2, row3, row4],
        columns=[
            "filename",
            "scene",
            "shot-type",
            "shot-framing",
            "color-temperature",
        ],
    )
    df["embedding"] = [
        np.array([1, 1, 1, 2]),
        np.array([3, 0, 1, 2]),
        np.array([6, 0, 1, 2]),
        np.array([0, 8, 1, 2]),
    ]
    df["embedding2"] = df["embedding"] * 0.5
    return df


@pytest.fixture()
def dset_img(df):
    return ClassificationDataset(
        df,
        filename_col="filename",
        label_col="scene",
        data_type=ImageDataItem,
        batch_size=2,
        metadata_col=None,
        _use_column_prefixes=True,
    )
