## Tests Priority

`filter_dataset`
`filter_and_mutate_dataset`
`update_grid`
`mark_filters`
`update_dataset`

---

## Abstract Classes

### `AbstractInterface`

Both data and dataset classes inherit from this. It does some very minimal setup and forces both to use a similar API

### `AbstractItemInterface`

Data classes only

### `AbstractDataItem`

Data classes only

### `BaseDataset`

---

## Two Level Hierarchy

### 1. Individual Data Points
### 2. Datasets (Aggregates of (1))

---

## Mixins & Extensions

These are used, more than anything, for organisational purposes. It helps keep a chunk of code that does one thing in one place and offers more granular control than creating separate modules for everything. 

### Mixins

* All have a `setup_...()` method which must be called in the dataset class's `setup()` method
* Some UI elements are setup in a `generate_...()` method that is called in either the mixin's or dataset class's `setup...view()` as it requires additional callbacks that may come from other mixins
* Some have a `setup...view()` method which takes one arg for passing in a list of callbacks. These must be called in the dataset class's `setup_view()` and can take in callbacks that modify behavior from other mixins

---

## High Level Overview of Mixins

### `BatchClassificationLabelsMixin`
* Sets up `batch_add` and `batch_remove` functionality that can be used on _all selected data points_.
* `batch_add` button lets you add any of the labels from the dataset's `.classes`
* `batch_remove` shows a union of all selected items' labels

### `WidthSliderMixin`
Sets up ability to control the width of data items in the labelling grid

### `InfoMixin`
Sets up the info bar that displays a bunch of key info about the dataset at a glance:
* Num Selected
* Num Displayed
* Num Filtered
* Num Total Items
* Num Looked At
* Num Completed
* Num Deleted

### `SelectionMixin`

Adds functionality to `select_all` or `unselect_all` items from `selection_source`. Based on `selection_source`, you could select
* items in the main labelling tab (`selection_source = "active_datapoints"`)
* items in the review tab (`selection_source = "review_datapoints"`)
* _all_ items in the dataset (`selection_source = "datapoints"`)

