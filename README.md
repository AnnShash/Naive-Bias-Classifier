# Naive Bais algorithm
This program is written including the biasing estimate(m-estimate)

P(ai|vj)= (nc + m*p)/(n+m)
where m = constant (eqvlnt sample size)
      p = prior estimate of the prob
      n = no of training examples
      nc = no of ex. for which v = vj and a = ai 
use m = 0 to calculate without using the biasing estimate
