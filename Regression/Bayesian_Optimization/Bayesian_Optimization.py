# coding: utf-8
import numpy as np
import kernel_matrix as km
# import Acquisition_function as af
# import Parameter_Optimization as pm
import matplotlib.pyplot as plt
import copy
from scipy.stats import norm

# class Bayesian_optimization:
#     def __init__(self, n = 2):
#         self.n = n
        
#     def read_data(self):
#         p = 20

#         x = np.random.rand(self.n, p)
#         xx = x[0] + x[1]
#         # A = np.insert( x, 0, [1]* p, axis = 0).T
#         y = (-0.5 - 0.5) * np.random.rand(p) + xx

#         return x, y, A

def truef(x):
    # return np.sin(10*x[0][:]) + np.sin(10*x[1])
    return np.sin(5*x)

def read_data(n = 1):
    p = 5

    x = np.random.rand(n, p)
    max_r = 0.1
    min_r = -0.1
    y = ((max_r - min_r) * np.random.rand(p) + min_r) + np.sin(5*x)#  + np.sin(10*x[1])

    return x.T, y.reshape(-1, 1)

def test_x(n = 1):
    p = 100
    x = np.linspace(0, 1, p).reshape(n, p)
    # x = np.random.rand(n, p)
    return x.T

def hyper_P(x, y, theta, Opt_type, num_i = 100, alpha = 0.01):

    if (Opt_type == "GD"):
        for i in range(num_i):
            theta = theta + alpha* km.Parameter_Optimization.Gradient_Parameter.HyperPara(x, y, theta, "GP")
            theta = copy.deepcopy(np.where(theta <= 1e-6, 1e-6, theta))

            print ("theta >> ")
            print (theta)
    
    # elif (Opt_type == "Adam"):
    #     m = 0
    #     v = 0
    #     Beta_1 = 0.9
    #     Beta_2 = 0.999
    #     eta = 1e-8
    #     eta_fin = 1e-6
    #     i = 0
    #     fin_flag = True

    #     while (i < num_i and fin_flag):
    #         g = km.Parameter_Optimization.Gradient_Parameter.HyperPara(x, y, theta, "GP")

    #         m = Beta_1*m + (1 - Beta_1)*g
    #         v = Beta_2*v + (1 - Beta_2)*g**2
    #         m_prd = (m)/(1 - Beta_1)
    #         v_prd = (v)/(1 - Beta_2)

    #         theta = theta + alpha*(m_prd/(np.sqrt(v_prd) + eta))
    #         theta = copy.deepcopy(np.where(theta <= 1e-6, 1e-6, theta))

    #         print ("theta >> ")
    #         print (theta)

    #         if (np.sqrt(np.sum((g)**2)) < eta_fin):
    #             fin_flag = False

    #         i += 1
    
    elif (Opt_type == "Adam"):
        m = 0
        v = 0
        Beta_1 = 0.9
        Beta_2 = 0.999
        eta = 1e-8
        eta_fin = 1e-6
        # i = 0
        X_len = len(x)

        num_epoch = 50
        batch_size = 20

        # fin_flag = True

        for epoch in range(num_epoch):
            shuffled_index = np.random.permutation(X_len)
            x_shuffled = x[shuffled_index]
            y_shuffled = y[shuffled_index]

            for j in range(0, X_len, batch_size):
                xi = x_shuffled[j: j+batch_size]
                yi = y_shuffled[j: j+batch_size]

                g = km.Parameter_Optimization.Gradient_Parameter.HyperPara(xi, yi, theta, "GP")

                m = Beta_1*m + (1 - Beta_1)*g
                v = Beta_2*v + (1 - Beta_2)*g**2
                m_prd = (m)/(1 - Beta_1)
                v_prd = (v)/(1 - Beta_2)

                theta = theta + alpha*(m_prd/(np.sqrt(v_prd) + eta))
                theta = copy.deepcopy(np.where(theta <= 1e-6, 1e-6, theta))

                # print ("theta >> ")
                # print (theta)

                # if (np.sqrt(np.sum((g)**2)) < eta_fin):
                    # fin_flag = False


    return theta

# def predict_F(x, x_add, theta, kernel_type = "GK", matrix_type = "Diagonal"):
#     K = km.kernel_function.Kernel_matrix(x, x, theta, "GK", "Diagonal")
#     K_inv = np.linalg.inv(K)

#     # x_test = test_x(n)

#     k_star = km.kernel_function.Kernel_matrix(x, x_add, theta, "GK", "Non_Diagonal")
#     k_starstar = km.kernel_function.Kernel_matrix(x_add, x_add, theta, "GK", "Diagonal")

#     mu = k_star.T @ K_inv @ y
#     var = k_starstar - k_star.T @ K_inv @ k_star
#     v = np.diag(np.abs(var)).reshape(-1,1)
    
#     return mu, v

if __name__ == "__main__":
    # Bo = Bayesian_optimization()
    # x, z, A = Bo.read_data()

    n = 1
    x, y = read_data(n)
    # theta = np.array([1.5, 0.7, 0.07])
    np.random.seed(42)
    theta = np.random.randn(3)
    theta = np.where(theta <= 0, -theta, theta)
    # theta = np.array([1.5, 0.7, 0.07])

    # theta = hyper_P(x, y, theta, "GD")
    print("In theta > ")
    theta = hyper_P(x, y, theta, "Adam")


    print ("theta >>")
    print (theta)
    x_test = test_x(n)

    # K = km.kernel_function.Kernel_matrix(x, x, theta, "GK", "Diagonal")
    # K_inv = np.linalg.inv(K)

    # x_test = test_x(n)

    # k_star = km.kernel_function.Kernel_matrix(x, x_test, theta, "GK", "Non_Diagonal")
    # k_starstar = km.kernel_function.Kernel_matrix(x_test, x_test, theta, "GK", "Diagonal")

    # mu = k_star.T @ K_inv @ y
    # var = k_starstar - k_star.T @ K_inv @ k_star
    # v = np.diag(np.abs(var)).reshape(-1,1)

    mu, v = km.kernel_function.predict_F(x, y, x_test, theta, "GK", "Diagonal")

    x_add, y_add = km.Acquisition_function.Gradient_Descent(x, y, theta)

    plt.figure(figsize=(12,8))
    plt.title('The result')
    plt.fill_between(x_test.flatten(), (mu - np.sqrt(v)).flatten(), (mu + np.sqrt(v)).flatten())
    plt.plot(x_test.flatten(), mu , color='red', label='predicted_mean')
    plt.plot(x_add.flatten(), y_add.flatten() , color='blue', label='EI')
    plt.scatter(x.flatten(), y.flatten(), label='traindata')
    plt.plot(x_test.flatten(), truef(x_test.flatten()), label='true_label', color='purple')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.show()