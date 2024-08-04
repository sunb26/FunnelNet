# from torch.nn.functional import one_hot
# from torch import tensor, Tensor
# from numpy import ndarray, mean, std, max, min, concatenate
# from scipy.stats import skew, kurtosis


# def feature_aggregate(feature):

#     if not isinstance(feature, ndarray):
#         feature = feature.numpy()

#     feature = feature.reshape(1, -1)
#     mean_features = mean(feature, axis=1)
#     std_features = std(feature, axis=1)
#     max_features = max(feature, axis=1)
#     min_features = min(feature, axis=1)
#     skew_features = skew(feature, axis=1)
#     kurtosis_features = kurtosis(feature, axis=1)

#     aggregated_features = concatenate((
#         mean_features,
#         std_features,
#         max_features,
#         min_features,
#         skew_features,
#         kurtosis_features
#     ))

#     if not isinstance(aggregated_features, Tensor):
#         aggregated_features = tensor(aggregated_features)

#     return aggregated_features


# def one_hot_encoded_y(y):
#     n_classes = len(y.unique())

#     y = one_hot(tensor(y), n_classes)

#     return y


# def one_hot_encoded_df(config, df, one_hot_data):
#     df = df.drop(df.columns[-1], axis=1)
#     df[config["dataset"]["col_names"][2]] = one_hot_data.values.tolist()
#     return df

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import StratifiedKFold


def smote(data, labels, seed):
    print("SMOTEing data...")

    data_reshaped = data.reshape(data.shape[0], -1)

    smote = SMOTE(random_state=seed)

    X_res, y_res = smote.fit_resample(data_reshaped, labels)

    features = X_res.reshape(X_res.shape[0], *data.shape[1:])
    labels = y_res

    print("SMOTEing done.")

    return features, labels


def skf(fold, features, labels, seed):
    cv = StratifiedKFold(n_splits=fold, shuffle=True, random_state=seed)
    folds = cv.split(features, labels)

    return folds
