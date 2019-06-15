#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd 
from itertools import combinations, combinations_with_replacement
    
    
class Inter_Annotator_Agreement:
    
    def __init__(self, frames, annotation_col, annotators_names, verbose=False):
        
        if len(frames) < 2:
            print('Cannot calculate scores with less than 2 frames.')
        
        self.verbose = verbose
        self.col = annotation_col
        self.ann_names = annotators_names 
        self.frames = frames
        self.m = len(frames) # number of annotators
        self.n = frames[0].shape[0] # number of anootations
        self.categories = self.get_categories()
        self.contingency_table = pd.crosstab(self.frames[0][self.col], \
                                             self.frames[1][self.col], \
                                             rownames=['annotator 1'], \
                                             colnames=['annotator 2'])
        self.agreement_table = self.get_agreement_table()
        
        
    def get_categories(self):
        
        categories_list = []
        
        for frame in self.frames:
            unique_values = frame[self.col].unique()
            unique_values = list(filter(lambda v: v==v, unique_values))
            for label in unique_values:
                
                if label not in categories_list:
                    categories_list.append(label)
        
        categories = list(set(categories_list))
        
        return categories
        
    def get_agreement_table(self):
        
        table = pd.DataFrame(0, index=self.frames[0].index, columns=self.categories)
        
        for i in table.index:
            
            for cat in self.categories:
                count = 0
                
                for frame in self.frames:
                    val = frame.loc[i,self.col]
                    
                    if val==cat:
                        count+=1
                
                table.at[i,cat] += count
                
        return table
    
    
    def Fleiss_overall_agreement(self):
        
        sum_agreements = self.agreement_table*(self.agreement_table-1)
        
        P_o = sum_agreements.values.sum()/(self.n*self.m*(self.m-1))
        
        if self.verbose:
            print('Fleiss overall agreement: %.2f'%P_o)
        
        return P_o
    
    
    def Fleiss_expected_random_agreement(self):
        
        P_j = self.agreement_table.sum()/(self.m*self.n) # marginals of each category 
        
        P_e = sum(P_j**2)
        
        if self.verbose:
            print('Marginals for each category: \n', P_j)
            print('Fleiss expected random agreement: %.2f'%P_e)
        
        return P_e
    
    
    def Fleiss_K(self):
        
        P_o = self.Fleiss_overall_agreement()
        
        P_e = self.Fleiss_expected_random_agreement()
        
        K = (P_o - P_e)/(1 - P_e)
        
        if self.verbose:
            print('Fleiss K score: %2f'%K)
        
        return K
    
    
    def Choen_overall_agreement(self,frames=None):
        
        if frames is None:
            
            true_positive_sum = sum([self.contingency_table.values[i][i] \
                                     for i in range(self.contingency_table.shape[0])])
        
        else:
            
            contingency_table = pd.crosstab(frames[0][self.col], \
                                             frames[1][self.col], \
                                             rownames=['annotator 1'], \
                                             colnames=['annotator 2'])
            
            true_positive_sum = sum([contingency_table.values[i][i] \
                                     for i in range(contingency_table.shape[0])])
            
        P_o = true_positive_sum / self.n
        
        if self.verbose:
            print('Contingecy table: \n', self.contingency_table)
            print('Choen overall agreement: %.2f'%P_o)
        
        return P_o
    
    
    def Choen_expected_random_agreement(self,frames=None):
        
        if frames is None:
            
            marginals_rows = self.contingency_table.sum(axis=1) / self.n
            marginals_cols = self.contingency_table.sum() / self.n
        
        else:
            
            contingency_table = pd.crosstab(frames[0][self.col], \
                                             frames[1][self.col], \
                                             rownames=['annotator 1'], \
                                             colnames=['annotator 2'])
            
            marginals_rows = contingency_table.sum(axis=1) / self.n
            marginals_cols = contingency_table.sum() / self.n
            
        P_e = sum(marginals_rows*marginals_cols)
        
        if self.verbose:
            print('Choen expected random agreement: %.2f'%P_e)
            
        return P_e
    
    
    def Choen_K(self,frames=None):
        
        P_o = self.Choen_overall_agreement(frames=frames)
        
        P_e = self.Choen_expected_random_agreement(frames=frames)
        
        K = (P_o-P_e) / (1-P_e)
        
        if self.verbose:
            print('Choen K score: %.2f'%K)
        
        return K
    
    
    def Light_K(self):
        
        Choen_K_scores = []
        
        for pair in combinations(self.frames,2):
            
            K_score = self.Choen_K(frames=pair)
            
            Choen_K_scores.append(K_score)
            
        K = np.mean(Choen_K_scores)
        
        return K
    
    # Krippendorff alpha stuff
    
    def relaiability_matrix(self):
        
        matrix = pd.DataFrame()
        
        for ind, frame in enumerate(self.frames):
            matrix[self.ann_names[ind]] = frame[self.col]
            
        return matrix
    
    # ratio metric
    def ratio_metric(self,a,b):
        
        if a!=b:
            return ((a-b)/(a+b))**2
        else:
            return 0
        
    # nominal metric
    def nominal_metric(self,a,b):
        
        if a!=b:
            return 1
        else:
            return 0
    
    
    ## ordinal metric
    def ordinal_metric(self, a,b,marginals):
    
        if a!=b:
            sum_marginals = sum(marginals[(a+1):b])
            avg_marginals = (marginals[a]+marginals[b])/2
            return (sum_marginals+avg_marginals)**2
        else:
            return 0
        
    # interval metric
    def interval_metric(self, a,b):
        
        if a!=b:
            return (a-b)**2
        else:
            return 0
        
    
    # works in degrees! To convert to radiance just replace 180 with pi
    def circular_metric(self, a,b,tot):
        
        if a!=b:
            return np.sin(180*((a-b)/tot))
        else:
            return 0
        
    # create matrix of squared distances between each pair of points 
    def get_metric_table(self, length, metric, marginals=None):
        
        metric_matrix = np.zeros((length,length))
        
        for i in range(length):
            for j in range(length):
                if metric == 'interval':
                    metric_matrix[i][j] = self.interval_metric(i,j)
                elif metric == 'nominal':
                    metric_matrix[i][j] = self.nominal_metric(i,j)
                elif metric == 'ordinal':
                    metric_matrix[i][j] = self.ordinal_metric(i,j,marginals)
                elif metric == 'ratio':
                    metric_matrix[i][j] = self.ratio_metric(i,j)
                elif metric == 'circular':
                    metric_matrix[i][j] = self.circular_metric(i,j)
        
        return metric_matrix
    
    # table of expected combinations observations 
    def get_expected_table(self, margins):
        
        length = len(margins)
        e_table = np.zeros((length,length))
        
        for i in range(length):
            for j in range(length):
                
                e_table[i][j] = margins.values[i]*margins.values[j]
        
        return e_table
    
    # table of shape [possible pairs of labels] * num_units 
    # each element is the number of possible pairs calculated based
    # on the annotations of each unit 
    def combinations_table(self):
        
        agree = self.agreement_table
        pairs_labels = combinations_with_replacement(self.categories,2)
        pairs_labels = [(c[0],c[1]) for c in pairs_labels]
        comb_table = pd.DataFrame(index=agree.index, columns=pairs_labels)
        
        for ind, row in agree.iterrows():
            
            count_dict = row[row!=0].to_dict()
            row_pairs = combinations_with_replacement(count_dict.keys(),2)
            row_pairs = [(c[0],c[1]) for c in row_pairs]
            
            for pair in row_pairs:
                
                label1 = pair[0]
                label2 = pair[1]
                
                if label1==label2:
                    tot_count = count_dict[label1]
                    comb_table.loc[ind,pair] = tot_count*(tot_count-1)
                    
                else:
                    count_label1 = count_dict[label1]
                    count_label2 = count_dict[label2]
                    comb_table.loc[ind,pair] = count_label1*count_label2
        
        comb_table.replace(np.nan, 0, inplace=True)
        
        return comb_table
    
    # table of shape [num_labels * num_labels]
    # each value is the sum of observed recording 
    # (over all units) of a specific pair of labels
    def coincidences_matrix(self):
        
        num_categories = len(self.categories)
        matrix = np.zeros([num_categories,num_categories])
        matrix = pd.DataFrame(data=matrix,index=self.categories,columns=self.categories)
        
        comb_table = self.combinations_table()
        
        for ind, row in comb_table.iterrows():
            
            margin = sum(self.agreement_table.loc[ind])
            
            if margin == 1:
                continue
            
            else:
                non_zero_pairs = list(row[row!=0].index)
                non_zero_counts = list(row[row!=0].values)
                
                for ind2, pair in enumerate(non_zero_pairs):
                    
                    label1 = pair[0]
                    label2 = pair[1]
                    
                    if label1==label2:
                        matrix.loc[label1,label2] += non_zero_counts[ind2]/(margin-1)
                    else:
                        matrix.loc[label1,label2] += non_zero_counts[ind2]/(margin-1)
                        matrix.loc[label2,label1] += non_zero_counts[ind2]/(margin-1)
        
        return matrix
    
    
    def Krippendorff_observed_disagreement(self, metric='interval'):
        
        coin_matrix = self.coincidences_matrix()
        margins = coin_matrix.sum(axis=1)
        tot = sum(margins)
        
        length = coin_matrix.shape[0]
        
        if metric != 'ordinal':
            metric = self.get_metric_table(length,metric)
        else:
            metric = self.get_metric_table(length,metric, margins)
        
        d_o = (1/tot)*np.sum(np.sum(coin_matrix*metric))
        
        return d_o, margins
    
    
    def Krippendorff_expected_disagreement(self, margins, metric='interval'):
        
        length = len(margins)
        tot = sum(margins)
        e_table = self.get_expected_table(margins)
        
        if metric != 'ordinal':
            metric = self.get_metric_table(length,metric)
        else:
            metric = self.get_metric_table(length,metric, margins)
            
        d_e = (1/(tot*(tot-1)))*np.sum(np.sum(e_table*metric))
        
        return d_e
    
    def Krippendorff_alpha(self, metric='interval'):
        
        d_o, margins = self.Krippendorff_observed_disagreement(metric)
        d_e = self.Krippendorff_expected_disagreement(margins, metric)
        
        alpha = 1 - (d_o/d_e)
        
        return alpha
