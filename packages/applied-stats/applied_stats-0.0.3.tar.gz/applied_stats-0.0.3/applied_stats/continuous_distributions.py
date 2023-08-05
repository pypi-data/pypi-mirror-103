import math as m

import numpy as np
from scipy import integrate
from scipy.special import beta
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

class Norm_rv:

    """
    Class to initialize a normal random variable with mean mu and variance
    sigma^2

    Norm_rv(mean, variance, crit_value=0.0)

    References
    ----------
    [1] Sahoo, Prasanna. "Probability and Mathematical Statistics",
    pp 166 - 169 (2008).
    """

    def __init__(self, mean, variance, crit_value=0.0):
        self.mean = float(mean)
        self.sigma = float(m.sqrt(variance))
        if variance >0 and variance < np.inf:
            self.variance = variance
        else:
            raise ValueError('Enter a variance between 0 and infinity')
        self.crit_value = float(crit_value)
        self.x_range = np.linspace(-4*self.variance, 4*self.variance, 500*self.variance)

    def __repr__(self):
        return f"Normal distribution with mean {self.mean}, variance {self.variance}, and critical value {self.crit_value}"

    def pdf(self):

        """
        this is the probability density function (pdf) of a normal distribution
        with mean mu and variance sigma^2. To check that it is, in fact, a pdf,
        the y values must sum to 1. This would theoretically be the integral
        from -infty to infty but is approximated here with a sum.
        """

        return (1/(self.sigma*m.sqrt(2*m.pi)))*m.e**((-1/2)*((self.x_range-self.mean)/self.sigma)**2)

    def plot_pdf(self, cv_probability=False):

        """
        this function takes a given normal random variable, uses the pdf that
        was previously calculated, and plots it.
        """

        plt.title(self.__repr__())
        plt.plot(self.x_range, self.pdf(),linestyle='dashed', color='blue',linewidth=3)
        if cv_probability==False:
            plt.fill_betweenx(self.pdf(), self.x_range, x2=self.mean,
                          where=(self.x_range<self.mean), color='navy', alpha=0.3)
        else:
            plt.fill_betweenx(self.pdf(), self.x_range, x2=self.crit_value,
                          where=(self.x_range<self.crit_value), color='navy', alpha=0.3)
        plt.tight_layout()
        plt.show()

    def probability_calc(self):

        """
        This calculates the probability to the LEFT of the critical value by
        integrating the area under the distribution from negative infinity
        to the critical value.

        Because the integration function needs a general x variable, and since
        the pdf from Norm_rv.pdf is evaluated over a range of x-values to plot,
        the normal pdf needs to be redefined in this method.This is true for
        all the other distributions as well.
        """

        f = lambda x: (1/(self.sigma*m.sqrt(2*m.pi)))*m.e**((-1/2)*((x-self.mean)/self.sigma)**2)
        self.probability, self.error_est = integrate.quad(f,-np.inf,self.crit_value)
        return f"P(X<crit_val) is {round(self.probability,5)} with an error estimate of {round(self.error_est,5)}"


