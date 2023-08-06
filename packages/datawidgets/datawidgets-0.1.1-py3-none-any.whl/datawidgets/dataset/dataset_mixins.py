from datawidgets.imports import *
from datawidgets.utils import *
from datawidgets.data import *

# from .base_dataset import *
# from .classification_dataset import *


class BatchClassificationLabelsMixin:
    _works_with = "ImageDatasetWithLabels"

    def setup_batch_labelling(self):
        # Create add and remove buttons
        self.batch_add_button = vue_autocomplete_box(
            items=self.classes,
            css_classes=[CSS_NAMES.BATCH_ADD_BUTTON],
        )

        self.batch_remove_button = vue_autocomplete_box(
            items=self.classes,
            css_classes=[CSS_NAMES.BATCH_REMOVE_BUTTON],
        )

        # Attach observers / callbacks to batch labelling buttons
        self.batch_add_button.observe(self.add_batch_label)
        self.batch_remove_button.observe(self.remove_batch_label)

    @property
    def batch_add_value(self):
        return self.batch_add_button.v_model

    @property
    def batch_remove_value(self):
        return self.batch_remove_button.v_model

    def update_batch_labelling_descriptions(self, *args):
        self.batch_add_button.label = f"Batch Add ({len(self.selected_items)})"
        self.batch_remove_button.label = f"Batch Remove ({len(self.selected_items)})"

        # `hasattr` is used here IN CASE this function is called before
        # `setup_batch_labelling` is called. We could probably do away with
        # it but it's here for safety as setup functions don't have an order
        if hasattr(self, "class_map_negative_buttons"):
            self.batch_remove_button.items = flatten(
                [item.label_buttons.labels for item in self.selected_items]
            )

    def add_batch_label(self, change):
        if self.batch_add_value in self.classes:
            for item in self.selected_items:
                if not item.max_labels_selected:
                    item.add_label(self.batch_add_value)
            self.batch_add_button.v_model = ""

    def remove_batch_label(self, change):
        if self.batch_remove_value in self.classes:
            for item in self.selected_items:
                item.remove_label(self.batch_remove_value)
            self.batch_remove_button.v_model = ""


class WidthSliderMixin:
    def setup_width_slider(self):
        self.width_slider = widgets.IntSlider(
            value=self.width,
            min=1,
            max=100,
            description="Image Width:",
            layout=widgets.Layout(align_items="center"),
        )
        self.width_slider.continuous_update = False
        self.width_slider.observe(
            lambda x: setattr(self, "width", self.width_slider.value)
        )


class SelectionMixin:
    ""
    selection_source = "active_datapoints"

    def unselect_all(self, *args, callbacks=[]):
        for item in getattr(self, self.selection_source):
            item.unselect()

    def select_all(self, *args, callbacks=[]):
        for item in getattr(self, self.selection_source):
            item.select()

    def invert_selection(self, *args, callbacks=[]):
        for item in getattr(self, self.selection_source):
            if item.is_selected:
                item.unselect()
            else:
                item.select()

    def generate_unselect_all_button(self, callbacks=[]):
        "Generates a button that unselects all selected items"

        unselect_all_button = Button(description="Unselect All")
        unselect_all_button.on_click(self.unselect_all)
        for cb in callbacks:
            unselect_all_button.on_click(cb)

        return unselect_all_button

    def generate_select_all_button(self, callbacks=[]):
        "Generates a button that selects all selected items"

        select_all_button = Button(description="Select All")
        select_all_button.on_click(self.select_all)
        for cb in callbacks:
            select_all_button.on_click(cb)

        return select_all_button

    def generate_invert_selection_button(self, callbacks=[]):
        "Generates a button to invert selected items"

        button = Button(description="Invert Selection")
        button.on_click(self.invert_selection)
        for cb in callbacks:
            button.on_click(cb)

        return button


class MinimalViewMixin:
    minimal_view_mode = False

    def generate_minimal_view_button(self, callbacks=[]):
        button = Button(description="Toggle Minimal View")
        button.layout.width = "200px"
        button.on_click(self.toggle_minimal_view_mode)

        for cb in callbacks:
            button.on_click(cb)

        return button

    def toggle_minimal_view_mode(self, *args):
        self.minimal_view_mode = not self.minimal_view_mode
        self.update_grid()


