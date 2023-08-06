import sciann as sn 
import numpy as np 
from scipy.optimize import fsolve

# x = sn.Variable('x')
# y = sn.Functional('y', x, 2*[10])
# m = sn.SciModel(x, y)

# x_data = np.linspace(0, 1, 100).reshape(-1,1)
# y_data = y.eval(x_data)
# y_data_2 = y.eval(m, x_data)

# print(x_data.shape, y_data.shape, y_data_2.shape)

M = np.random.uniform(0, 1, (10,10))
x0 = np.random.uniform(0, 1, (11,))
r = np.zeros(11)
r[-1] = 1


def func(xs, *args):
    x = xs[:-1] 
    l = xs[-1]
    return 0.5*np.matmul(M,x).dot(x) + l*(np.sum(x) - 1) - r

def jac(xs):
    J = np.zeros([a+1 for a in M.shape])
    J[:-1, :-1] = M
    J[-1, :-1] = 1.
    J[:-1, -1] = 1.
    return J

# xf = fsolve(func, x0, jac)
# print(xf)



from scipy.optimize import Bounds, LinearConstraint, minimize 
bounds = Bounds(np.zeros(10), np.ones(10))
const = LinearConstraint(np.ones(10), 1, 1)
Jac = M

def func2(x):
    return 0.5*np.matmul(M,x).dot(x)

def jac_func2(x):
    return np.matmul(M,x)

def hess_func2(x):
    return M

x0 = np.ones(10)/10
x = minimize(func2, x0, method='trust-constr', jac=jac_func2, hess=hess_func2,
               constraints=[const], bounds=bounds, options={'verbose':0})

print(x.x, x.x.sum())

