$$
\frac{U}{E} = K\frac{z-a}{z-1}
$$
-------
$$
U(z-1) = E*K(z-a)\\
$$
--------
Dividindo os dois lados por z
--------
$$
U(1-z^{-1}) = E*K(1-a*z^{-1})\\
$$
-------
$$
U-Uz^{-1} = K(E-a*z^{-1}E)\\
$$
-------
$$
U = K(E-a*z^{-1}*E) + Uz^{-1}\\
$$
-------
aplicando a transformada Z inversa
-------
$$
u[k] = K(e[k]- a*e[k-1]) + u[k-1]\\
$$
-------


OUTRO ASSUNTO
controle de v e theta
$$
e_{ang} = \theta_{ref} - \theta
$$
-----
$$
G = (s+a) \\
u_{ang} = G * e_{ang}
$$
------
$$
u_{ang} = e_{ang} *(s+a)
$$
-----
$$
u_{ang} = e_{ang} * s + e_{ang} * a
$$
-----
expandindo a primeira ocorrencia de $e_{ang}$
$$
u_{ang} = (\theta_{ref} - \theta) * s + e_{ang} * a
$$
------
fazendo a distributiva de s
$$
u_{ang} = (\theta_{ref}*s - \theta*s)  + e_{ang} * a
$$
-----
aplicando a transformada inversa de laplace
$$
u_{ang} = (\omega_{ref} - \omega)  + e_{ang} * a
$$
-----
opção 2:
$$
u_{ang} = \dot{e_{ang}}  + e_{ang} * a
$$
------
retangular pra traz
$$
\frac{e_{ang}[k] - e_{ang}[k-1]}{T}
$$
-------
regra trapezoidal
$$
\frac{2}{T}\frac{z-1}{z+1}
$$
-------
$$
der[k] = 2 * \frac{e_{ang}[k] - e_{ang}[k-1]}{T} - der[k-1]
$$