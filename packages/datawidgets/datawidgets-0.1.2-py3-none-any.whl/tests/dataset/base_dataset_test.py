import pytest
from types import SimpleNamespace
from datawidgets.all import *


@pytest.mark.parametrize(
    ["filt", "result"],
    [
        (
            [1, 2, 3],
            np.array([1, 2, 3]),
        ),
        (
            pd.Series(["Values Dont Matter", "Indices Do"]),
            np.array([0, 1]),
        ),
        (
            pd.Series([10, 20], index=[2, 3]),
            np.array([2, 3]),
        ),
        (
            np.array([1, 2, 3]),
            np.array([1, 2, 3]),
        ),
        # Boolean indexing has different behavior. Indices are returned based
        # on the boolean values (like `np.where`)
        (
            pd.Series([True, False]),
            np.array([0]),
        ),
        (
            np.array([True, False]),
            np.array([0]),
        ),
        (
            pd.Series([True, False, True, True]),
            np.array([0, 2, 3]),
        ),
        (
            pd.Series([True, False, True], index=[4, 5, 6]),
            np.array([4, 6]),
        ),
        ([False, False, True], np.array([2])),
    ],
)
def test_check_filter(filt, result):
    assert (BaseDataset._check_filter(filt) == result).all()


def test_filter_dataset_basic(dset_img):
    df = dset_img.filter_dataset([0, 3, 2])
    assert (df.index.values == np.array([0, 3, 2])).all()
