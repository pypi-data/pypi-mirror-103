from datawidgets.imports import *
from datawidgets.ui.style import *
from .annoy import *


class AnnoyIndexerMixin:
    def setup_annoy_index(self):
        # Setup dict to store similarity stuff per col
        self.ANNStations = {
            col: {}.fromkeys(["indexer", "button"]) for col in self.embedding_cols
        }

        # Setup ANN similarity
        for col in self.embedding_cols:
            dim = len(self.df[col].iloc[0])

            start = time.time()

            indexer = AnnoyIndexer(
                dimension=dim,
                n_trees=self.embedding_n_trees,
            )
            indexer.build_from_indexed_dataframe(self.df, col)

            time_taken = datetime.timedelta(seconds=time.time() - start)
            self.log(f"Built {col} indexer in {time_taken}")
            self.ANNStations[col]["indexer"] = indexer

    def generate_ANN_buttons(self, callbacks=[]) -> List[Button]:
        buttons = []
        for col in self.embedding_cols:

            button = Button(description=f"Find Neighbors ({col})")
            button.layout.width = "250px"
            button.add_class(CSS_NAMES.ANN_BUTTON)
            button.on_click(
                partial(
                    self.find_nearest_neighbors,
                    indexer=self.ANNStations[col]["indexer"],
                )
            )

            for cb in callbacks:
                button.on_click(cb)

            self.ANNStations[col]["button"] = button
            buttons.append(button)
        return buttons

    def setup_ann_view(self, callbacks=[]):
        self.ann_buttons = self.generate_ANN_buttons(callbacks=callbacks)
        # self.ann_controls = widgets.Accordion(
        #     children=[HBox(children=self.ann_buttons, layout=CSS_LAYOUTS.flex_layout)]
        # )
        # self.ann_controls.set_title(0, "ANN (Nearest Neighbor) Sorting Controls")
        self.ann_controls = HBox(
            children=self.ann_buttons, layout=CSS_LAYOUTS.flex_layout
        )
        self.ann_controls.add_class(CSS_NAMES.ANN_CONTROLS_ACCORDION)

    def find_nearest_neighbors(self, *args, indexer: AnnoyIndexer):
        if len(self.selected_items) > 0:
            ann_indices = indexer.search(
                index=self.selected_items[0].id,
                num_items=len(self.df),
            )
            self.grid_range_slider.value = (0, self.batch_size)
            self.datapoints[ann_indices[0]].unselect()
            self.filter_and_mutate_dataset(ann_indices)
            self.refresh()