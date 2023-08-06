import pytest
from datawidgets.all import *


@pytest.mark.parametrize(
    ["property", "result"],
    [
        ("num_completed", 0),
        ("num_under_review", 0),
        ("num_deleted", 0),
        ("num_modified", 0),
        ("num_selected", 0),
        ("num_loaded", 2),
        ("num_fully_loaded", 2),
        ("num_needs_refresh", 0),
        ("selected_names", []),
        ("selected_items", []),
        ("selected_ids", []),
    ],
)
def test_mark_properties_on_init(property, result, dset_img):
    """
    Basic test to see if mark properties are initialised correctly
    """
    dset = dset_img
    assert getattr(dset, property) == result


@pytest.mark.parametrize(
    "mark_attr",
    [("hide_review"), ("hide_completed"), ("hide_deleted")],
)
def test_mark_filters_show_all_items_when_false(dset_img, mark_attr):
    """
    Ensure that no images are hidden by the marking filters when we are
    don't want to hide them
    """
    # If self.hide_review or self.hide_... is False, we return True
    # for _all_ items as we'd like to see all of them
    setattr(dset_img, mark_attr, False)
    assert getattr(dset_img, f"{mark_attr}_filter").all()


@pytest.mark.parametrize(
    ["mark_attr", "hide_mark_attr_items"],
    [
        ("hide_review", True),
        ("hide_completed", True),
        ("hide_deleted", True),
        ("hide_review", False),
        ("hide_completed", False),
        ("hide_deleted", False),
    ],
)
def test_mark_filter_toggles(dset_img, mark_attr, hide_mark_attr_items):
    """
    Check if toggle buttons for marks like `mark_review` change the status
    upon being clicked
    """
    dset = dset_img

    # == 'review' | 'completed' | 'deleted'
    mark_name = mark_attr.split("_")[-1]

    # if not dset.hide_review is True; make it True
    # by clicking the toggle button
    if not getattr(dset, mark_attr) is hide_mark_attr_items:
        getattr(dset, f"mark_{mark_name}_toggle").click()
        assert getattr(dset, mark_attr) is hide_mark_attr_items


@pytest.fixture()
def dset_img_simulated(dset_img):
    """
    Simulate some UI interactions
      * Modify one image's labels
      * Mark one as completed
      * Mark one as under review
      * Mark one as deleted
    """
    # # fmt: off
    # # Modify the first image's label
    # (
    #     dset_img
    #     .active_datapoints[0]
    #     .label_buttons.buttons.children[0]
    #     .click()
    # )
    # # fmt: on

    def select_first_img():
        dset_img.active_datapoints[0].select()

    # Mark the selected image as completed
    select_first_img()
    dset_img.mark_completed_button.click()

    # Mark the selected image as deleted
    select_first_img()
    dset_img.mark_deleted_button.click()

    # Mark the selected image as under review
    select_first_img()
    dset_img.mark_review_button.click()

    return dset_img


@pytest.mark.parametrize(
    ["property", "result"],
    [
        ("num_completed", 1),
        ("num_under_review", 1),
        ("num_deleted", 1),
        # ("num_modified", 1),
    ],
)
def test_mark_properties_basic_simulation(property, result, dset_img_simulated):
    """
    Check if selecting an image and clicking the mark toggle button works
    as expected
    """
    dset = dset_img_simulated
    assert getattr(dset, property) == result
