import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor

#支持向量机回归（SVMR）,核函数默认设置为rbf，C和gamma的范围默认是10的-5至5次方
def SVMR(refle, param, alphas=np.logspace(-5, 5, 11), figure=True):
    parameter = {
        "C": alphas,
        "gamma": alphas,
    }
    clf = GridSearchCV(
        svm.SVR(kernel="rbf"),
        param_grid=parameter,
        cv=10,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
    ).fit(refle, param)
    rmses = np.abs(clf.cv_results_["mean_test_score"]).reshape(len(alphas), len(alphas))
    if figure:
        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(
            go.Contour(x=alphas, y=alphas, z=rmses),
            row=1,
            col=2,
        )
        fig.add_trace(
            go.Scatter(
                x=param,
                y=clf.predict(refle),
                mode="markers",
                marker=dict(color="black", symbol=100),
            ),
            row=1,
            col=1,
        )
        fig.update_xaxes(type="log", row=1, col=2)
        fig.update_yaxes(type="log", row=1, col=2)
        fig.update_layout(height=400, width=900, template="simple_white")
        fig.show()
    return clf, rmses


#随机森林回归（RF），决策树数量默认是100至600
def RF(refle, param, alphas=np.arange(100, 301, 10), figure=True):
    clf = GridSearchCV(
        RandomForestRegressor(random_state=42),
        param_grid={"n_estimators": alphas},
        cv=10,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
    ).fit(refle, param)
    rmses = np.abs(clf.cv_results_["mean_test_score"])
    rf = RandomForestRegressor(n_estimators=clf.best_params_["n_estimators"], random_state=42).fit(
        refle, param
    )
    if figure:
        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(
            go.Scatter(x=alphas, y=rmses, mode="lines", line_color="black"),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=param,
                y=rf.predict(refle),
                mode="markers",
                marker=dict(color="black", symbol=100),
            ),
            row=1,
            col=2,
        )
        fig.update_layout(height=400, width=900, template="simple_white",showlegend=False)
        fig.show()
    return rf, rmses


#AdaBoosting回归（ADAB），默认100至300棵决策树
def ADAB(refle, param, alphas=np.arange(100, 301, 10), figure=True):
    clf = GridSearchCV(
        AdaBoostRegressor(random_state=42),
        param_grid={"n_estimators": alphas},
        cv=10,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
    ).fit(refle, param)
    rmses = np.abs(clf.cv_results_["mean_test_score"])
    adab = AdaBoostRegressor(n_estimators=clf.best_params_["n_estimators"], random_state=42).fit(
        refle, param
    )
    if figure:
        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(
            go.Scatter(x=alphas, y=rmses, mode="lines", line_color="black"),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=param,
                y=adab.predict(refle),
                mode="markers",
                marker=dict(color="black", symbol=100),
            ),
            row=1,
            col=2,
        )
        fig.update_layout(height=400, width=900, template="simple_white",showlegend=False)
        fig.show()
    return adab, rmses



#Gradient Boosting Decision Tree回归（GBDT），默认决策树100至300棵
def GBDT(refle, param, alphas=np.arange(100, 301, 10), figure=True):
    clf = GridSearchCV(
        GradientBoostingRegressor(random_state=42),
        param_grid={"n_estimators": alphas},
        cv=10,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
    ).fit(refle, param)
    rmses = np.abs(clf.cv_results_["mean_test_score"])
    gbdt = GradientBoostingRegressor(n_estimators=clf.best_params_["n_estimators"], random_state=42).fit(
        refle, param
    )
    if figure:
        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(
            go.Scatter(x=alphas, y=rmses, mode="lines", line_color="black"),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=param,
                y=gbdt.predict(refle),
                mode="markers",
                marker=dict(color="black", symbol=100),
            ),
            row=1,
            col=2,
        )
        fig.update_layout(height=400, width=900, template="simple_white",showlegend=False)
        fig.show()
    return gbdt, rmses