
import pandas as pd
from mlfinlab.portfolio_optimization.estimators import TheoryImpliedCorrelation

def calculating_dirty_correl(stock_returns,weights,tree_classification):

    # Calculating the empirical correlation matrix
    corr_matrix = stock_returns.corr()

    # Calculating the relation of sample length T to the number of variables N
    # It's used for de-noising the TIC matrix
    tn_relation = stock_returns.shape[0] / stock_returns.shape[1]

    # The class that contains the TIC algorithm
    tic = TIC()

    # Calculating the Theory-Implied Correlation matrix
    tic_matrix = tic.tic_correlation(tree_classification, corr_matrix, tn_relation, kde_bwidth=0.01)

    # Calculating the distance between the empirical and the theory-implied correlation matrices
    matrix_distance = tic.corr_dist(corr_matrix, tic_matrix)

    return matrix_distance