from datawidgets.imports import *
from datawidgets.ui import *
from IPython.display import FileLink


class DownloadModifiedMixin:
    def setup_download_modified(self):
        self.export_area = widgets.Output()

    def prep_download(self, *args, fname: str = None):
        df = self.get_results()
        if fname is None:
            fname = f"__results__{len(df)}-items.csv"
        df.to_csv(fname, index=False)
        link = FileLink(fname, result_html_prefix="<h3> Download Modified Items: </h3>")
        with self.export_area:
            self.export_area.clear_output()
            display(link)
            display(df)

    def generate_export_refresh_button(self, global_callbacks=[]):
        button = Button(description="Refresh Modified Items")
        button.on_click(self.prep_download)
        button.layout = CSS_LAYOUTS.wide_button

        return button


class ViewCompletedMixin:
    _valid_attrs = [
        "is_completed",
        "is_selected",
        "is_under_review",
        "is_modified",
        "is_deleted",
    ]
    review_attr = ""

    def refresh_completed_grid(self, *args):
        self.review_attr = "is_completed"
        self.update_review_grid()

    def generate_review_completed_button(self, global_callbacks=[]):
        button = Button(description="Show All Completed")
        button.on_click(self.refresh_completed_grid)
        button.layout.width = "180px"

        for cb in global_callbacks:
            button.on_click(cb)

        return button


class ViewModifiedMixin:
    def refresh_modified_grid(self, *args):
        # self.review_datapoints = self.get_modified_items()
        self.review_attr = "is_modified"
        self.update_review_grid()

    def generate_review_modified_button(self, global_callbacks=[]):
        button = Button(description="Show All Modified")
        button.on_click(self.refresh_modified_grid)
        button.layout.width = "180px"

        for cb in global_callbacks:
            button.on_click(cb)

        return button


class ViewReviewMixin:
    def refresh_review_grid(self, *args):
        # self.review_datapoints = self.get_review_items()
        self.review_attr = "is_under_review"
        self.update_review_grid()

    def generate_review_review_button(self, global_callbacks=[]):
        button = Button(description="Show All Review")
        button.on_click(self.refresh_review_grid)
        button.layout.width = "180px"

        for cb in global_callbacks:
            button.on_click(cb)

        return button


class ViewDeletedMixin:
    def refresh_deleted_grid(self, *args):
        # self.review_datapoints = self.get_deleted_items()
        self.review_attr = "is_deleted"
        self.update_review_grid()

    def generate_review_deleted_button(self, global_callbacks=[]):
        button = Button(description="Show All Deleted")
        button.on_click(self.refresh_deleted_grid)
        button.layout.width = "180px"

        for cb in global_callbacks:
            button.on_click(cb)

        return button


class ViewSelectedMixin:
    def get_selected_items(self):
        selected_items = []
        for item in self.datapoints:
            if item.is_selected:
                selected_items.append(item)
        return selected_items

    def refresh_selected_grid(self, *args):
        self.review_attr = "is_selected"
        self.update_review_grid()

    def generate_selected_refresh_button(self, global_callbacks=[]):
        button = Button(description="Show All Selected")
        button.on_click(self.refresh_selected_grid)
        button.layout.width = "180px"

        for cb in global_callbacks:
            button.on_click(cb)

        return button


class ReviewMixin(
    ViewModifiedMixin,
    ViewSelectedMixin,
    ViewCompletedMixin,
    ViewReviewMixin,
    ViewDeletedMixin,
):
    def update_review_grid(self, *args):
        if not self.review_attr in self._valid_attrs:
            raise ValueError(
                f"Expected `attr` to be one of {self._valid_attrs}, "
                f"got {self.review_attr} instead"
            )

        items = []
        prev_batch = []
        next_batch = []

        if hasattr(self, "active_datapoints"):
            # prev_batch = [item.source for item in self.active_datapoints]
            prev_batch = [item.id for item in self.review_datapoints]

        next_batch = self.df.index[getattr(self.df, self.review_attr)].values.tolist()

        # For when we have a review slider
        # next_batch = (
        #     self.df[getattr(self.df, self.review_attr)].iloc[start:end].index.tolist()
        # )
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

        self.review_grid.children = [i.view for i in items]
        self.review_datapoints = items

        next_batch.extend([item.id for item in self.active_datapoints])
        for fname in np.setdiff1d(prev_batch, next_batch):
            item = self.datapoints[fname]
            item.unload()

    def setup_review_grid(self):
        self.review_grid = widgets.Box(
            children=[],
            width="100%",
            layout=CSS_LAYOUTS.flex_layout,
        )
        # self.view_selected_button = self.generate_review_refresh_button()
        # self.view_modified_items_button = self.generate_review_modified_button()
        # self.view_completed_items_button = self.generate_review_completed_button()
        # self.view_review_items_button = self.generate_review_review_button()