class ChiSq_rv:

    """
    Class for a Chi-squared random variable with k degrees of freedom

    ChiSq_rv(deg_freedom, crit_value=0.0)

    As degrees of freedom increases to infinity, the Chi-squared distribution
    approximates a normal distribution. You may notice that with >171 degrees of
    freedom, the math.gamma function returns a range error as this is a very
    large number and exceeds the Python-allowed data type limit.

    References
    ----------
    [1] Sahoo, Prasanna. "Probability and Mathematical Statistics",
    pp 392 (2008).
    """

    def __init__(self, df, crit_value=0.0):
        if df > 0:
            self.df = df
        else:
            raise ValueError('Degrees of freedom must be > 0')
        self.mean = self.df
        self.variance = 2*self.df
        self.crit_value = float(crit_value)
        self.x_range = np.linspace(0, 5*self.df, 2000)

    def __repr__(self):
        return f"Chi-squared distribution with {self.df} degrees of freedom and critical value {self.crit_value}"

    def pdf(self):

        """
        this is the probability density function (pdf) of a chi squared
        distribution with k degrees of freedom.To check that it is, in fact,
        a pdf, the y values must integrate to 1.
        """

        #TODO: add integration rather than sum approximation
        return (1/(m.gamma(self.df/2)*2**(self.df/2)))*self.x_range**((self.df/2)-1)*m.e**(-self.x_range/2)


    def plot_pdf(self, cv_probability=False):

        """
        this function takes a given Chi-squared random variable, uses the pdf
        that was previously calculated, and plots it.
        """

        plt.title(self.__repr__())
        plt.plot(self.x_range, self.pdf(),linestyle='dashed', color='red',linewidth=3)
        if cv_probability==False:
            plt.fill_betweenx(self.pdf(), self.x_range, x2=self.df,
                          where=(self.x_range>self.df), color='red', alpha=0.3)
        else:
            plt.fill_betweenx(self.pdf(), self.x_range, x2=self.crit_value,
                          where=(self.x_range>self.crit_value), color='red', alpha=0.3)
        plt.tight_layout()
        plt.show()


    def probability_calc(self):

        """
        This calculates the probability to the RIGHT of the critical value by
        integrating the area under the distribution from the critical value to
        infinity.
        """

        f = lambda x: (1/(m.gamma(self.df/2)*2**(self.df/2)))*x**((self.df/2)-1)*m.e**(-x/2)
        self.probability, self.error_est = integrate.quad(f,self.crit_value,np.inf)
        return f"P(X>crit_val) is {round(self.probability,5)} with an error estimate of {round(self.error_est,5)}"

class t_rv:

    """
    Class for a random variable with a t-distribution and v degrees of freedom

    t_rv(deg_freedom, crit_value=0.0)

    As degrees of freedom increases to infinity, the t distribution approximates
    a standard normal distribution. You may notice that with >171 degrees of
    freedom, the math.gamma function returns a range error as this is a very
    large number and exceeds the Python-allowed data type limit.

    References
    ----------
    [1] Sahoo, Prasanna. "Probability and Mathematical Statistics",
    pp 396 (2008).
    """

    def __init__(self, df, crit_value=0.0):
        if df > 0:
            self.df = df
        else:
            raise ValueError('Degrees of freedom must be > 0')

        if df >= 3:
            self.mean = 0
            self.variance = (self.df / (self.df - 2))
        else:
            raise ValueError('E(X) DNE for df = 1 and Var(X) DNE for df = {1,2}')

        self.crit_value = float(crit_value)
        self.x_range = np.linspace(-2*self.df, 2*self.df, 2000)

    def __repr__(self):
        return f"t distribution with {self.df} degrees of freedom and critical value {self.crit_value}"

    def pdf(self):

        """
        this is the probability density function (pdf) of a t distribution with
        v degrees of freedom. To check that it is, in fact, a pdf, the y values
        must integrate to 1.
        """

        return m.gamma((self.df+1)/2) / (m.sqrt(m.pi * self.df) * m.gamma(self.df / 2) * (1 + ((self.x_range**2)/self.df))**((self.df + 1) / 2))

    def plot_pdf(self, cv_probability=False):

        """
        this function takes a given t random variable, uses the pdf that
        was previously calculated, and plots it.
        """

        plt.title(self.__repr__())
        plt.plot(self.x_range, self.pdf(),linestyle='dashed', color='purple',linewidth=3)
        if cv_probability==False:
            plt.fill_betweenx(self.pdf(), self.x_range, x2=self.df,
                          where=(self.x_range>self.df), color='purple', alpha=0.3)
        else:
            plt.fill_betweenx(self.pdf(), self.x_range, x2=self.crit_value,
                          where=(self.x_range>self.crit_value), color='purple', alpha=0.3)
        plt.tight_layout()
        plt.show()


    def probability_calc(self):

        """
        This calculates the probability to the RIGHT of the critical value by
        integrating the area under the distribution from the critical value
        to infinity.
        """

        f = lambda x: m.gamma((self.df+1)/2) / (m.sqrt(m.pi * self.df) * m.gamma(self.df / 2) * (1 + ((x**2)/self.df))**((self.df + 1) / 2))
        self.probability, self.error_est = integrate.quad(f,self.crit_value,np.inf)
        return f"P(X>crit_val) is {round(self.probability,5)} with an error estimate of {round(self.error_est,5)}"


