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
    LabellingGridMixin,
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
        self.width = width
        # self.num_deleted = 0

        self.validate_unique_inputs(self.df, self.filename_col)
        self.coerce_string_inputs()

        init_matplotlib_theme()
        self.init_css()
        self.setup()
        self.setup_view()

    def setup_df_marks_and_index(self):
        self.df.reset_index(drop=True, inplace=True)
        self.df["is_selected"] = False
        self.df["is_modified"] = False
        self.df["is_deleted"] = False
        self.df["is_completed"] = False
        self.df["is_under_review"] = False
        self.source_index = self.df.index.copy()

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
    def _check_filter(
        filter_: Union[Sequence[int], np.ndarray, pd.Series]
    ) -> np.ndarray:

        # If boolean
        if isinstance(filter_, pd.Series):
            # Keep only True values if boolean masking
            if isinstance(filter_.iloc[0], (bool, np.bool8, np.bool)):
                filter_ = filter_[filter_]
            return filter_.index.values

        if not isinstance(filter_, np.ndarray):
            filter_ = np.array(filter_)

        if filter_.dtype == np.bool_:
            return np.where(filter_)

        return filter_

    def filter_dataset(self, filter_: Union[Sequence[int], np.ndarray, pd.Series]):
        "Returns a view of `self.df` without any modifications"
        filter_ = self._check_filter(filter_)
        return self.df.loc[filter_]

    def filter_and_mutate_dataset(
        self, filter_: Union[Sequence[int], np.ndarray, pd.Series]
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
        self.setup_df_marks_and_index()
        self.setup_items()
        self.setup_logging()
        self.setup_width_slider()
        self.setup_labelling_grid()
        self.setup_info()

    def __len__(self):
        return len(self.df)

    def get_results(self):
        idxs = [item.id for item in self.datapoints if not item.is_deleted]
        df = self.df.loc[idxs]
        df["notes"] = [
            item.note.value if hasattr(item, "note") else ""
            for item in self.datapoints[df.index.values]
        ]
        return df.reset_index().rename(columns={"index": "id"})

    @property
    def hide_review_filter(self):
        if self.hide_review is True:
            return ~(self.df.is_under_review == True)
        else:  # if self.hide_review is False:
            res = pd.Series(len(self.df) * [True])
            res.index = self.df.index
            return res

    @property
    def hide_completed_filter(self):
        if self.hide_completed is True:
            return ~(self.df.is_completed == True)
        else:  # if self.hide_completed is False:
            res = pd.Series(len(self.df) * [True])
            res.index = self.df.index
            return res

    @property
    def hide_deleted_filter(self):
        if self.hide_deleted is True:
            return ~(self.df.is_deleted == True)
        else:  # if self.hide_deleted is False:
            res = pd.Series(len(self.df) * [True])
            res.index = self.df.index
            return res

    @property
    def mark_filters(self):
        return (
            self.hide_review_filter
            & self.hide_completed_filter
            & self.hide_deleted_filter
        )

    @property
    def modified_filter(self):
        return self.df.is_modified == True

    # TODO: Is it inefficient to have these properties for very large datasets?
    @property
    def selected_names(self):
        return [item.source for item in self.selected_items]

    @property
    def selected_ids(self):
        return [item.id for item in self.selected_items]

    @property
    def num_modified(self):
        return self.df.is_modified.sum()

    @property
    def num_deleted(self):
        return self.df.is_deleted.sum()

    @property
    def num_under_review(self):
        return self.df.is_under_review.sum()

    @property
    def num_completed(self):
        return self.df.is_completed.sum()

    @property
    def num_selected(self):
        num_selected = sum([item.is_selected for item in self.datapoints])
        if hasattr(self, "ann_buttons"):
            if num_selected > 1:
                for button in self.ann_buttons:
                    button.disabled = True
            else:
                for button in self.ann_buttons:
                    button.disabled = False
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
