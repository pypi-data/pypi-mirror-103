from datawidgets.imports import *
from .review_mixins import *
from .filtering_mixins import *
from .dataset_mixins import *
from .mark_mixins import *
from .stats_mixins import *
from datawidgets.data import *
from datawidgets.interface import *
from datawidgets.utils import *
from datawidgets.exceptions import *


class BaseDataset(
    AbstractInterface,
    ImageGridMixin,
    WidthSliderMixin,
    SelectionMixin,
    InfoMixin,
):
    datapoints = []
    active_datapoints = []
    review_datapoints = []

    def __init__(
        self,
        df: pd.DataFrame,
        data_type: AbstractDataItem,
        batch_size: int = 50,
        width: int = 100,
        filename_col: str = "filename",
    ):
        self.df = df
        self.data_type = data_type
        self.batch_size = batch_size
        self.filename_col = filename_col
        self.df.index = self.df[self.filename_col]
        self.width = width
        # self.num_deleted = 0

        self.validate_unique_inputs(self.df, self.filename_col)
        self.coerce_string_inputs()

        init_matplotlib_theme()
        self.init_css()
        self.setup()
        self.setup_view()

    def coerce_string_inputs(self):
        self.df[self.filename_col] = self.df[self.filename_col].apply(str)

    @staticmethod
    def validate_unique_inputs(df, input_colname: str):
        "Raise an error if duplicate sources exist"

        num_unique_inputs = df[input_colname].unique().shape[0]
        num_datapoints = df.shape[0]

        if not num_unique_inputs == num_datapoints:
            duplicates = (
                df[input_colname]
                .value_counts()
                .reset_index()
                .rename(columns={input_colname: "frequency", "index": input_colname})
            )
            duplicates = duplicates[duplicates.frequency > 1]

            raise DuplicateInputsError(
                f"Expected df['{input_colname}'] to have unique values, but found "
                f"{len(duplicates)} duplicates: \n"
                f"{duplicates}"
            )

    def init_css(self):
        CSS = f"""
        <style>
        {(Path(__file__).parent.parent / "ui" / "style.css").read_text()}
        </style>
        """
        display(HTML(CSS))

    @abstractmethod
    def setup_items(self):
        "Sets up `self.datapoints`"
        pass

    @staticmethod
    def _check_filter(filter_: Union[Sequence[str], np.ndarray, pd.Series]):
        if isinstance(filter_, pd.Series):
            # Keep only True values if boolean masking
            if isinstance(filter_.iloc[0], (bool, np.bool8, np.bool)):
                filter_ = filter_[filter_]
            filter_ = filter_.index.values
        return filter_

    def filter_dataset(self, filter_: Union[Sequence[str], np.ndarray, pd.Series]):
        "Returns a view of `self.df` without any modifications"
        filter_ = self._check_filter(filter_)
        return self.df.loc[filter_]

    def filter_and_mutate_dataset(
        self, filter_: Union[Sequence[str], np.ndarray, pd.Series]
    ):
        """
        Reorder and/or delete items from internal dataset by self.df's index, which
            is set to the filename on init
        If passing in a boolean `pd.Series` mask, only True values are kept
        """
        filter_ = self._check_filter(filter_)
        items = {}
        for i in filter_:
            # del self.datapoints[i]
            items[i] = self.datapoints[i]
        self.datapoints = pd.Series(items)
        self.df = self.df.loc[filter_]
        self.source_index = self.df.index.copy()

    def refresh(self):
        self.update_grid()
        self.update_info()

    def setup(self):
        self.setup_items()
        self.setup_logging()
        self.setup_width_slider()
        self.setup_img_grid()
        self.setup_info()

    def __len__(self):
        return len(self.df)

    # TODO: Is it inefficient to have these properties for very large datasets?
    @property
    def selected_names(self):
        return [item.source for item in self.selected_items]

    @property
    def num_modified(self):
        return sum([item.is_modified for item in self.datapoints])

    @property
    def num_deleted(self):
        return sum([item.is_deleted for item in self.datapoints])

    @property
    def num_under_review(self):
        return sum([item.is_under_review for item in self.datapoints])

    @property
    def num_selected(self):
        num_selected = sum([item.is_selected for item in self.datapoints])
        if hasattr(self, "similarity_button"):
            if num_selected > 1:
                self.similarity_button.disabled = True
            else:
                self.similarity_button.disabled = False
        return num_selected

    @property
    def selected_items(self):
        return [item for item in self.datapoints if item.is_selected]
        # return [item for item in self.active_datapoints if item.is_selected]

    @property
    def num_loaded(self):
        return sum([item.is_loaded for item in self.datapoints])

    @property
    def num_fully_loaded(self):
        return sum(
            [item.is_loaded and not item.needs_refresh for item in self.datapoints]
        )

    @property
    def num_needs_refresh(self):
        return sum([item.needs_refresh for item in self.datapoints])

    @property
    def loaded_items(self):
        return [item for item in self.datapoints if item.is_loaded]

    @property
    def fully_loaded_items(self):
        return [item for item in self.loaded_items if not item.needs_refresh]


