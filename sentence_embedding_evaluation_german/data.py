import pandas as pd
import numpy as np
import torch


def get_data_split(n: int,
                   split_ratio: float = 0.2,
                   random_seed: int = 42):
    # set seed for reproducibility
    if random_seed:
        torch.manual_seed(random_seed)
    # random indicies
    idx = torch.randperm(n)
    n_valid = int(n * split_ratio)
    idx_valid = idx[:n_valid]
    idx_train = idx[n_valid:]
    return idx_train, idx_valid


class GermEval17(torch.utils.data.Dataset):
    """ ABSD-Relevance, -Sentiment, -Category
    Examples:
    ---------
    dset = GermEval17(
        preprocesser, "Relevance", test=False,
        early_stopping=True, split_ratio=0.1)
    X_valid, y_valid = dset.get_validation_set()
    n_classes = dset.num_classes()
    dgen = torch.utils.data.DataLoader(
        dset, **{'batch_size': 64, 'shuffle': True, 'num_workers': 6})
    for X, y in dgen: break
    """
    def __init__(self,
                 preprocesser,
                 datafolder: str = "datasets",
                 task: int = 1,
                 test: bool = False,
                 early_stopping: bool = False,
                 split_ratio: float = 0.2,
                 random_seed: int = 42):
        assert task in ["Relevance", "Sentiment", "Category"]
        self.colidx = int(
            ["Relevance", "Sentiment", "Category"].index(task) + 2)

        if task == "Relevance":
            self.labels = [False, True]
        elif task == "Sentiment":
            self.labels = ['negative', 'neutral', 'positive']
        elif task == "Category":
            self.labels = [
                'Image', 'Informationen', 'Connectivity',
                'Auslastung_und_Platzangebot', 'Service_und_Kundenbetreuung',
                'Gastronomisches_Angebot', 'Allgemein', 'Design',
                'Sonstige_Unregelmässigkeiten', 'Gepäck', 'DB_App_und_Website',
                'Atmosphäre', 'Zugfahrt', 'Ticketkauf', 'nan',
                'Reisen_mit_Kindern', 'Barrierefreiheit', 'Sicherheit',
                'Toiletten', 'Komfort_und_Ausstattung']

        # read data
        split = "test" if test else "train"
        data = pd.read_csv(
            f"{datafolder}/germeval17/{split}.tsv", sep="\t").values
        data[:, 4] = [str(s).split(":")[0] for s in data[:, 4]]
        # bad examples to be removed
        idxbad = [i for i, x in enumerate(data[:, 1])
                  if not isinstance(x, str)]
        data = np.delete(data, idxbad, axis=0)

        # preprocess
        self.X = preprocesser(data[:, 1].tolist())
        self.y = torch.tensor(
            [self.labels.index(row[self.colidx]) for row in data])
        # prepare data split
        if early_stopping and split == "train":
            self.indices, self.idx_valid = get_data_split(
                self.X.shape[0], random_seed=random_seed)
        else:
            self.indices = torch.tensor(range(self.X.shape[0]))
            self.idx_valid = None

    def get_validation_set(self):
        if self.idx_valid is not None:
            return self.X[self.idx_valid], self.y[self.idx_valid]
        else:
            return None, None

    def num_classes(self):
        return len(self.labels)

    def num_features(self):
        return self.X.shape[1]

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, rowidx):
        return self.X[self.indices[rowidx]], self.y[self.indices[rowidx]]


class GermEval18(torch.utils.data.Dataset):
    """ OL18A, OL18B
    Examples:
    ---------
    dset = GermEval18(
        preprocesser, "A", test=False,
        early_stopping=True, split_ratio=0.1)
    X_valid, y_valid = dset.get_validation_set()
    n_classes = dset.num_classes()
    dgen = torch.utils.data.DataLoader(
        dset, **{'batch_size': 64, 'shuffle': True, 'num_workers': 6})
    for X, y in dgen: break
    """
    def __init__(self,
                 preprocesser,
                 datafolder: str = "datasets",
                 task: int = 1,
                 test: bool = False,
                 early_stopping: bool = False,
                 split_ratio: float = 0.2,
                 random_seed: int = 42):
        assert task in ["A", "B", "C"]
        self.colidx = int(["A", "B", "C"].index(task) + 1)

        if task == "A":
            self.labels = ['OFFENSE', 'OTHER']
        elif task == "B":
            self.labels = ['PROFANITY', 'INSULT', 'ABUSE', 'OTHER']

        # read data
        split = "test" if test else "train"
        data = pd.read_csv(
            f"{datafolder}/germeval18/{split}.txt", sep="\t").values
        # preprocess
        self.X = preprocesser(data[:, 0].tolist())
        self.y = torch.tensor(
            [self.labels.index(row[self.colidx]) for row in data])

        # prepare data split
        if early_stopping and split == "train":
            self.indices, self.idx_valid = get_data_split(
                self.X.shape[0], random_seed=random_seed)
        else:
            self.indices = torch.tensor(range(self.X.shape[0]))
            self.idx_valid = None

    def get_validation_set(self):
        if self.idx_valid is not None:
            return self.X[self.idx_valid], self.y[self.idx_valid]
        else:
            return None, None

    def num_classes(self):
        return len(self.labels)

    def num_features(self):
        return self.X.shape[1]

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, rowidx):
        return self.X[self.indices[rowidx]], self.y[self.indices[rowidx]]


