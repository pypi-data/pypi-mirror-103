import os
import datetime
import pickle
import json
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from src.utils.utils import get_roc_curves
from sklearn.pipeline import Pipeline


class Experiment:
    """
    NOTE: поддерживатся только алгоритмы классификации
    TODO: создать отдельные классы-наследники для работы с регрессией ИЛИ
    отдельный класс для сохранение метрик

    Класс для запуска экспериментов и сохранения артефактов модели на диск.
    Каждый запуск порождает отдельную подпапку с таймстемпом в папке
    с названием эксперимента
    Сохраняет json-файл с метриками, график ROC-AUC в png, модель и самого себя в pickle
    и обучающую выборку в pickle (отдельно предикторы и таргет)

    Класс пытается найти файл с переменными окружения `.env` и найти там переменную
    `PROJECT_DIR` - рекомендуется создать такой файл в корне папки с проектом

    Основной метод - `run`, но есть доступ к `fit/predict` модели
    Параметры:
    ----------

        name : str
                Название эксперимента, определяет родительскую папку, куда будут
                сохраняться артефакты модели

        target_column : str
                Имя столбца с целевой переменной - сохраняется в файл с метриками

        estimator : Generic
                Модель для применения к данным. На данный момент лучше всего
                протестировано с `sklearn.pipeline.Pipeline`, но должен подойти любой
                класс, поддерживающий `fit/predict`

        proj_dir : str
                Имя корневой директории проекта, если не указана, то предпринимается
                поиск в файле `.env`. Если поиск оказывается не успешным, то корневой
                считается та же директория, из которой запускается скрипт

        subfolder : str
                Название общей папки со всеми экспериментами. Если не указано, то
                устанавливается в значение `models`.
                Папка создается внутри рабочей директории `proj_dir`

        params : dict
                Не используется. Предполагается загрузка гиперпараметров для `estimator`

        random_seed : int
                Инициализация генероторо случайных чисел

    """

    def __init__(self, name, target_column, estimator, proj_dir=None, subfolder=None, params=None, random_seed=0):
        load_dotenv(find_dotenv())
        self.name = name
        self.target_column = target_column
        self.est = estimator
        self.params = params
        self.seed = random_seed
        if proj_dir is None:
            self.proj_dir = Path(os.environ.get("PROJECT_DIR", "."))
        self.subfolder = "models" if subfolder is None else subfolder

    def run(self, X, y, save_to_disk=True, **fit_params):
        self.fit(X, y, **fit_params)
        if save_to_disk:
            self._create_exp_directory()
            self._dump_all(self.exp_dirname)
            self.save_roc_curve(self.exp_dirname)

    def fit(self, X, y, **fit_params):
        self._get_current_time_str()
        self._generate_exp_dirname()
        self._split_data(X, y)
        self.est.fit(self.X_train, self.y_train, **fit_params)
        return self

    def predict(self, X, y=None):
        res = self._predict(X, y)
        return res

    def get_metrics(self):
        self._get_metrics()
        return self.metrics

    def _get_current_time_str(self):
        self.cur_time = str(datetime.datetime.now())[:-7]
        self.cur_time = self.cur_time.replace("-", "").replace(":", "").replace(" ", "_")

    def _generate_exp_dirname(self):
        self.exp_dirname = self.proj_dir / self.subfolder / self.name / self.cur_time

    def _create_exp_directory(self):
        self.exp_dirname.mkdir(parents=True, exist_ok=True)

    def _split_data(self, X, y):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, stratify=y, random_state=self.seed
        )

    def _predict(self, X, y=None):
        return self.est.predict_proba(X)[:, 1]

    def _get_gini_score(self, y_true, y_score):
        roc_auc = roc_auc_score(y_true, y_score)
        gini = np.round(2 * roc_auc - 1, 7)

        return gini

    def _get_train_test_predictions(self):
        self.preds_train = self._predict(self.X_train)
        self.preds_test = self._predict(self.X_test)

    def _get_metrics(self):
        self._get_train_test_predictions()

        try:
            params = self.est.steps[-1][1].get_params()
        except AttributeError:
            params = self.est.get_params()
        self.metrics = {
            "seed": self.seed,
            "target_column": self.target_column,
            "gini_train": self._get_gini_score(self.y_train, self.preds_train),
            "gini_test": self._get_gini_score(self.y_test, self.preds_test),
            "est_algorithm_params": params,
        }

    def save_roc_curve(self, path):
        fname = "roc_curve.png"
        self._get_roc_curve()
        plt.savefig(path / fname)
        plt.close()

    def roc_curve(self):
        self._get_roc_curve()

    def _get_roc_curve(self):
        if not hasattr(self, "metrics"):
            self._get_metrics()
        plt.figure(figsize=(8, 8))
        self.roc_plot = get_roc_curves(
            [self.y_train, self.y_test],
            [self.preds_train, self.preds_test],
            labels=["train", "test"],
        )

    def _dump_all(self, path):
        self._dump_metrics(path)
        self._dump_train_data(path)
        self._dump_estimator(path)
        self._dump_self(path)

    def _dump_metrics(self, path):
        if not hasattr(self, "metrics"):
            self._get_metrics()
        p = path / "metrics.json"
        with open(p, "w") as file:
            json.dump(self.metrics, file, ensure_ascii=True, indent=4)

    def _dump_train_data(self, path):
        for n, d in zip(["X_train", "y_train"], [self.X_train, self.y_train]):
            p = path / (n + ".pkl")
            with open(p, "wb") as file:
                pickle.dump(d, file)

    def _dump_estimator(self, path):
        p = path / ("estimator" + ".pkl")
        with open(p, "wb") as file:
            pickle.dump(self.est, file)

    def _dump_self(self, path):
        p = path / (self.name + "_experiment.pkl")
        with open(p, "wb") as file:
            pickle.dump(self, file)


class ExperimentCatboost(Experiment):
    """
    Класс для уточнения реализации при работе c Catboost[Classifier]
    """

    def fit(self, X, y, save_to_disk=True, **fit_params):
        """
        Дублирует поведение родительского метода fit, но добавляет параметр eval_set

        """
        est_step_name = self.est.steps[-1][0]
        self._get_current_time_str()
        self._generate_exp_dirname()
        self._split_data(X, y)
        fit_params.update({f"{est_step_name}__eval_set": (self.X_test, self.y_test)})
        self.est.fit(self.X_train, self.y_train, **fit_params)

        return self
