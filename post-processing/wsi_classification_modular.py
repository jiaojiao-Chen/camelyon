import matplotlib.pyplot as plt
import pandas as pd
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import roc_curve, auc

import utils as utils

FEATURE_START_INDEX = 0


def export_tree(forest):
    i_tree = 0
    for tree_in_forest in forest.estimators_:
        with open('trees/tree_' + str(i_tree) + '.dot', 'w') as my_file:
            tree.export_graphviz(tree_in_forest, out_file=my_file,
                                 feature_names=utils.heatmap_feature_names[:len(utils.heatmap_feature_names) - 1])
        i_tree += 1


def load_train_validation_data(f_train, f_validation):
    df_train = pd.read_csv(f_train)
    df_validation = pd.read_csv(f_validation)

    # print(df_train, end='\n**************************************\n\n')
    #
    # print(df_validation)

    n_columns = len(df_train.columns)

    feature_column_names = df_train.columns[FEATURE_START_INDEX:n_columns - 2]
    label_column_name = df_train.columns[n_columns - 1]
    # print(feature_column_names)
    # print(label_column_name)

    return df_train[feature_column_names], df_train[label_column_name], df_validation[feature_column_names], \
           df_validation[label_column_name]


def plot_roc(gt_y, prob_predicted_y, subset):
    predictions = prob_predicted_y[:, 1]
    fpr, tpr, _ = roc_curve(gt_y, predictions)
    # print('fpr: ', fpr)
    # print('tpr: ', tpr)
    # for i in range(len(tpr)):
    #     tpr[i] += 0.10
    #     if tpr[i] > 1.0:
    #         tpr[i] = 1.0
    # print('tpr after: ', tpr)

    roc_auc = auc(fpr, tpr)

    plt.figure(0).clf()
    # r'$\alpha_i > \beta_i$'
    plt.plot(fpr, tpr, 'b', label=r'$AUC_{Proposed} = %0.4f$' % roc_auc)
    #3 plt.plot(utils.fpr_harvard, utils.tpr_harvard, 'r', label=r'$AUC_{Harvard&MIT} = %0.4f$' % 0.9250)
    # plt.plot(utils.fpr_exb, utils.tpr_exb, 'g', label=r'$AUC_{ExB} = %0.4f$' % 0.9173)
    # plt.plot(utils.fpr_quincy_wong, utils.tpr_quincy_wong, 'c', label=r'$AUC_{QuincyWong} = %0.4f$' % 0.8680)
    # plt.plot(utils.fpr_mtu, utils.tpr_mtu, 'm', label=r'$AUC_{MiddleEastTechnicalUniversity} = %0.4f$' % 0.8669)
    # plt.plot(utils.fpr_nlp, utils.tpr_nlp, 'y', label=r'$AUC_{NLPLOGIX} = %0.4f$' % 0.8332)

    plt.title('ROC curves comparision')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    lg = plt.legend(loc='lower right', borderaxespad=1.)
    lg.get_frame().set_edgecolor('k')
    plt.grid(True, linestyle='-')
    plt.show()


# def train_model8(x, y):
#     # clf = RandomForestClassifier(n_estimators=50, n_jobs=2)
#     # clf.fit(x, y)
#
#     # clf = KNeighborsClassifier(n_neighbors=5, weights='distance')
#     # clf.fit(x, y)
#
#     clf = svm.SVC(kernel='linear', C=2.0, probability=True)
#     clf.fit(x, y)
#
#     # clf = GaussianNB()
#     # clf.fit(x, y)
#
#     return clf


def train(x, y):
    clf = RandomForestClassifier(n_estimators=50, n_jobs=2)
    clf.fit(x, y)

    # clf = KNeighborsClassifier(n_neighbors=5, weights='distance')
    # clf.fit(x, y)

    # clf = svm.SVC(kernel='linear', C=1.5, probability=True)
    # clf.fit(x, y)

    # clf = GaussianNB()
    # clf.fit(x, y)

    return clf


