# Changelog
All notable changes to this project will be documented in this file.
The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Unreleased
### Added
* Dynamically add labels to class map (via [#78](https://github.com/rsomani95/datawidgets/pull/78/))
### Changed

---

## [0.1.0] - 23rd April, 2021
### Added
* ANN Integration - Spotify's [`Annoy`](https://github.com/spotify/annoy) (via [#72](https://github.com/rsomani95/datawidgets/pull/72))
* Started adding some tests
* Review items unloading (via [#77](https://github.com/rsomani95/datawidgets/pull/77))
### Changed
* Rename:
  * `"Class Map Filtering Controls"` -> `"Label Filters"`
  * `"Metadata Filtering Controls"` -> `"Metadata Filters"`
* Split dataset classes into separate modules - `base_dataset` and `classification_dataset`
* Default index is now a numeric one as opposed to the filename
* Made `get_results` more transparent (Fixed [#23](https://github.com/rsomani95/datawidgets/issues/23))
* Rename `ImageGridMixin` and its methods to a more generic `LabellingGridMixin`
* Internal dataset is initialised with dedicated columns for mark attributes (`is_under_review`, `is_completed`, etc). This has many benefits:
  * Class `property`s like `num_completed`, `num_under_review`, etc. are computed using the internal `df`'s filters, which is vectorised as opposed to for loops previously
  * `update_grid` gets a massive upgrade. Instead of awkward looping and nested if statements, we now filter the dataset and index exactly where we need to
  * `update_grid_range_slider`'s logic is also now updated with the mark filters, making it much cleaner, and less hacky
  * All review datapoints are gathered by indexing into the `df` rather than cumbersome for loops with if-else blocks
* Improved performance for larger scale batch editing (via [#76](https://github.com/rsomani95/datawidgets/pull/76/) and [this commit](https://github.com/rsomani95/datawidgets/commit/a7bf170e2a946a509254a33349890318868f4778)).
* **Bugfix**: Fetching review items was loading _all_ the previous datapoints behind the scenes
* **Bugfix**: `update_grid` was ignoring `review_datapoints` and unloaded those unnecessarily

---

## [0.0.9] - 16th April, 2021
### Added
* Generalise `ClassificationDataset` and do some ground work for setting up a generic API to define custom data types (via [#68](https://github.com/rsomani95/datawidgets/pull/68))
* Numeric ID for `ImageDataItem`s (via [#69](https://github.com/rsomani95/datawidgets/pull/69))
* Metadata filtering (via [#63](https://github.com/rsomani95/datawidgets/pull/63))
  * Allows you to (optionally) add a column with a list of tags that help you filter through your data more effectively
  * With [#65](https://github.com/rsomani95/datawidgets/pull/65), you can add multiple such columns
  * You can view stats for both metadata and label columns (via [#64](https://github.com/rsomani95/datawidgets/pull/64))
* Data validation
  * Coerce input column to string type to avoid sneaky `PosixPath` bugs
  * Ensure that the input `DataFrame` is tidy i.e. each datapoint occupies no more than one row

### Changed
* Filtering controls are collapsible (via [#66](https://github.com/rsomani95/datawidgets/pull/66))
* Moved all exceptions to dedicated file

---

## [0.0.8] - 14th April, 2021
### Added
* Cleaner item unloading implementation (via [#62](https://github.com/rsomani95/datawidgets/pull/62))
### Changed
* Fixed image ordering logic ([#29](https://github.com/rsomani95/datawidgets/issues/29))

---

## [0.0.7] - 13th April, 2021
### Added
* Matplotlib theme for plotting
* Restore progress functionality (via [#60](https://github.com/rsomani95/datawidgets/pull/60))
* Introduce high level API for image classification datasets (via [#58](https://github.com/rsomani95/datawidgets/pull/59))
  * You can now setup labelled or unlabelled datasets from a bunch of files and/or folder using `ImageClassificationDataset.from{labelled|unlabelled}_file_collection`

### Changed


---
## [0.0.6] - 10th April, 2021
### Added
* **_`Stats`_** tab to view label distribution for different views of the data (via [#54](https://github.com/rsomani95/datawidgets/pull/54), and [this commit](https://github.com/rsomani95/datawidgets/commit/b649ce93a8e09010dacd41006f68f9f012b2082d))
* Custom CSS for all the custom widget classes (via [#55](https://github.com/rsomani95/datawidgets/pull/55))
* Ability to use selection and _all_ marking controls in the review tab
* Myriad UI improvements
  * Show image grid range & marking controls at bottom of main labelling grid
  * Etc.

### Changed
* Make internal code cleaner and more consistent (via [#53](https://github.com/rsomani95/datawidgets/pull/53))
* Improvements in logic to unload items that aren't being viewed
  * This needs some serious reworking. The logic is messy and inconsistent

---
## [0.0.5] - 7th April, 2021

### Added
* Lazy loading support (via [#43](https://github.com/rsomani95/datawidgets/pull/43))
  * Initial setup is now > 10x faster! None of the widgets are created on init, but only when required to be viewed
  * Similarly, images that aren't being viewed are unloaded to reduce memory load for larger datasets
* "_Looked At_" attribute added to the info bar
* _Minimal View_ functionality:
  * Press a button to go into "minimal mode", where you only see images inside the grid. All labels and other components are hidden, and the border is reduced
  * Useful when you only want to inspect a filtered set of images for visual similarity

### Changed
* `ImageClassificationDataset.get_results` only shows results of items that have been loaded i.e. looked at while labelling
* Rename `Strict Matching Mode` -> `Exact Matching Mode`
* Marking images as _**deleted**_ or _**completed**_ can now be done with selections made across multiple pages. Earlier, you could only do these operations on images *in* the grid
  * Technically, this is achieved by looping over `self.datapoints` rather than `self.active_datapoints`

---
## [0.0.4] - 5th April, 2021

### Added
* `Mark As Review`: allows user to mark selected images as under review
* Added `Show All Review` and `Show All Deleted` buttons in the UI Review Tab
* Design pattern of _"marking"_ images (as `completed`, `under_review`, or `deleted`)
* Generalised callback system for watching mouse events at the data level (via [#42](https://github.com/rsomani95/datawidgets/pull/42))

### Changed
* Move all marking attributes to dedicated module at both the individual data and dataset level
* Deleting an image doesn't modify the internal dataset but is now only an attribute, like `is_completed` or `is_under_review`
* Refactor UI setup of all _marking_ functionality into dedicated `setup_view...` functions
* `ImageClassificationDataset.get_modified_df` -> `ImageClassificationDataset.get_results`
  * Now displays all items that were _not deleted_
  * Earlier, we returnds items that were either _modified_ or marked as _completed_