class F_rv:

    """
    Class for a random variable with an F distribution with v_1 and v_2
    degrees of freedom with x > 0, v_2 >= 5. If v < 5, the Var(X) DNE and if
    v_2 < 3, E(X) DNE.

    F_rv(v_1, v_2, crit_value=0.0)

    As degrees of freedom increases to infinity, the F distribution approximates
    a standard normal distribution. You may notice that as degrees of
    freedom grows large, the math.gamma function returns a range error
    as this is a very large number and exceeds the Python-allowed data type
    limit.

    References
    ----------
    [1] Sahoo, Prasanna. "Probability and Mathematical Statistics",
    pp 401 (2008).
    """

    def __init__(self, v_1, v_2, crit_value=0.0):

        if v_1 >0:
            self.v_1 = v_1
        else:
            raise ValueError('v_1 must be > 0')

        if v_2 >= 5:
            self.v_2 = v_2
            self.mean = self.v_2 / (self.v_2 - 2)
            self.variance = (2*self.v_2**2 * (self.v_1 + self.v_2 -2)) \
                            /((self.v_1)*(self.v_2 - 2)^2 * (self.v_2 -4))
        else:
            if v_2 < 3:
                raise ValueError('with v_2 < 3, E(X) DNE')
            else:
                raise ValueError('with v_2 < 5, Var(X) DNE')

        self.crit_value = float(crit_value)
        self.x_range = np.linspace(0, 2*self.v_2, 2000)

    def __repr__(self):
        return f"""F(v_1,v_2) distribution with v_1={self.v_1} , v_2={self.v_2}
        degrees of freedom, mean {round(self.mean,2)}, and critical value
        {self.crit_value}"""

    def pdf(self):

        """
        this is the probability density function (pdf) of an F distribution with
        v_1 and v_2 degrees of freedom. To check that it is, in fact, a pdf,
        the y values must integrate to 1.
        """

        return (m.gamma((self.v_1 + self.v_2) / 2) * (self.v_1 / self.v_2)**(self.v_1 / 2) * self.x_range**((self.v_1 /2) -1)) \
        / (m.gamma(self.v_1 / 2) * m.gamma(self.v_2 / 2) * (1 + (self.v_1 /self.v_2)*self.x_range)**((self.v_1 + self.v_2) / 2))

    def plot_pdf(self, cv_probability=False):

        """
        this function takes a given F random variable, uses the pdf that
        was previously calculated, and plots it.
        """

        plt.title(self.__repr__())
        plt.plot(self.x_range, self.pdf(),linestyle='dashed', color='forestgreen',linewidth=3)
        if cv_probability==False:
            plt.fill_betweenx(self.pdf(), self.x_range, x2=self.mean,
                          where=(self.x_range>self.mean), color='forestgreen', alpha=0.3)
        else:
            plt.fill_betweenx(self.pdf(), self.x_range, x2=self.crit_value,
                          where=(self.x_range>self.crit_value), color='forestgreen', alpha=0.3)
        plt.tight_layout()
        plt.show()

    def probability_calc(self):

        """
        This calculates the probability to the RIGHT of the critical value by
        integrating the area under the distribution from the critical value
        to infinity.
        """

        f =  lambda x: ((self.v_2**(self.v_2/2) * self.v_1**(self.v_1/2) 
                         * x**(self.v_1/2 -1))/
                        ((self.v_2 +self.v_1*x)**((self.v_1 + self.v_2)/2) * 
                        beta(self.v_1/2, self.v_2/2))) 
        self.probability, self.error_est = integrate.quad(f,self.crit_value,np.inf)
        return f"P(X>crit_val) is {round(self.probability,5)} with an error estimate of {round(self.error_est,5)}"
