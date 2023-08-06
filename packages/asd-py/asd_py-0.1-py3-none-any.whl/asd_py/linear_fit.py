import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import GridSearchCV
from plotly.subplots import make_subplots
import plotly.graph_objects as go


#岭回归（Ridge regression），返回模型及不同alpha的RMSE
def Ridge(refle, param, alphas=np.logspace(-6, 6, 100), figure=True):
    clf = GridSearchCV(
        linear_model.Ridge(),
        {
            "alpha": alphas
        },
        cv=10,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
    ).fit(refle, param)
    rmses = np.abs(clf.cv_results_["mean_test_score"])
    ridge = linear_model.Ridge(alpha=clf.best_params_['alpha']).fit(
        refle, param)
    if figure:
        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(
            go.Scatter(x=alphas, y=rmses, mode="lines", showlegend=False),
            1,
            1,
        )
        fig.add_trace(
            go.Scatter(x=param,
                       y=ridge.predict(refle),
                       mode="markers",
                       showlegend=False),
            1,
            2,
        )
        fig.update_xaxes(title_text="Alpha", type="log", row=1, col=1)
        fig.update_yaxes(title_text="RMSE", row=1, col=1)
        fig.update_xaxes(title_text="Mearued value", row=1, col=2)
        fig.update_yaxes(title_text="Predicted value", row=1, col=2)
        fig.show()
    return ridge, rmses


#套索回归（Lasso regression），返回模型及不同alpha的RMSE
def Lasso(refle, param, alphas=np.logspace(-6, 6, 100), figure=True):
    clf = GridSearchCV(
        linear_model.Lasso(),
        {
            "alpha": alphas
        },
        cv=10,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
    ).fit(refle, param)
    rmses = np.abs(clf.cv_results_["mean_test_score"])
    lasso = linear_model.Lasso(alpha=clf.best_params_['alpha']).fit(
        refle, param)
    if figure:
        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(
            go.Scatter(x=alphas, y=rmses, mode="lines", showlegend=False),
            1,
            1,
        )
        fig.add_trace(
            go.Scatter(x=param,
                       y=lasso.predict(refle),
                       mode="markers",
                       showlegend=False),
            1,
            2,
        )
        fig.update_xaxes(title_text="Alpha", type="log", row=1, col=1)
        fig.update_yaxes(title_text="RMSE", row=1, col=1)
        fig.update_xaxes(title_text="Mearued value", row=1, col=2)
        fig.update_yaxes(title_text="Predicted value", row=1, col=2)
        fig.show()
    return lasso, rmses


#弹性网回归（ElasticNet regression），返回模型及不同alpha的RMSE
def Elastic(refle, param, alphas=np.logspace(-6, 6, 100), figure=True):
    clf = GridSearchCV(
        linear_model.ElasticNet(),
        {
            "alpha": alphas
        },
        cv=10,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
    ).fit(refle, param)
    rmses = np.abs(clf.cv_results_["mean_test_score"])
    elastic = linear_model.ElasticNet(alpha=clf.best_params_['alpha']).fit(
        refle, param)
    if figure:
        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(
            go.Scatter(x=alphas, y=rmses, mode="lines", showlegend=False),
            1,
            1,
        )
        fig.add_trace(
            go.Scatter(x=param,
                       y=elastic.predict(refle),
                       mode="markers",
                       showlegend=False),
            1,
            2,
        )
        fig.update_xaxes(title_text="Alpha", type="log", row=1, col=1)
        fig.update_yaxes(title_text="RMSE", row=1, col=1)
        fig.update_xaxes(title_text="Mearued value", row=1, col=2)
        fig.update_yaxes(title_text="Predicted value", row=1, col=2)
        fig.show()
    return elastic, rmses


#偏最小二乘回归（PLSR）,返回模型及不同隐含因子（Latnet variables, LVs)的RMSE
def PLSR(refle, param, LVs = np.arange(1,31), figure=True):
    clf = GridSearchCV(
        PLSRegression(),
        {"n_components": LVs},
        cv=10,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
    ).fit(refle, param)
    rmses = np.abs(clf.cv_results_["mean_test_score"])
    plsr = PLSRegression(n_components=clf.best_params_['n_components']).fit(refle,param)
    if figure:
        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(
            go.Scatter(x=LVs, y=rmses, mode="lines", showlegend=False),
            1,
            1,
        )
        fig.add_trace(
            go.Scatter(
                x=param, y=plsr.predict(refle).ravel(), mode="markers", showlegend=False
            ),
            1,
            2,
        )
        fig.update_xaxes(title_text="Latnet variables", row=1, col=1)
        fig.update_yaxes(title_text="RMSE", row=1, col=1)
        fig.update_xaxes(title_text="Mearued value", row=1, col=2)
        fig.update_yaxes(title_text="Predicted value", row=1, col=2)
        fig.show()
    return plsr, rmses