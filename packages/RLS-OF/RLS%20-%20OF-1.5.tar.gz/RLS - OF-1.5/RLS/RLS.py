import TRA as TRA
import numpy as np


class RLS():
    def __init__(self, measurement, initial_prediction, compute_Jacobian_and_resid, forward_model, generate_test_data = None, d_param=1e-50,
                 r_param=1e-50,
                 lower_constraint=-np.inf, upper_constraint=np.inf, num_iterations=5):

        self.initial_prediction = np.copy(initial_prediction.reshape((len(initial_prediction), 1)))
        self.num_iterations = num_iterations

        self.compute_Jacobian_and_resid = compute_Jacobian_and_resid
        self.forward_model = forward_model
        self.generate_test_data = generate_test_data

        self.verbose = True

        self.measurement = measurement

        self.gamma = d_param
        self.lam = r_param
        self.J = np.zeros((len(measurement), len(self.initial_prediction)))
        self.residual = np.zeros((len(measurement), 1))

        self.lower_constraint = lower_constraint
        self.upper_constraint = upper_constraint

        self.regularisation_matrix()

    def LS_function(self, predicted):

        residual = self.forward_model(predicted) - self.measurement

        penalty = np.matmul(self.RM, predicted - self.initial_prediction)
        f = 0.5 * np.linalg.norm(residual) ** 2 + 0.5 * self.lam * np.linalg.norm(penalty) ** 2

        return f

    def regularisation_matrix(self):
        RM = np.zeros((len(self.initial_prediction), len(self.initial_prediction)))

        for i in range(0, 9):
            RM[i, i + 1] = 0.5
        for i in range(0, 9):
            RM[i + 1, i] = -0.5
        RM[0, 0] = -1
        RM[0, 1] = 1
        RM[-1, -1] = 1
        RM[-1, -2] = -1
        self.RM = RM
        self.RM_square = np.matmul(np.transpose(self.RM), self.RM)

    def compute_hessian(self, current_estimate):

        self.J, self.residual = self.compute_Jacobian_and_resid(current_estimate)

        self.JT = np.transpose(self.J)
        hess = np.matmul(self.JT, self.J)

        hess_regularised = np.matmul(self.JT, self.J) + self.lam * self.RM_square

        return hess_regularised

    def compute_gradient(self, current_estimate):

        self.JT = np.transpose(self.J)

        grad = np.matmul(self.JT, self.residual) + self.lam * np.matmul(self.RM_square,
                                                                        current_estimate - self.initial_prediction)

        return grad

    def compute_minimum(self):

        LM_algorithm = TRA.Levenberg_Marquart(self.initial_prediction, self.compute_hessian, self.compute_gradient,
                                              self.LS_function, d_param=self.gamma,
                                              lower_constraint=self.lower_constraint,
                                              upper_constraint=self.upper_constraint,
                                              num_iterations=self.num_iterations)

        reconstructed = LM_algorithm.optimisation_main()

        return reconstructed

    def find_reg_param(self):

        number_of_test = 10
        number_of_reg_points = 10
        lam_array = 10 ** (np.linspace(-40, -10, number_of_reg_points))
        reconstructed_profiles = np.zeros((number_of_test, 10, number_of_reg_points))
        measurement_profiles = np.zeros((number_of_test, 10))

        for i in range(0, number_of_test):
            measurement_profile = self.generate_test_data()
            measurement_profiles[i, :] = measurement_profile.reshape((1, 10))

        best_reg = np.zeros((number_of_test, 1))
        print('Finding regularisation parameter')

        for i in range(0, number_of_test):
            print('profile ', i + 1, '/', number_of_test)
            print('*Compute initial output*')
            measurement_FRP = self.forward_model(measurement_profiles[i, :])

            measurement_original = self.measurement
            self.measurement = measurement_FRP
            LM_algorithm = TRA.Levenberg_Marquart(self.initial_prediction, self.compute_hessian, self.compute_gradient,
                                                  self.LS_function, d_param=self.gamma,
                                                  lower_constraint=self.lower_constraint,
                                                  upper_constraint=self.upper_constraint,
                                                  num_iterations=1)

            LM_algorithm.verbose = False

            print('*Compute gradient and Hessian*')
            initial_damping_param = LM_algorithm.gamma
            LM_algorithm.compute_variables()

            error = np.zeros((number_of_reg_points, 1))

            for j in range(0, number_of_reg_points):
                print('lambda = ', lam_array[j])
                LM_algorithm.gamma = initial_damping_param

                self.lam = lam_array[j]

                reconstructed = self.initial_prediction + LM_algorithm.direction()

                reconstructed_profiles[i, :, j] = reconstructed.reshape((1, 10))
                error[j] = np.linalg.norm(
                    reconstructed_profiles[i, :, j].reshape((10, 1)) - measurement_profiles[i, :].reshape(
                        (10, 1))) / np.linalg.norm(
                    measurement_profiles[i, :].reshape((10, 1)))
                lam_s = '%.2f' % np.log10(lam_array[j])
                print('         Lambda exponent= ', lam_s, ' | reg param index ', j + 1, '/', number_of_reg_points,
                      ' | error =', error[j])
                print('--------------------------------------------------------------------------')
                print('--------------------------------------------------------------------------')


            index = np.where(np.min(error) == error)
            best_reg[i] = lam_array[index[0]]
            print('         Lambda best = ', best_reg[i])


        self.measurement = measurement_original
        return best_reg
