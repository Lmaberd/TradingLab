# Split train, test, val (70-15-15). make sure dates are chronological.
# apply walk forward validation

# Fit GARCH to train model and tune on train/test data. Then evaluate on validation set

# use metrics like MSE/MAE against squared returns, QLIKE Loss, log-likelihood on OOS returns