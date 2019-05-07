#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd 
import itertools

class Inter_Annotator_Agreement:
    
    def __init__(self, frames, annotation_col, verbose=False):
        
        if len(frames) < 2:
            print('Cannot calculate scores with less than 2 frames.')
        
        self.verbose = verbose
        self.col = annotation_col
        self.frames = frames
        self.m = len(frames) # number of annotators
        self.n = frames[0].shape[0] # number of anootations
        self.categories = self.get_categories()
        self.contingency_table = pd.crosstab(self.frames[0][self.col], \
                                             self.frames[1][self.col], \
                                             rownames=['annotator 1'], \
                                             colnames=['annotator 2'])
    
    def get_categories(self):
        
        categories_list = []
        
        for frame in self.frames:
            categories_list.append(frame[self.col].unique())
            
        categories = set().union(*categories_list)
        
        return categories
        
    def agreement_table(self):
        
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
        
        table = self.agreement_table()
        
        sum_agreements = table*(table-1)
        
        P_o = sum_agreements.values.sum()/(self.n*self.m*(self.m-1))
        
        if self.verbose:
            print('Fleiss overall agreement: %.2f'%P_o)
        
        return P_o
    
    
    def Fleiss_expected_random_agreement(self):
        
        table = self.agreement_table()
        
        P_j = table.sum()/(self.m*self.n) # marginals of each category 
        
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
        
        for pair in itertools.combinations(self.frames,2):
            
            K_score = self.Choen_K(frames=pair)
            
            Choen_K_scores.append(K_score)
            
        K = np.mean(Choen_K_scores)
        
        return K
    
    
    
    