class LabellingGridMixin:
    """
    Sets up `self.grid` to contains `self.images`.
    Use `generate_grid_range_slider` followed by `set_grid_range_slider` in a global
      context like so:

    dset = ImageDataset(...)
    def REFRESH_GLOBAL_DISPLAY(...)
    indxs_slider = dset.generate_grid_range_slider(callbacks=[REFRESH_GLOBAL_DISPLAY])
    dset.set_grid_range_slider(indxs_slider)
    """

    _maybe_uses = ["ClassMapFilterMixin"]

    def setup_labelling_grid(self):
        self.grid = widgets.Box(
            children=[],
            width="100%",
            layout=CSS_LAYOUTS.flex_layout,
        )
        self.update_grid()

    def update_grid(self, *args, df: pd.DataFrame = None):
        """Sets up self.grid to all `self.images` if no grid range slider is initialised
        else to the interval values of the slider
        """
        items = []
        prev_batch = []
        next_batch = []

        # Get lower and upper bounds for looping over datapoints
        if hasattr(self, "grid_range_slider"):
            start, end = self.grid_range_slider.value
        else:
            start, end = (0, self.batch_size)

        df = None
        if hasattr(self, "positive_class_map_filter"):
            if not self.empty_metadata:
                df = self.filter_dataset(
                    self.class_map_subset_filter
                    & self.metadata_subset_filter
                    & self.mark_filters
                )
            else:
                df = self.filter_dataset(
                    self.class_map_subset_filter & self.mark_filters
                )

        # more like when self.hasattr...
        if hasattr(self, "active_datapoints"):
            # prev_batch = [item.source for item in self.active_datapoints]
            prev_batch = [item.id for item in self.active_datapoints]

        if hasattr(self, "positive_class_map_filter"):
            # Get items for the next batch
            for row in df.iloc[start:end].itertuples():
                index = row[0]
                item = self.datapoints[index]
                next_batch.append(item.id)

            # Load next items first
            for item_id in next_batch:
                item = self.datapoints[item_id]
                if not item.is_loaded:
                    item.load()
                    item.update_view()
                elif item.is_loaded and item.needs_refresh:
                    item.refresh()

                if hasattr(self, "minimal_view_mode"):
                    if self.minimal_view_mode:
                        item.update_view_minimal()
                    else:
                        item.update_view()
                items.append(item)

        else:
            # This gets executed only the first time we call `update_grid`
            # i.e. before `active_datapoints` exist or filtering is setup
            for i, (key, item) in enumerate(self.datapoints.items()):
                if i >= start and i < end:
                    items.append(item)

        children = [i.view for i in items]
        self.active_datapoints = items
        self.grid.children = children

        # Unload after loading (so it doesn't look ugly as hell)
        # Also ensure that we don't unload items in the review grid
        next_batch.extend([item.id for item in self.review_datapoints])
        for fname in np.setdiff1d(prev_batch, next_batch):
            item = self.datapoints[fname]
            item.unload()

    def reset_grid_range_value(self, *args):
        self.grid_range_slider.value = (0, self.batch_size)

    def set_grid_range_slider(self, grid_range_slider: widgets.IntRangeSlider):
        self.grid_range_slider = grid_range_slider
        self.update_grid()

    def update_grid_range_slider(self, *args):
        min_value, max_value = self.grid_range_slider.value
        max_limit = len(self)

        if max_value > len(self):
            max_value = len(self)

        # Adjust values based on currently applied filters
        if hasattr(self, "positive_class_map_filter"):
            if not self.empty_metadata:
                max_limit = (
                    self.class_map_subset_filter
                    & self.metadata_subset_filter
                    & self.mark_filters
                ).sum()
            else:
                max_limit = (self.class_map_subset_filter & self.mark_filters).sum()

        if max_value > max_limit:
            max_value = max_limit
        if min_value > max_limit:
            # HACK ? reset min value...
            # TODO: is this necessary??
            min_value = 0

        self.grid_range_slider.value = (min_value, max_value)
        self.grid_range_slider.max = max_limit

    def generate_grid_range_slider(self, callbacks=[]):
        grid_range_slider = widgets.IntRangeSlider(
            value=(0, self.batch_size),
            min=0,
            max=len(self),
            description="Show Images #",
        )
        grid_range_slider.add_class(CSS_NAMES.GRID_RANGE_SLIDER)
        grid_range_slider.continuous_update = False

        def increment_range(*args):
            range_values = grid_range_slider.value
            grid_range_slider.value = (
                range_values[1],
                range_values[1] + self.batch_size,
            )
            self.update_grid_range_slider()

        def decrement_range(*args):
            range_values = grid_range_slider.value
            grid_range_slider.value = (
                range_values[0] - self.batch_size,
                range_values[0],
            )
            self.update_grid_range_slider()

        grid_range_slider.observe(self.update_grid, "value")
        if hasattr(self, "update_info"):
            grid_range_slider.observe(self.update_info, "value")
        grid_range_slider.observe(self.update_grid_range_slider, "value")

        for cb in callbacks:
            grid_range_slider.observe(cb, "value")

        increment_button = Button(description="»")
        decrement_button = Button(description="«")

        increment_button.add_class(CSS_NAMES.RANGE_NEXT_PREV_BUTTONS)
        decrement_button.add_class(CSS_NAMES.RANGE_NEXT_PREV_BUTTONS)
        increment_button.on_click(increment_range)
        decrement_button.on_click(decrement_range)

        return decrement_button, grid_range_slider, increment_button