class ClassificationDataset(
    BaseDataset,
    BatchClassificationLabelsMixin,
    ClassMapFilterMixin,
    MetadataFilterMixin,
    ReviewMixin,
    DownloadModifiedMixin,
    LabelsStatsMixin,
    MinimalViewMixin,
    MarkSelectedAsCompletedMixin,
    MarkSelectedAsReviewMixin,
    MarkSelectedAsDeletedMixin,
    RestoreProgressMixin,
):
    def __init__(
        self,
        df,
        data_type: AbstractDataItem = ImageDataItem,
        filename_col: str = "filename",
        batch_size: int = 50,
        width: int = 25,
        class_map: Optional[ClassMap] = None,
        additional_classes: Optional[List[str]] = [],
        label_col: str = "label",
        metadata_col: Union[None, str, List[str]] = None,
        is_multilabel: bool = False,
        _use_column_prefixes: bool = True,
        _drop_metadata_columns: bool = False,
    ):
        # `additional_classes` are great for when you're auto configuring the
        # class map but want to add a few more options
        ""
        self.source_index = pd.Index(df[filename_col])
        self.df = df.copy()
        self.label_col = label_col
        self.filename_col = filename_col
        self.is_multilabel = is_multilabel
        self._use_column_prefixes = _use_column_prefixes
        self._drop_metadata_columns = _drop_metadata_columns
        self.metadata_col = metadata_col

        self.validate_metadata_colnames()

        if class_map is None:
            self.class_map = self.parse_class_map_from_df(
                additional_classes=additional_classes
            )
        else:
            self.class_map = class_map
        self.metadata_class_map = self.parse_metadata_class_map_from_df()

        self.classes = self.class_map._id2class
        self.metadata_classes = self.metadata_class_map._id2class

        # HACK: blah..
        super().__init__(
            df=self.df,
            filename_col=filename_col,
            batch_size=batch_size,
            width=100,
            data_type=data_type,
        )
        self.width = width
        self.width_slider.value = self.width

    def validate_metadata_colnames(self):
        if isinstance(self.metadata_col, str):
            self.metadata_col = [self.metadata_col]
        elif isinstance(self.metadata_col, list):
            self.metadata_col = self.metadata_col
        elif self.metadata_col is None:
            self.metadata_col = None
        else:
            raise TypeError(
                f"Expected {self.metadata_col} to be either a <str> or a <List[str]> "
                f"but got {type(self.metadata_col)} instead"
            )

    @classmethod
    def from_labelled_file_collection(
        cls,
        data_type: AbstractDataItem,
        folder_paths: Union[str, List[str]] = [],
        filenames: Union[str, List[str]] = [],
        batch_size: int = 50,
        grandparent: bool = False,
        additional_classes: Union[str, List[str]] = [],
        is_multilabel: bool = True,
    ):
        """
        Creates a dataset from a bunch of folders and declares the sets the name
          of the folder as the label
        A class map is created with these label names, and if there are any
          additional classes you'd like to add, you can pass it to `additional_classes`

        By default, the parent folder's name is used as the label. If you'd like to use
          the grandparent instead, use the `grandparent=True` flag
        """
        if isinstance(folder_paths, str):
            folder_paths = [folder_paths]

        image_files = flatten([get_image_files(f) for f in folder_paths]) + filenames
        df = pd.DataFrame(data=image_files, columns=["filepath"])
        df.loc[:, "label"] = df.apply(
            lambda row: Path(row.filepath).parent.parent.name
            if grandparent
            else Path(row.filepath).parent.name,  # parent level
            axis=1,
        )

        return cls(
            df=df,
            data_type=data_type,
            filename_col="filepath",
            batch_size=batch_size,
            class_map=None,
            additional_classes=additional_classes,
            label_col="label",
            is_multilabel=is_multilabel,
        )

    @classmethod
    def from_unlabelled_file_collection(
        cls,
        data_type: AbstractDataItem,
        folder_paths: Union[str, List[str]] = [],
        filenames: Union[str, List[str]] = [],
        batch_size: int = 50,
        class_map=None,
        is_multilabel: bool = True,
    ):
        """
        Creates a dataset from a bunch of filenames and/or images inside folders
        You can pass in a `class_map` object to declare valid label choices, else a
          blank one will be created for you
        """
        if isinstance(folder_paths, str):
            folder_paths = [folder_paths]

        image_files = flatten([get_image_files(f) for f in folder_paths]) + filenames
        df = pd.DataFrame(data=image_files, columns=["filepath"])
        df.loc[:, "label"] = df.apply(lambda x: [], axis=1)

        return cls(
            df=df,
            data_type=data_type,
            filename_col="filepath",
            batch_size=batch_size,
            class_map=class_map,
            label_col="label",
            is_multilabel=is_multilabel,
        )

    def parse_class_map_from_df(self, additional_classes: Optional[List[str]]):
        """
        Derives the ClassMap from all the unique values in `self.label_col`
        """
        self.df[self.label_col] = self.df[self.label_col].apply(convert_labels_to_list)
        if not self.is_multilabel:

            def truly_single_label(row: pd.Series):
                label = row[self.label_col]
                fname = row[self.filename_col]
                if not len(label) == 1:
                    raise ValueError(
                        f"Expected only one label per image in single label mode, but '{fname}' "
                        f"has {len(label)} labels: {label}"
                    )

            self.df.apply(truly_single_label, axis=1)

        all_labels = self.df[self.label_col].values
        return ClassMap(
            classes=uniqueify(flatten(all_labels)) + additional_classes,
            background=None,
        )

    def parse_metadata_class_map_from_df(self) -> ClassMap:
        """
        Sets up metadata filtering if being used. Does the following:

        1. Take all the metadata columns passed in
        2. Convert them to lists
        3. Combine them into a new column called "combined-metadata"
        4. Drop the input metadata columns
        5. Form
        """

        if self.metadata_col is None:
            self.empty_metadata = True
            self.metadata_col = "metadata"
            self.df.apply(lambda _: [], axis=1)
            return ClassMap(classes=[], background=None)

        self.empty_metadata = False

        # 2. Convert metadata columns to lists
        for col in self.metadata_col:
            self.df[col] = self.df[col].apply(convert_labels_to_list)

        # 3. Combine all the metadata columns into a new column

        ## Create prefixes for column values if using multiple cols
        if self._use_column_prefixes:
            if len(self.metadata_col) == 1:
                prefixer = lambda x: ""
            else:
                prefixer = lambda x: x.upper() + ": "
        else:
            prefixer = lambda x: ""

        ## Combine metadata w/ prefixes
        def combine_metadata(row: pd.Series):

            combined_metadata = []
            for col in self.metadata_col:
                combined_metadata.append(
                    [f"{prefixer(col)}{value}" for value in row[col]]
                )
            return flatten(combined_metadata)

        self.df["combined_metadata"] = self.df.apply(combine_metadata, axis=1)
        if self._drop_metadata_columns:
            self.df.drop(columns=self.metadata_col, inplace=True)
        self.metadata_col = "combined_metadata"

        all_labels = self.df[self.metadata_col].values
        return ClassMap(
            classes=uniqueify(flatten(all_labels)),
            background=None,
        )

    def get_results(self):
        # TODO: Use a named tuple or dataclass for rows
        rows = []

        # Iterate through all datapoints and find the completed / modified items
        for fname, item in self.datapoints.items():

            # TODO: Should we load and show all datapoints?
            # or skip the item altogether?
            if not item.is_loaded:
                continue
                # item.load()

            filename = fname
            labels = item.labels
            note = item.note.value

            if not item.is_deleted:
                rows.append(
                    [
                        fname,
                        labels,
                        note,
                        item.numeric_id,
                        item.is_modified,
                        item.is_completed,
                        item.is_under_review,
                        item.is_deleted,
                    ]
                )

        modified_df = pd.DataFrame(
            rows,
            columns=[
                self.filename_col,
                self.label_col,
                "notes",
                "numeric_id",
                "is_modified",
                "is_completed",
                "is_under_review",
                "is_deleted",
            ],
        )

        # Merge with main dataframe while replacing the `self.label_col`
        modified_df = modified_df.merge(
            self.df.drop(columns=[self.label_col]).reset_index(drop=True),
            on=self.filename_col,
        )
        modified_df.index = modified_df[self.filename_col]
        return modified_df

    def setup(self):
        # super().setup()

        self.setup_logging()
        self.setup_width_slider()
        self.setup_batch_labelling()

        self.setup_review_grid()
        self.setup_download_modified()

        self.setup_info()
        self.setup_items()

        self.setup_class_map_filtering()
        self.setup_metadata_filtering()
        self.setup_img_grid()

        self.update_info()
        self.update_batch_labelling_descriptions()
        self.setup_labels_stats()
        self.setup_restore_progress_button()

    @property
    def num_completed(self):
        return sum([item.is_completed for item in self.datapoints])

    def setup_items(self):
        items = {}
        for numeric_id, (fname, row) in tqdm(
            enumerate(self.df.iterrows(), start=1),
            total=len(self.df),
            desc="Setting Up Data Items",
        ):
            item = self.data_type(
                numeric_id=numeric_id,
                source=getattr(row, self.filename_col),
                class_map=self.class_map,
                labels=row[self.label_col],
                is_multilabel=self.is_multilabel,
                parent_dataset=self,
            )
            items[fname] = item
        self.datapoints = pd.Series(items)

    def setup_view(self, global_callbacks=[]):
        callbacks = [
            self.update_info,
            self.update_batch_labelling_descriptions,
        ]

        self.setup_class_map_filtering_view(global_callbacks=callbacks)
        self.setup_metadata_filtering_view(global_callbacks=callbacks)

        (
            decrement_range,
            view_range_slider,
            increment_range,
        ) = self.generate_grid_range_slider()
        unselect_button = self.generate_unselect_all_button(callbacks)
        select_button = self.generate_select_all_button(callbacks)
        invert_selection_button = self.generate_invert_selection_button(callbacks)
        self.minimal_view_button = self.generate_minimal_view_button()

        refresh_review_modified_button = self.generate_review_modified_button(
            [self.update_info]
        )
        refresh_view_selected_button = self.generate_selected_refresh_button(
            [self.update_info]
        )
        refresh_review_completed_button = self.generate_review_completed_button(
            [self.update_info]
        )
        refresh_review_review_button = self.generate_review_review_button(
            [self.update_info]
        )
        refresh_review_deleted_button = self.generate_review_deleted_button(
            [self.update_info]
        )
        refresh_export_button = self.generate_export_refresh_button()

        # Update grid range values upon clicking any of the filtering buttons
        self.class_map_filter_button.on_click(self.update_grid_range_slider)
        self.class_map_filter_button.on_click(self.reset_grid_range_value)
        self.metadata_filter_button.on_click(self.update_grid_range_slider)
        self.metadata_filter_button.on_click(self.reset_grid_range_value)

        try:

            def reset_grid_idxs(*args):
                self.grid_range_slider.value = (
                    0,
                    min(self.grid_range_slider.value[1], len(self)),
                )

            self.similarity_button = self.generate_similarity_button(callbacks=[])
            self.similarity_button.on_click(reset_grid_idxs)

        except:
            self.similarity_button = Button()
            self.similarity_button.layout = CSS_LAYOUTS.empty

        self.set_grid_range_slider(view_range_slider)

        self.setup_view_mark_completed(
            callbacks=[self.update_grid, self.update_grid_range_slider] + callbacks
        )
        self.setup_view_mark_review(
            callbacks=[self.update_grid, self.update_grid_range_slider] + callbacks
        )
        self.setup_view_mark_deleted(
            callbacks=[self.update_grid, self.update_grid_range_slider] + callbacks
        )

        mark_controls = HBox(
            [
                self.mark_deleted_controls,
                self.mark_completed_contols,
                self.mark_review_controls,
            ]
        )
        mark_controls_minimal = HBox(
            [
                self.mark_deleted_button,
                self.mark_completed_button,
                self.mark_review_button,
            ]
        )

        selection_controls = HBox(
            [select_button, invert_selection_button, unselect_button]
        )
        item_display_controls = [
            decrement_range,
            self.grid_range_slider,
            increment_range,
        ]
        image_view_controls = HBox([self.width_slider, *item_display_controls])
        grid_view_controls = HBox([self.minimal_view_button])
        sorting_controls = HBox([self.similarity_button])
        batch_labelling_controls = HBox(
            [
                self.batch_add_button,
                self.batch_remove_button,
            ]
        )
        review_controls = HBox(
            [
                refresh_review_modified_button,
                refresh_view_selected_button,
                refresh_review_completed_button,
                refresh_review_review_button,
                refresh_review_deleted_button,
            ]
        )

        mark_controls.layout = CSS_LAYOUTS.flex_layout
        mark_controls_minimal.layout = CSS_LAYOUTS.flex_layout
        selection_controls.layout = CSS_LAYOUTS.flex_layout
        image_view_controls.layout = CSS_LAYOUTS.flex_layout
        grid_view_controls.layout = CSS_LAYOUTS.flex_layout
        sorting_controls.layout = CSS_LAYOUTS.flex_layout
        batch_labelling_controls.layout = CSS_LAYOUTS.flex_padded
        review_controls.layout = CSS_LAYOUTS.flex_layout

        self.REVIEW_TAB = widgets.VBox(
            [
                review_controls,
                CSS_SPACERS.vspace(10),
                mark_controls_minimal,
                CSS_SPACERS.vspace(5),
                selection_controls,
                CSS_SPACERS.vspace(5),
                self.info,
                HBox(
                    [self.width_slider, *self.review_grid_display_controls],
                    layout=CSS_LAYOUTS.flex_layout,
                ),
                CSS_SPACERS.vspace(5),
                batch_labelling_controls,
                self.review_grid,
            ]
        )

        (
            self.refresh_total_labels_stats,
            self.refresh_filtered_labels_stats,
            self.refresh_selected_labels_stats,
            self.refresh_active_datapoints_stats,
            self.refresh_review_datapoints_stats,
        ) = self.generate_refresh_stats_button(callbacks=[])
        self.stats_controls = VBox(
            [
                self.stats_source_button,
                HBox(
                    [
                        self.refresh_total_labels_stats,
                        self.refresh_filtered_labels_stats,
                        self.refresh_selected_labels_stats,
                        self.refresh_active_datapoints_stats,
                        self.refresh_review_datapoints_stats,
                    ]
                ),
            ]
        )
        self.stats_controls.layout = CSS_LAYOUTS.flex_layout_col

        STATS_TAB = VBox(
            [
                HBox([self.stats_controls]),
                self.stats_output_area,
            ]
        )

        # refresh_export_button.click()
        refresh_export_button_centered = HBox([refresh_export_button])
        refresh_export_button_centered.layout = CSS_LAYOUTS.flex_layout
        EXPORT_TAB = VBox(
            [
                refresh_export_button_centered,
                self.export_area,
            ]
        )

        if self.empty_metadata:
            self.metadata_filtering_controls.layout = CSS_LAYOUTS.empty

        # fmt: off
        MAIN_CONTROLS = widgets.VBox(
            [
                self.class_map_filtering_controls, CSS_SPACERS.vspace(5),
                self.metadata_filtering_controls,  CSS_SPACERS.vspace(5),
                image_view_controls, CSS_SPACERS.vspace(10),
                mark_controls,       CSS_SPACERS.vspace(10),
                selection_controls,  CSS_SPACERS.vspace(2),
                sorting_controls,    CSS_SPACERS.vspace(2),
                grid_view_controls,  CSS_SPACERS.vspace(5),
                batch_labelling_controls,
            ]
        )

        MAIN_TAB = widgets.VBox(
            [
                MAIN_CONTROLS,
                self.info,
                self.grid,             CSS_SPACERS.vspace(20),
                mark_controls_minimal, CSS_SPACERS.vspace(5),
                HBox(item_display_controls, layout=CSS_LAYOUTS.flex_layout),
            ]
        )
        # fmt: on

        RESTORE_TAB = widgets.VBox(
            [
                self.info,
                self.restore_button_group.view,
            ]
        )

        self.view = widgets.Tab(
            [
                MAIN_TAB,
                self.REVIEW_TAB,
                STATS_TAB,
                EXPORT_TAB,
                RESTORE_TAB,
            ]
        )

        self.view.set_title(0, "Main Labelling")
        self.view.set_title(1, "Review")
        self.view.set_title(2, "Stats")
        self.view.set_title(3, "Export")
        self.view.set_title(4, "Restore")

        # Define behavior when tabs are changed
        def swap_selection_source(*args):

            if self.view.selected_index == 0:
                self.selection_source = "active_datapoints"
            if self.view.selected_index == 1:
                self.selection_source = "review_datapoints"

            self.update_info()

        self.view.observe(swap_selection_source, "selected_index")


from scipy import spatial


class FeatureEmbeddedDataset(ClassificationDataset, EmbeddingSimilarityMixin):
    def __init__(
        self,
        df,
        batch_size: int = 50,
        width: int = 25,
        class_map: Optional[ClassMap] = None,
        additional_classes: Optional[List[str]] = [],
        embedding_colname: Union[str, List[str]] = "extracted_features",
        embedding_similarity_metric=spatial.distance.cosine,
        label_col: str = "label",
        is_multilabel: bool = False,
    ):
        if isinstance(embedding_colname, str):
            embedding_colname = [embedding_colname]
        self.embedding_colname = embedding_colname
        self.embedding_similarity_metric = embedding_similarity_metric

        super().__init__(
            df=df,
            batch_size=batch_size,
            width=width,
            label_col=label_col,
            class_map=class_map,
            additional_classes=additional_classes,
            is_multilabel=is_multilabel,
        )

    @classmethod
    def from_labelled_file_collection(cls):
        raise NotImplementedError

    @classmethod
    def from_unlabelled_file_collection(cls):
        raise NotImplementedError

    def setup(self):
        super().setup()
        self.setup_similarity()


# tmp backward compat
CinemaNetDataset = FeatureEmbeddedDataset
