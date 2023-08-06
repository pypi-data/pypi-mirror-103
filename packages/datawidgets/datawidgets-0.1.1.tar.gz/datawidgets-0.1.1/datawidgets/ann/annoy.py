from datawidgets.imports import *
from annoy import AnnoyIndex


class AnnoySimilarityMetrics(Enum):
    Angular = "angular"
    Euclidean = "euclidean"
    Manhattan = "manhattan"
    Hamming = "hamming"
    Dot = "dot"


class AnnoyIndexer:
    """
    Wrapper for Spotify's Annoy
    See https://github.com/spotify/annoy for more details
    """

    def __init__(
        self,
        dimension: int,
        n_trees: int = 10,
        search_k: int = -1,
        metric: AnnoySimilarityMetrics = None,
    ):
        if metric is None:
            metric = AnnoySimilarityMetrics.Euclidean

        if not isinstance(metric, AnnoySimilarityMetrics):
            raise TypeError(
                f"Metric must be of type {SimilarityMetrics}, got {type(metric)} instead"
            )

        self.n_trees = n_trees
        self.search_k = search_k
        self.metric = metric.value
        self.dimension = dimension
        self.indexer = AnnoyIndex(self.dimension, self.metric)

    def build_from_indexed_dataframe(self, df: pd.DataFrame, colname: str):
        "Builds an index from a DataFrame with vectors stored in a column"
        if not isinstance(colname, str):
            raise TypeError(f"Expected {str} `colname`, got {type(colname)}")

        for row in df[[colname]].itertuples(index=True):
            self.indexer.add_item(row[0], row[1])
        self.indexer.build(self.n_trees)

    def search(self, index: int, num_items: int = 100):
        return self.indexer.get_nns_by_item(
            index,
            num_items,
            # searck_k=self.search_k,
        )

    def __repr__(self):
        return f"AnnoyIndex with {self.indexer.get_n_items()} items and {self.indexer.get_n_trees()} trees"