import torch
import numpy as np
import pandas as pd
from sklearn import preprocessing
import math


class Regressor():
    def __init__(self, x, nb_epoch=100, learning_rate=0.01):
        X, _ = self.preprocessor(x, training=True)

        self.input_size = X.shape[1]
        self.output_size = 3
        self.nb_epoch = nb_epoch

        self.model = torch.nn.Linear(self.input_size, self.output_size)
        self.criterion = torch.nn.MSELoss()
        self.optimiser = torch.optim.SGD(self.model.parameters(), lr=learning_rate)
        return

    def preprocessor(self, x, y=None, training=False):
        # Convert dataframes to numpy ndarrays
        x = x.to_numpy()
        if isinstance(y, pd.DataFrame):
            y = y.to_numpy()

        # If training extract minmax values
        if training:
            self.x_max = x.max(axis=0)
            self.x_min = x.min(axis=0)
            if isinstance(y, np.ndarray):
                self.y_max = y.max(axis=0)
                self.y_min = y.min(axis=0)

        # Normalise values using MinMax normalisation
        x = (x - self.x_min) / (self.x_max - self.x_min)
        # Currently, normalising y as this should help during training - remember to convert back!
        if isinstance(y, np.ndarray):
            y = (y - self.y_min) / (self.y_max - self.y_min)

        # Return preprocessed x and y, return None for y if it was None
        return x, (y if isinstance(y, np.ndarray) else None)

    def fit(self, x, y):
        X, Y = self.preprocessor(x, y=y, training=True)

        batch_size = 5
        batches = math.ceil(len(X) / batch_size)

        for epoch in range(self.nb_epoch):
            indices = np.random.permutation(len(X))
            X = X[indices]
            Y = Y[indices]

            for i in range(batches):
                start = i * batch_size
                if i < batches - 1:
                    end = (i + 1) * batch_size
                else:
                    end = len(X)

                x_train_tensor = torch.from_numpy(X[start:end]).float()
                y_train_tensor = torch.from_numpy(Y[start:end]).float()

                x_train_tensor.requires_grad_(True)
                self.optimiser.zero_grad()
                y_hat = self.model(x_train_tensor)
                loss = self.criterion(y_hat, y_train_tensor)
                loss.backward()
                self.optimiser.step()

            print(f"Epoch: {epoch}\t L: {loss:.4f}")
        return self

    def predict(self, x):
        X, _ = self.preprocessor(x, training=False)  # Do not forget
        with torch.no_grad():
            x_test = torch.from_numpy(X).float()
            p = self.model(x_test).numpy()
        # rescale predictions to convert back to standard form
        p = p * (self.y_max - self.y_min) + self.y_min
        return p

    def score(self, x, y):
        predictions = self.predict(x)
        y = y.to_numpy()
        mse = np.mean((predictions - y) ** 2)
        rmse = np.sqrt(mse)
        return rmse


def read_data():
    dataset = pd.read_csv("dataset_all_columns.csv")
    dataset = dataset.fillna(dataset.mean())
    print(dataset[10:15])
    return dataset


def run_pipeline(dataset):
    x_train = dataset.drop(["STAI1", "STAI2", "Pittsburgh", "Daily_stress"], axis=1)
    y_train = dataset[["STAI2", "Pittsburgh", "Daily_stress"]]

    regressor = Regressor(x_train)
    regressor.fit(x_train, y_train)

    error = regressor.score(x_train, y_train)
    print("\nRegressor error: {}\n".format(error))


if __name__ == "__main__":
    data = read_data()
    run_pipeline(data)
