# Plot the decision boundary of SVM
from sklearn.svm import SVC
from ailearn.utils import plot_classifier
from sklearn.datasets import make_moons

x, y = make_moons(n_samples=100, noise=0.15, random_state=30)
model = SVC()
plot_classifier(model, x, y, figsize=(12, 8))