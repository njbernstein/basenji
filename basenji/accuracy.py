#!/usr/bin/env python

import numpy as np
from scipy.stats import pearsonr, spearmanr

'''
accuracy.py

Accuracy class to more succinctly store predictions/targets and
compute accuracy statistics.
'''

class Accuracy:
    def __init__(self, targets, preds, targets_na=None, loss=None, target_losses=None):
        self.targets = targets
        self.preds = preds
        self.targets_na = targets_na
        self.loss = loss
        self.target_losses = target_losses

        self.num_targets = self.targets.shape[-1]


    def pearsonr(self, log=False, pseudocount=1):
        ''' Compute target PearsonR vector. '''

        scor = np.zeros(self.num_targets)

        for ti in range(self.num_targets):
            if self.targets_na is not None:
                preds_ti = self.preds[~self.targets_na,ti]
                targets_ti = self.targets[~self.targets_na,ti]
            else:
                preds_ti = self.preds[:,ti]
                targets_ti = self.targets[:,ti]
            if log:
                preds_ti = np.log2(preds_ti+pseudocount)
                targets_ti = np.log2(targets_ti+pseudocount)

            pc, _ = pearsonr(targets_ti, preds_ti)
            pcor[ti] = pc

        return pcor


    def r2(self, log=False, pseudocount=1):
        ''' Compute target R2 vector. '''
        r2_vec = np.zeros(self.num_targets)

        for ti in range(self.num_targets):
            if self.targets_na is not None:
                preds_ti = self.preds[~self.targets_na,ti]
                targets_ti = self.targets[~self.targets_na,ti]
            else:
                preds_ti = self.preds[:,ti]
                targets_ti = self.targets[:,ti]
            if log:
                preds_ti = np.log2(preds_ti+pseudocount)
                targets_ti = np.log2(targets_ti+pseudocount)

            tmean = targets_ti.mean(dtype='float64')
            tvar = (targets_ti-tmean).var(dtype='float64')
            pvar = (targets_ti-preds_ti).var(dtype='float64')
            r2_vec[ti] = 1.0 - pvar/tvar

        return r2_vec


    def spearmanr(self):
        ''' Compute target SpearmanR vector. '''

        scor = np.zeros(self.num_targets)

        for ti in range(self.num_targets):
            if self.targets_na is not None:
                preds_ti = self.preds[~self.targets_na,ti]
                targets_ti = self.targets[~self.targets_na,ti]
            else:
                preds_ti = self.preds[:,ti]
                targets_ti = self.targets[:,ti]

            sc, _ = spearmanr(targets_ti, preds_ti)
            scor[ti] = sc

        return scor


################################################################################
# __main__
################################################################################
if __name__ == '__main__':
    main()
