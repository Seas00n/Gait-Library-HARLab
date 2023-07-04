import numpy as np
import matplotlib.pyplot as plt
from gmr import GMM, kmeansplusplus_initialization, covariance_initialization
from gmr.utils import check_random_state
from sklearn.mixture import BayesianGaussianMixture


n_steps = 50
n_demonstrations = 10
sigma = 0.25
mu = 0.5

T = np.linspace(0, 1, n_steps)
ground_truth = np.empty((2, n_steps))
ground_truth[0] = T
ground_truth[1] = T + (1 / (sigma * np.sqrt(2 * np.pi)) *
                       np.exp(-0.5 * ((T - mu) / sigma) ** 2))
fig = plt.figure()
plt.plot(ground_truth[0], ground_truth[1])
plt.show()
random_state = np.random.RandomState()

X = np.empty((2, n_steps, n_demonstrations))
fig = plt.figure()
for i in range(n_demonstrations):
    noisy_sigma = sigma * random_state.normal(1.0, 0.1)
    noisy_mu = mu * random_state.normal(1., 0.1)
    X[0, :, i] = T
    X[1, :, i] = T + (1 / (noisy_sigma * np.sqrt(2 * np.pi)) *
                      np.exp(-0.5 * ((T - noisy_mu) / noisy_sigma) ** 2))
    plt.plot(X[0, :, i], X[1, :, i])
plt.show()

start = np.zeros(2)
goal = np.array([1, 2])
current_start = ground_truth[:, 0]
current_goal = ground_truth[:, -1]
current_amplitude = current_goal - current_start
amplitude = goal - start
ground_truth = ((ground_truth.T - current_start) * amplitude /
                current_amplitude + start).T
fig = plt.figure
plt.plot(ground_truth[0], ground_truth[1])
plt.show()

for i in range(n_demonstrations):
    current_start = X[:, 0, i]
    current_goal = X[:, -1, i]
    current_amplitude = current_goal - current_start
    X[:, :, i] = ((X[:, :, i].T - current_start) *
                  amplitude / current_amplitude + start).T
fig, ax = plt.subplots()
for i in range(n_demonstrations):
    ax.plot(X[0, :, i], X[1, :, i])
X = X.transpose(2, 1, 0)
steps = X[:, :, 0].mean(axis=0)
expected_mean = X[:, :, 1].mean(axis=0)
expected_std = X[:, :, 1].std(axis=0)
ax.plot(steps, expected_mean, linewidth=4)
plt.show()


n_demonstrations, n_steps, n_task_dims = X.shape
X_train = np.empty((n_demonstrations, n_steps, n_task_dims + 1))
X_train[:, :, 1:] = X
t = np.linspace(0, 1, n_steps)
X_train[:, :, 0] = t
X_train = X_train.reshape(n_demonstrations * n_steps, n_task_dims + 1)


random_state = check_random_state(0)
n_components = 4
initial_means = kmeansplusplus_initialization(X_train, n_components, random_state)
initial_covs = covariance_initialization(X_train, n_components)

bgmm = BayesianGaussianMixture(n_components=n_components, max_iter=100).fit(X_train)
gmm = GMM(
    n_components=n_components,
    priors=bgmm.weights_,
    means=bgmm.means_,
    covariances=bgmm.covariances_,
    random_state=random_state)
plt.figure(figsize=(10, 5))
plt.subplot(121)
plt.title("Confidence Interval from GMM")

plt.plot(X[:, :, 0].T, X[:, :, 1].T, c="k", alpha=0.1)

means_over_time = []
y_stds = []
for step in t:
    conditional_gmm = gmm.condition([0], np.array([step]))
    conditional_mvn = conditional_gmm.to_mvn()
    means_over_time.append(conditional_mvn.mean)
    y_stds.append(np.sqrt(conditional_mvn.covariance[1, 1]))
    samples = conditional_gmm.sample(100)
    plt.scatter(samples[:, 0], samples[:, 1], s=1)
means_over_time = np.array(means_over_time)
y_stds = np.array(y_stds)


plt.plot(means_over_time[:, 0], means_over_time[:, 1], c="r", lw=2)
plt.fill_between(
    means_over_time[:, 0],
    means_over_time[:, 1] - 1.96 * y_stds,
    means_over_time[:, 1] + 1.96 * y_stds,
    color="r", alpha=0.5)
plt.show()