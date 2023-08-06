import numpy as np
from scipy.stats import norm


class GeometricBrownianMotion:

    def simulate_path(self, S, mu, sigma, dt, T):
        prev_price = S
        prices = []
        step = 0
        while step < T:
            ds = prev_price*mu*dt + prev_price*sigma*np.random.randn()*np.sqrt(dt)
            prev_price = prev_price+ds
            prices.append((prev_price))
            step += dt
        return prices

    def __init__(self, S, mu, sigma, dt, T):
        self.simulated_path = self.simulate_path(S, mu, sigma, dt, T)


class StochasticVarianceModel:

    def simulate_path(self, S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T):
        prices = []
        price_now = S
        inst_var_now = inst_var
        prev_inst_var = inst_var_now
        step = 0
        while step < T:
            e1 = norm.ppf(np.random.random())
            e2 = e1*rho + np.sqrt(1-(rho**2))*norm.ppf(np.random.random())

            price_now = price_now + (r - div) * price_now * dt + price_now * np.sqrt(prev_inst_var * dt) * e1
            prev_inst_var = inst_var_now
            inst_var_now = prev_inst_var + (alpha - beta*prev_inst_var)*dt + vol_var*np.sqrt(prev_inst_var*dt)*e2

            # Avoid negative cases and floor variance at zero
            if inst_var_now > .0000001:
                pass
            else:
                inst_var_now = .0000001
            prices.append(price_now)
            step += dt
        return prices

    def __init__(self, S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T):
        self.simulated_path = self.simulate_path(S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T)


class MonteCarloCall:

    def simulate_price_gbm(self, strike, n, r, S, mu, sigma, dt, T):
        payouts = []
        for i in range(0, n):
            GBM = GeometricBrownianMotion(S, mu, sigma, dt, T)
            if(GBM.simulated_path[-1] >= strike):
                payouts.append((GBM.simulated_path[-1]-strike)*np.exp(-r*T))
            else:
                payouts.append(0)
        return np.average(payouts)

    def simulate_price_svm(self, strike, n, S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T):
        payouts = []
        for i in range(0, n):
            SVM = StochasticVarianceModel(S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T)
            if(SVM.simulated_path[-1] >= strike):
                payouts.append((SVM.simulated_path[-1]-strike)*np.exp(-r*T))
            else:
                payouts.append(0)
        return np.average(payouts)

    def __init__(self, strike, n, r, S, mu, sigma, dt, T, alpha=None, beta=None, rho=None, div=None, vol_var=None):
        if alpha is None:
            self.price = self.simulate_price_gbm(strike, n, r, S, mu, sigma, dt, T)
        else:
            inst_var = np.sqrt(sigma)
            self.price = self.simulate_price_svm(strike, n, S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T)


class MonteCarloPut:

    def simulate_price_gbm(self, strike, n, r, S, mu, sigma, dt, T):
        payouts = []
        for i in range(0, n):
            GBM = GeometricBrownianMotion(S, mu, sigma, dt, T)
            if(GBM.simulated_path[-1] <= strike):
                payouts.append((strike-GBM.simulated_path[-1])*np.exp(-r*T))
            else:
                payouts.append(0)
        return np.average(payouts)

    def simulate_price_svm(self, strike, n, S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T):
        payouts = []
        for i in range(0, n):
            SVM = StochasticVarianceModel(S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T)
            if(SVM.simulated_path[-1] <= strike):
                payouts.append((strike-SVM.simulated_path[-1])*np.exp(-r*T))
            else:
                payouts.append(0)
        return np.average(payouts)

    def __init__(self, strike, n, r, S, mu, sigma, dt, T, alpha=None, beta=None, rho=None, div=None, vol_var=None):
        if alpha is None:
            self.price = self.simulate_price_gbm(strike, n, r, S, mu, sigma, dt, T)
        else:
            inst_var = np.sqrt(sigma)
            self.price = self.simulate_price_svm(strike, n, S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T)


class MonteCarloBinaryCall:

    def simulate_price_gbm(self, strike, n, payout, r, S, mu, sigma, dt, T):
        payouts = []
        for i in range(0, n):
            GBM = GeometricBrownianMotion(S, mu, sigma, dt, T)
            if(GBM.simulated_path[-1] >= strike):
                payouts.append(payout*np.exp(-r*T))
            else:
                payouts.append(0)
        return np.average(payouts)

    def simulate_price_svm(self, strike, n, payout, S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T):
        payouts = []
        for i in range(0, n):
            SVM = StochasticVarianceModel(S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T)
            if(SVM.simulated_path[-1] >= strike):
                payouts.append(payout*np.exp(-r*T))
            else:
                payouts.append(0)
        return np.average(payouts)

    def __init__(self, strike, n, payout, r, S, mu, sigma, dt, T, alpha=None, beta=None, rho=None, div=None, vol_var=None):
        if alpha is None:
            self.price = self.simulate_price_gbm(strike, n, payout, r, S, mu, sigma, dt, T)
        else:
            inst_var = np.sqrt(sigma)
            self.price = self.simulate_price_svm(strike, n, payout, S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T)


class MonteCarloBinaryPut:

    def simulate_price_gbm(self, strike, n, payout, r, S, mu, sigma, dt, T):
        payouts = []
        for i in range(0, n):
            GBM = GeometricBrownianMotion(S, mu, sigma, dt, T)
            if(GBM.simulated_path[-1] <= strike):
                payouts.append(payout*np.exp(-r*T))
            else:
                payouts.append(0)
        return np.average(payouts)

    def simulate_price_svm(self, strike, n, payout, S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T):
        payouts = []
        for i in range(0, n):
            SVM = StochasticVarianceModel(S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T)
            if(SVM.simulated_path[-1] <= strike):
                payouts.append(payout*np.exp(-r*T))
            else:
                payouts.append(0)
        return np.average(payouts)

    def __init__(self, strike, n, payout, r, S, mu, sigma, dt, T, alpha=None, beta=None, rho=None, div=None, vol_var=None):
        if alpha is None:
            self.price = self.simulate_price_gbm(strike, n, payout, r, S, mu, sigma, dt, T)
        else:
            inst_var = np.sqrt(sigma)
            self.price = self.simulate_price_svm(strike, n, payout, S, mu, r, div, alpha, beta, rho, vol_var, inst_var, dt, T)


class MonteCarloBarrierCall:

    def __init__(self):
        pass


class MonteCarloBarrierPut:

    def __init__(self):
        pass
