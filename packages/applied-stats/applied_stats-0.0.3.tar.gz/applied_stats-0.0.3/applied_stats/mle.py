import numpy as np 

"""
"The method of maximum likelihood in a sense picks out of all the possible
values of theta the one most likely to have produced the given observations
x1, x2, ..., xn. " (Sahoo, 2008)

"The rationale behind point estimation is quite simple. When sampling is from
a population described by a pdf or pmf f(x|theta), knowledge of theta yields
knowledge of the entire population." (Casella, Berger, 2017)

Every calculation below assumes that each x from the sample is identical and 
independently distributed (iid)

The code below will calculate the numeric value for a given MLE based 
on the distribution; analytical solutions can be found in the text referenced 
below.

References
----------
[1] Sahoo, Prasanna. "Probability and Mathematical Statistics", 
pp 417 (2008).
[2] Casella, G., Berger, R. L., "Statistical Inference"
Belmont (California): Brooks/Cole Cengage Learning pp 337 (2017) 
"""

#continuous distributions: input data can include any real number

def uniform(X): 
    
    """
    If X ~iid~ U(alpha, beta), that is, both alpha and beta unknown, the MLEs 
    are the 1st and nth order statistics, X(i) and X(n). Thus, the smallest 
    and largest values from the sample. 
    
    Parameters
    ----------
    X : array_like 
    
    Returns: 
    ----------
    uniform_mle : calculated MLE for the uniform distribution 
    
    References 
    ----------
    [1] Sahoo, "Probability and Mathematical Statistics", pp 423
    [2] Tone, MAT 562: Mathematical Statistics notes, U of L
    """
    
    alpha_mle = np.min(X)
    beta_mle = np.max(X)

    return alpha_mle, beta_mle

def exponential(X):
    
    """
    If If x1,x2,...xn ~iid~ EXP(theta) the MLE, theta-hat is X-bar. 
    
    Parameters
    ----------
    X : array_like 
    
    Returns: 
    ----------
    exponential_mle : calculated MLE (theta-hat) the exponential distribution 
    
    References
    ----------
    [1] Sahoo, "Probability and Mathematical Statistics", pp 458
    [2] Tone, MAT 562: Mathematical Statistics notes, U of L
    """

    n = len(X)
    exponential_mle = np.mean(X)
    
    return exponential_mle

def normal(X): 
    
    """
    If x1,x2,...xn ~iid~ N(mu, sigma^2), (both mu and sigma^2 unknown) the MLEs
    are X-bar and (1/n)*sum(x_i - x-bar)^2 from i to n. 
    
    Parameters
    ----------
    X : array_like 
    
    Returns: 
    ----------
    mu_mle, var_mle : a tuple of the MLEs for mu-hat and sigma^2-hat for 
    N(mu, var)
    
    References
    ----------
    [1] Sahoo, "Probability and Mathematical Statistics", pp 422
    [2] Tone, MAT 562: Mathematical Statistics notes, U of L 
    """
    #cleaning calculations 
    X_array = np.array(X) 
    n = len(X_array)
    
    mu_mle = np.mean(X)
    var_mle = (1/n) * np.sum(np.square(X_array - mu_mle))
    
    return mu_mle, var_mle


#discrete distributions: data values MUST countably finite, non-negative ints

def discrete_check(X):
    
    """
    Since the next section of MLEs need to be discrete, this will return True
    if every data point is an integer
    
    Parameters
    ----------
    X : array like 
    
    Returns: 
    ----------
    a : boolean value 
    """

    _int_check = np.equal(np.mod(X,1),0)
    a = np.all(_int_check)
    return a 
    
#discrete MLE calculations 
def bernoulli(X): 
    
    """
    
    If x1,x2,...xn ~iid~ BER(p), then the MLE, p-hat, is X-bar
    
    Parameters
    ----------
    X : array_like 
    
    Returns: 
    ----------
    bernoulli_mle : MLE calculation for p-hat for Bernoulli distribution  
    
    References
    ----------
    [1] Casella, G., Berger, R. L., "Statistical Inference"
    Belmont (California): Brooks/Cole Cengage Learning pp 317-318 (2017) 
    """
    
    _input = np.array(X) 
    n = len(_input)  
    discrete_bool = discrete_check(_input)
    bernoulli_mle = np.mean(X) 
    
    if discrete_bool == True:
        return bernoulli_mle 
    else:
        raise ValueError("X must be a discrete data set (only integers)")

def binomial(X):
    
    #TODO: fix this with k successes 
    
    """
    If x1,x2,...xn ~iid~ BIN(k,p) then the MLE is X-bar, the sample proportion 
    
    Parameters
    ----------
    X : array_like 
    
    Returns: 
    ----------
    binomial_mle : MLE calculation for p-hat for Binomial(k,p)  
    
    References
    ----------
    [1] Casella, G., Berger, R. L., "Statistical Inference"
    Belmont (California): Brooks/Cole Cengage Learning pp 317-318 (2017) 
    """
    
    _input = np.array(X) 
    n = len(_input)  
    discrete_bool = discrete_check(_input)
    binomial_mle = np.mean(X) 
    
    if discrete_bool == True:
        return binomial_mle 
    else:
        raise ValueError("X must be a discrete data set (only integers)")

def geometric(X): 
    
    """
    If x1,x2,...xn ~iid~ GEO(p) then the MLE is 1 / X-bar
    
    Parameters
    ----------
    X : array_like 
    
    Returns: 
    ----------
    geo_mle : MLE calculation for p-hat for GEO(p)  
    
    References
    ----------
    [1] Casella, G., Berger, R. L., "Statistical Inference"
    Belmont (California): Brooks/Cole Cengage Learning (2017) 
    [2] Tone, MAT 562: Mathematical Statistics notes, U of L 
    """
    
    _input = np.array(X) 
    n = len(_input)  
    discrete_bool = discrete_check(_input)
    geo_mle = 1 / np.mean(X)
    
    if discrete_bool == True:
        return geo_mle 
    else:
        raise ValueError("X must be a discrete data set (only integers)") 

def poisson(X):
    
    """
    
    If x1,x2,...xn ~iid~ POIS(lambda) then the MLE is X-bar
    
    Parameters
    ----------
    X : array_like 
    
    Returns: 
    ----------
    poisson_mle : MLE calculation for lambda-hat for POIS(p)  
    
    (Could not find a reference in the texts I was using, so found a derivation
     on the website below)
    
    References
    ----------
    Taboga, M. (n.d.). Poisson distribution - maximum likelihood estimation. 
    Retrieved April 17, 2021, from 
    https://www.statlect.com/fundamentals-of-statistics/
    Poisson-distribution-maximum-likelihood
    """
    
    _input = np.array(X) 
    n = len(_input)  
    discrete_bool = discrete_check(_input)
    poisson_mle = np.mean(X) 
    
    if discrete_bool == True:
        return poisson_mle 
    else:
        raise ValueError("X must be a discrete data set (only integers)") 


    
    
    
    
    
    
    
    