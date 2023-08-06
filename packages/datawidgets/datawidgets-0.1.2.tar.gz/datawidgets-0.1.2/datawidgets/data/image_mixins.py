from datawidgets.imports import *
from datawidgets.ui import *
from datawidgets.data.image import *


class NoteMixin:
    def setup_note(self):
        self.note = widgets.Text()
        self.hide_review_note()
        self._setup_note_interaction()

    def hide_review_note(self):
        self.note.placeholder = ""
        self.note.layout = CSS_LAYOUTS.empty
        self.note.remove_class(CSS_NAMES.IMG_NOTE)
        self.note.add_class(CSS_NAMES.IMG_NOTE_HIDDEN)
        self.showing_review_note = False

    def show_review_note(self):
        self.note.placeholder = "Review Note:"
        self.note.layout = CSS_LAYOUTS.flex_layout
        self.note.add_class(CSS_NAMES.IMG_NOTE)
        self.note.remove_class(CSS_NAMES.IMG_NOTE_HIDDEN)
        self.showing_review_note = True

    def _setup_note_interaction(self):
        ""

        def toggle_review_note(*args):
            if self.showing_review_note:
                self.hide_review_note()
            else:
                self.show_review_note()

        self.toggle_note_button = Button(description="🖊️")
        self.toggle_note_button.on_click(toggle_review_note)
        self.toggle_note_button.add_class(CSS_NAMES.TOGGLE_IMG_NOTE_BUTTON)


class ClassificationLabelsMixin:
    """
    Three points where updating of labels happens:
      1. `self.add_label`
      2. `self.remove_label`
      3. when any of `self.label_buttons` is clicked

    The updating logic is defined in `self.update_dataset()`, which is called
    during both (1) and (2), and is passed as a callback to (3) on init
    """

    _works_with = "ImageWithLabels"

    def setup_labelling(self):
        self.label_buttons = ClassificationLabelButtons(
            class_map=self.class_map,
            labels=self._labels,
            callbacks=[
                self.monitor_searchbox_status,
                self.remove_label,
            ],
        )
        self.searchbox = Dropdown(
            options=self.classes + [""],
            value="",
            layout=CSS_LAYOUTS.flex_layout,
        )
        self.searchbox.add_class(CSS_NAMES.LABEL_SEARCH_BOX)
        self.searchbox.observe(self.monitor_searchbox_value)

        self.monitor_searchbox_status()

    @property
    def labels(self):
        return self.label_buttons.labels

    @property
    def max_labels_selected(self):
        if not self.is_multilabel and len(self.labels) == 1:
            return True
        return False

    def monitor_searchbox_status(self, change=None):
        if self.max_labels_selected:
            self.searchbox.disabled = True
        else:
            self.searchbox.disabled = False

    def monitor_searchbox_value(self, change):
        if self.searchbox.value != "" and self.searchbox.value in self.classes:
            self.add_label(self.searchbox.value)

            # empty the searchbox if a full, unique label is entered (and assigned)
            # if sum([l.startswith(self.searchbox.value) for l in self.classes]) == 1:
            #     self.searchbox.value = ""

            self.searchbox.value = ""
        self.monitor_searchbox_status()

    def set_labels(self, labels: List[str]):
        if isinstance(labels, str):
            labels = [str]

        [self.label_buttons.remove(l) for l in self.labels]
        [self.label_buttons.append(l) for l in labels]
        self.update_dataset()

    def update_dataset(self, *args):
        self.is_modified = True
        if self.dset is not None:

            self.dset.df.at[self.id, self.dset.label_col] = self.labels
            self.dset.df.at[self.id, "is_modified"] = self.is_modified
            self.log(f"Altered {self.id}'s labels...?")

            self.dset.update_info()

    def add_label(self, label: str):
        self.label_buttons.append(label)
        self.update_dataset()

    def remove_label(self, label: str):
        self.label_buttons.remove(label)
        self.update_dataset()