class InfoMixin:
    _update_info_now = True

    def update_info(self, *args, additional_info: List[str] = []):
        if self._update_info_now:
            if isinstance(additional_info, str):
                additional_info = [additional_info]

            num_images_in_grid = len(getattr(self, self.selection_source))
            if hasattr(self, "class_map_positive_buttons"):
                if self.empty_metadata:
                    num_filtered_images = self.class_map_subset_filter.sum()
                else:
                    num_filtered_images = (
                        self.class_map_subset_filter & self.metadata_subset_filter
                    ).sum()

            info = [
                f"Selected: {self.num_selected}",
                f"Displayed: {num_images_in_grid}",
                f"Filtered: {num_filtered_images}",
                f"Total: {len(self)}",
                f"Deleted: {self.num_deleted}",
                f"Modified: {self.num_modified}",
                f"Looked At: {self.num_loaded}/{len(self)}",
                f"Completed: {self.num_completed}/{len(self)}",
            ]

        else:
            NA_TEXT = "N/A"
            info = [
                f"Selected: {NA_TEXT}",
                f"Displayed: {NA_TEXT}",
                f"Filtered: {NA_TEXT}",
                f"Total: {NA_TEXT}",
                f"Deleted: {NA_TEXT}",
                f"Modified: {NA_TEXT}",
                f"Looked At: {NA_TEXT}",
                f"Completed: {NA_TEXT}",
            ]

        info = "&emsp;&emsp;".join(info)
        self.info.value = f"<h5>{info}<h5>"
        self.info.add_class(CSS_NAMES.MAIN_INFO_PANEL)
        self.info.layout = CSS_LAYOUTS.flex_layout

    def _toggle_update_info_now(self):
        self._update_info_now = not _update_info_now

    def setup_info(self):
        # Setup info bar
        self.info = widgets.HTML()

        def update_info_definitely(*args):
            self._update_info_now = True
            self.update_info()
            self._update_info_now = False

        self.refresh_info = Button(description="⟳")
        self.refresh_info.layout.width = "40px"
        self.refresh_info.on_click(update_info_definitely)
        self.refresh_info.add_class(CSS_NAMES.INFO_REFRESH_BUTTON)
        self.info_bar = HBox([self.refresh_info, self.info])
        self._setup_settings_info_realtime()

    def _setup_settings_info_realtime(self):
        "Setup global settings for updating info bar in realtime"

        # Create dropdown menu with options
        self.settings_info_realtime = widgets.Dropdown(
            options=[True, False],
            description="Update Info Realtime: ",
        )
        self.settings_info_realtime.add_class(CSS_NAMES.SETTINGS)
        self.settings_info_realtime.add_class(CSS_NAMES.SETTINGS_INFO_REALTIME)

        # Attach event observers:
        #   * Set update info in realtime to True
        #   * Update info on changing value
        self.settings_info_realtime.observe(
            lambda x: setattr(
                self, "_update_info_now", self.settings_info_realtime.value
            ),
        )
        self.settings_info_realtime.observe(self.update_info)


class RestoreProgressMixin:
    def setup_restore_progress_button(self):
        self.restore_button_group = UploadButton(
            description="Upload Progress File (.csv, .feather)"
        )
        self.restore_button_group.upload_button.layout.width = "350px"
        self.restore_button_group.go_button.on_click(self._restore_progress)
        self.restore_button_group.go_button.on_click(self.update_info)
        self.restore_button_group.go_button.on_click(self.update_grid)

    def _restore_progress(self, *args):
        # Read uploaded CSV
        for _, v in self.restore_button_group.upload_button.value.items():
            pass

        try:
            restore_df = pd.read_csv(io.StringIO(str(v["content"], "utf-8")))
        except:
            restore_df = pd.read_feather(io.BytesIO(v["content"]))

        restore_df.index = restore_df[self.filename_col]
        # for item in tqdm(self.datapoints, desc="Restoring Data Items"):
        for index, row in tqdm(
            restore_df.iterrows(), desc="Restoring Data Items", total=len(restore_df)
        ):
            try:
                item = self.datapoints[index]
            except KeyError:
                continue

            item.load()
            item.update_view()

            # Marks require some more complex stuff. Maybe this should be
            # a traitlets implementation, though that might be overkill complexity

            item.mark_as_completed() if row.is_completed else item.unmark_as_completed()
            item.mark_as_deleted() if row.is_deleted else item.unmark_as_deleted()
            item.mark_as_under_review() if row.is_under_review else item.unmark_as_under_review()

            if isinstance(row.label, str):
                labels = ast.literal_eval(row.label)
            else:
                labels = list(row.label)

            item.set_labels(labels)
            item.is_modified = row.is_modified