class GermEval19(torch.utils.data.Dataset):
    """ OL19A, OL19B, OL19C
    Examples:
    ---------
    dset = GermEval19(
        preprocesser, "A", test=False,
        early_stopping=True, split_ratio=0.1)
    X_valid, y_valid = dset.get_validation_set()
    n_classes = dset.num_classes()
    dgen = torch.utils.data.DataLoader(
        dset, **{'batch_size': 64, 'shuffle': True, 'num_workers': 6})
    for X, y in dgen: break
    """
    def __init__(self,
                 preprocesser,
                 datafolder: str = "datasets",
                 task: int = 1,
                 test: bool = False,
                 early_stopping: bool = False,
                 split_ratio: float = 0.2,
                 random_seed: int = 42):
        assert task in ["A", "B", "C"]
        self.colidx = int(["A", "B", "C"].index(task) + 1)

        if task == "A":
            self.labels = ['OFFENSE', 'OTHER']
            fsuf = "12"
        elif task == "B":
            self.labels = ['PROFANITY', 'INSULT', 'ABUSE', 'OTHER']
            fsuf = "12"
        elif task == "C":
            self.labels = ['EXPLICIT', 'IMPLICIT']
            fsuf = "3"

        # read data
        split = "gold" if test else "train"
        data = pd.read_csv(
            f"{datafolder}/germeval19/{split}{fsuf}.txt", sep="\t").values
        # preprocess
        self.X = preprocesser(data[:, 0].tolist())
        self.y = torch.tensor(
            [self.labels.index(row[self.colidx]) for row in data])

        # prepare data split
        if early_stopping and split == "train":
            self.indices, self.idx_valid = get_data_split(
                self.X.shape[0], random_seed=random_seed)
        else:
            self.indices = torch.tensor(range(self.X.shape[0]))
            self.idx_valid = None

    def get_validation_set(self):
        if self.idx_valid is not None:
            return self.X[self.idx_valid], self.y[self.idx_valid]
        else:
            return None, None

    def num_classes(self):
        return len(self.labels)

    def num_features(self):
        return self.X.shape[1]

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, rowidx):
        return self.X[self.indices[rowidx]], self.y[self.indices[rowidx]]


class GermEval21(torch.utils.data.Dataset):
    """ TOXIC, ENGAGE FCLAIM
    Examples:
    ---------
    dset = GermEval21(
        preprocesser, "TOXIC", test=False,
        early_stopping=True, split_ratio=0.1)
    X_valid, y_valid = dset.get_validation_set()
    n_classes = dset.num_classes()
    dgen = torch.utils.data.DataLoader(
        dset, **{'batch_size': 64, 'shuffle': True, 'num_workers': 6})
    for X, y in dgen: break
    """
    def __init__(self,
                 preprocesser,
                 datafolder: str = "datasets",
                 task: str = "TOXIC",
                 test: bool = False,
                 early_stopping: bool = False,
                 split_ratio: float = 0.2,
                 random_seed: int = 42):
        assert task in ["TOXIC", "ENGAGE", "FCLAIM"]
        self.colidx = int(["TOXIC", "ENGAGE", "FCLAIM"].index(task) + 2)

        # read data
        split = "test" if test else "train"
        data = pd.read_csv(f"{datafolder}/germeval21/{split}.csv").values
        # preprocess
        self.X = preprocesser(data[:, 1].tolist())
        self.y = torch.tensor([row[self.colidx] for row in data])

        # prepare data split
        if early_stopping and split == "train":
            self.indices, self.idx_valid = get_data_split(
                self.X.shape[0], random_seed=random_seed)
        else:
            self.indices = torch.tensor(range(self.X.shape[0]))
            self.idx_valid = None

    def get_validation_set(self):
        if self.idx_valid is not None:
            return self.X[self.idx_valid], self.y[self.idx_valid]
        else:
            return None, None

    def num_classes(self):
        return 2

    def num_features(self):
        return self.X.shape[1]

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, rowidx):
        return self.X[self.indices[rowidx]], self.y[self.indices[rowidx]]


class GermEval21vmwe(torch.utils.data.Dataset):
    """ VMWE
    Examples:
    ---------
    dset = GermEval21vmwe(
        preprocesser, test=False,
        early_stopping=True, split_ratio=0.1)
    X_valid, y_valid = dset.get_validation_set()
    n_classes = dset.num_classes()
    dgen = torch.utils.data.DataLoader(
        dset, **{'batch_size': 64, 'shuffle': True, 'num_workers': 6})
    for X, y in dgen: break
    """
    def __init__(self,
                 preprocesser,
                 datafolder: str = "datasets",
                 test: bool = False,
                 early_stopping: bool = False,
                 split_ratio: float = 0.2,
                 random_seed: int = 42):
        # self.labels = ['figuratively', 'literally', 'both', 'undecidable']
        self.labels = ['figuratively', 'literally']

        # read data
        split = "test" if test else "train"
        data = pd.read_csv(
            f"{datafolder}/germeval21vmwe/{split}.tsv", sep="\t").values
        # bad examples to be removed
        idxbad = [i for i, x in enumerate(data[:, 2])
                  if x not in self.labels]
        data = np.delete(data, idxbad, axis=0)

        # preprocess
        self.X = preprocesser(data[:, 3].tolist())
        self.y = torch.tensor([self.labels.index(row[2]) for row in data])

        # prepare data split
        if early_stopping and split == "train":
            self.indices, self.idx_valid = get_data_split(
                self.X.shape[0], random_seed=random_seed)
        else:
            self.indices = torch.tensor(range(self.X.shape[0]))
            self.idx_valid = None

    def get_validation_set(self):
        if self.idx_valid is not None:
            return self.X[self.idx_valid], self.y[self.idx_valid]
        else:
            return None, None

    def num_classes(self):
        return 2

    def num_features(self):
        return self.X.shape[1]

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, rowidx):
        return self.X[self.indices[rowidx]], self.y[self.indices[rowidx]]