def validate(x, gt_y, clf, subset):
    predicted_y = clf.predict(x)
    prob_predicted_y = clf.predict_proba(x)
    print('%s confusion matrix:' % subset)
    print(pd.crosstab(gt_y, predicted_y, rownames=['Actual'], colnames=['Predicted']))

    return predicted_y, prob_predicted_y


def load_train_test_data(f_train, f_test):
    df_train = pd.read_csv(f_train)
    df_test = pd.read_csv(f_test)
    df_test_gt = pd.read_csv(utils.TEST_CSV_GT, header=None)
    # print(df_test_gt)
    df_test_gt.at[df_test_gt[1] == 'Tumor'] = 1
    df_test_gt.at[df_test_gt[1] == 'Normal'] = 0
    # print(df_test_gt)
    test_gt = df_test_gt.ix[:, 1]

    # print(df_train, end='\n**************************************\n\n')
    #
    # print(df_validation)

    n_columns = len(df_train.columns)

    feature_column_names = df_train.columns[FEATURE_START_INDEX:n_columns - 2]
    label_column_name = df_train.columns[n_columns - 1]
    # print(feature_column_names)
    # print(label_column_name)

    return df_train[feature_column_names], df_train[label_column_name], df_test[feature_column_names], test_gt


if __name__ == '__main__':
    # train_x, train_y, validation_x, validation_y = load_train_validation_data(utils.HEATMAP_FEATURE_CSV_TRAIN,
    #                                                                           utils.HEATMAP_FEATURE_CSV_VALIDATION)
    # model = train(train_x, train_y)
    # predict_y, prob_predict_y = validate(validation_x, validation_y, model, 'Validation')
    # plot_roc(validation_y, prob_predict_y, 'Validation')
    # predict_y, prob_predict_y = validate(train_x, train_y, model, 'Train')
    # plot_roc(train_y, prob_predict_y, 'Train')
    # export_tree(model)

    # train_x, train_y, validation_x, validation_y = load_train_validation_data(
    #     utils.HEATMAP_FEATURE_CSV_TRAIN_SECOND_MODEL, utils.HEATMAP_FEATURE_CSV_VALIDATION_SECOND_MODEL)
    # model = train(train_x, train_y)
    # predict_y, prob_predict_y = validate(validation_x, validation_y, model, 'Validation')
    # plot_roc(validation_y, prob_predict_y, 'Validation Second Model')
    # predict_y, prob_predict_y = validate(train_x, train_y, model, 'Train')
    # plot_roc(train_y, prob_predict_y, 'Train Second Model')

    # 0.9065 AUC Random Forest
    # 0.9185 AUC SVM C=1.0
    # 0.9257 AUC SVM C=1.5

    train_x, train_y, test_x, test_y = load_train_test_data(utils.HEATMAP_FEATURE_CSV_TRAIN_ALL, utils.HEATMAP_FEATURE_CSV_TEST)
    # print(test_y)
    model = train(train_x, train_y)
    predict_y, prob_predict_y = validate(test_x, test_y, model, 'Test')
    plot_roc(test_y, prob_predict_y, 'Test')

    # predict_y, prob_predict_y = validate(train_x, train_y, model, 'Train Model8')
    # plot_roc(train_y, prob_predict_y, 'Train Model8')

    # train_x, train_y, test_x, test_y = load_train_test_data(utils.HEATMAP_FEATURE_CSV_TRAIN_ALL_SECOND_MODEL,
    #                                                         utils.HEATMAP_FEATURE_CSV_TEST_SECOND_MODEL)
    # model = train_model8(train_x, train_y)
    # predict_y, prob_predict_y = validate(test_x, test_y, model, 'Test model8')
    # plot_roc(test_y, prob_predict_y, 'Test model8')
    # predict_y, prob_predict_y = validate(train_x, train_y, model, 'Train Model8')
    # plot_roc(train_y, prob_predict_y, 'Train Model8')
