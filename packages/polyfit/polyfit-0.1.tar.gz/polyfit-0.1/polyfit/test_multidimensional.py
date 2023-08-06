'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

coeffs = np.array([1,-5,1, 1, 1])

N = 1000
x_points = np.linspace(0,4, num = N)
y_points = np.linspace(0,5, num = N)
X_sparse = np.column_stack((x_points, y_points))
#print("X shape: ", X_sparse.shape)
poly = PolynomRegressor(deg = 2)
#D = poly.build_designmatrix(X_sparse)
#print(D.shape)

poly.coeffs_ = coeffs

z_true = poly.predict(X_sparse)
z_noisy = np.random.normal(z_true, 1)
#print(z_true)
#print("data: ", z_noisy)

poly_new = PolynomRegressor(deg = 2)#, regularization='l1', lam = 1e-1)
cons = {0: Constraints(sign='positive'), 1: Constraints(monotonicity='inc')}#, curvature='concave'
poly_new.fit(X_sparse, z_noisy, loss='l2', interactions = True)#, constraints=cons)
pred = poly_new.predict(X_sparse, interactions = True)
D = poly_new.build_designmatrix(X_sparse, interactions = True)
#print("X: ", X_sparse)
#poly = PolynomialFeatures(2, interaction_only = True)
#print("polyfeatures: ", poly.fit_transform(X_sparse))
#print("D: ", D)
#print("D shape: ", D.shape)
#print("pred: ", pred)
est_coeffs = poly_new.coeffs_
print("est. coeeffs: ", est_coeffs)


XX, YY = np.meshgrid(x_points, y_points)

ZZ = np.full_like(XX, est_coeffs[0]) + XX * est_coeffs[1] + XX * XX * est_coeffs[2] +\
    YY * est_coeffs[3] + YY * YY * est_coeffs[4] + XX * YY * est_coeffs[5]
    

fig = plt.figure()
ax = fig.gca(projection='3d')

surf = ax.plot_surface(XX, YY, ZZ, \
                       linewidth=0, antialiased=False)#, cmap=cm.coolwarm

ax.scatter(x_points, x_points, z_noisy, c = 'b', marker='o', zorder = 0)

plt.show()
'''