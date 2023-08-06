from datawidgets.imports import *
from ..interface import *
from .image_mixins import *


class MarkAsSelectedMixin:
    def setup_mark_selected(self):
        pass

    def _update_dset_df_selected(self):
        if hasattr(self, "dset"):
            self.dset.df.loc[self.id, "is_selected"] = self.is_selected

    def select(self):
        "Select and add respective CSS class"
        self.is_selected = True
        self.item.add_class(CSS_NAMES.IMG_BOX_SELECTED)
        self._update_dset_df_selected()

    def unselect(self):
        "Unselect and remove respective CSS class"
        self.is_selected = False
        self.item.remove_class(CSS_NAMES.IMG_BOX_SELECTED)
        self._update_dset_df_selected()

    def toggle_selected_status(self):
        if not self.is_selected:
            self.select()
        elif self.is_selected:
            self.unselect()


class MarkAsDeletedMixin:
    def setup_mark_deleted(self):
        pass

    def _update_dset_df_deleted(self):
        if hasattr(self, "dset"):
            self.dset.df.loc[self.id, "is_deleted"] = self.is_deleted

    def mark_as_deleted(self):
        self.unselect()
        self.unmark_as_under_review()
        self.unmark_as_completed()
        self.is_deleted = True
        self.view.add_class(CSS_NAMES.IMG_DELETED)
        self._update_dset_df_deleted()

    def unmark_as_deleted(self):
        self.unselect()
        self.is_deleted = False
        self.view.remove_class(CSS_NAMES.IMG_DELETED)
        self._update_dset_df_deleted()


class MarkAsCompletedMixin:
    def setup_mark_completed(self):
        pass

    def _update_dset_df_completed(self):
        if hasattr(self, "dset"):
            self.dset.df.loc[self.id, "is_completed"] = self.is_completed

    def mark_as_completed(self):
        self.unselect()
        self.is_completed = True
        self.item.add_class(CSS_NAMES.IMG_COMPLETED)
        self._update_dset_df_completed()

    def unmark_as_completed(self):
        self.unselect()
        self.is_completed = False
        self.item.remove_class(CSS_NAMES.IMG_COMPLETED)
        self._update_dset_df_completed()


class MarkAsReviewMixin:
    def setup_mark_review(self):
        pass

    def _update_dset_df_review(self):
        if hasattr(self, "dset"):
            self.dset.df.loc[self.id, "is_under_review"] = self.is_under_review

    def mark_as_under_review(self):
        self.unselect()
        self.is_under_review = True
        self.item.add_class(CSS_NAMES.IMG_IN_REVIEW)
        self._update_dset_df_review()

    def unmark_as_under_review(self):
        self.unselect()
        self.is_under_review = False
        self.item.remove_class(CSS_NAMES.IMG_IN_REVIEW)
        self._update_dset_df_review()