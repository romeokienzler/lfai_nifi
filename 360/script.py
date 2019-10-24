import sys
import json
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import ClassificationMetric
import pandas as pd
from io import StringIO

#sys.stdout.write(sys.argv[1])
config = json.loads(sys.argv[1].replace('\'','\"'))


# initialize list of lists 
# 0 black
# 1 white
# 0 reject
# 1 accept

df_ground_truth = pd.DataFrame([[0,0], [1,1], [0,1], [1,0], [1,0]], columns = ['protected','label'])
#fair
#df_classifier = pd.DataFrame([[0,0], [1,1], [0,1], [1,1], [1,0]], columns = ['protected','label']) 
#unfair
#df_classifier = pd.DataFrame([[0,0], [1,1], [0,0], [1,1], [1,0]], columns = ['protected','label']) 

input = ''.join(sys.stdin.readlines())
data = StringIO(input)
df_classifier = pd.read_csv(data, sep=",", header=None, names=config['columns'])

privileged_groups=config['privileged_groups']
unprivileged_groups=config['unprivileged_groups']

dataset_ground_truth = BinaryLabelDataset(
    favorable_label=1,
    unfavorable_label=0,
    df=df_ground_truth,
    label_names=config['label_names'],
    protected_attribute_names=config['protected_attribute_names'],
    unprivileged_protected_attributes=unprivileged_groups)

dataset_classifier = BinaryLabelDataset(
    favorable_label=1,
    unfavorable_label=0,
    df=df_classifier,
    label_names=config['label_names'],
    protected_attribute_names=config['protected_attribute_names'],
    unprivileged_protected_attributes=unprivileged_groups)

classificaltion_metric = \
            ClassificationMetric(
                            dataset_ground_truth,
                            dataset_classifier,
                            unprivileged_groups=unprivileged_groups,
                            privileged_groups=privileged_groups)

TPR = classificaltion_metric.true_positive_rate()
TNR = classificaltion_metric.true_negative_rate()
bal_acc_nodebiasing_test = 0.5*(TPR+TNR)

metrics = {
    "classification_accuracy": classificaltion_metric.accuracy(),
    "balanced_classification_accuracy": bal_acc_nodebiasing_test,
    "statistical_parity_difference": classificaltion_metric.statistical_parity_difference(),
    "disparate_impact": classificaltion_metric.disparate_impact(),
    "equal_opportunity_difference": classificaltion_metric.equal_opportunity_difference(),
    "average_odds_difference": classificaltion_metric.average_odds_difference(),
    "theil_index": classificaltion_metric.theil_index(),
    "false_negative_rate_difference": classificaltion_metric.false_negative_rate_difference()
}

sys.stdout.write(json.dumps(metrics))
