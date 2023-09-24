# Writeup
The formula used by the lcg is $x_n = ax_{n-1} + c \mod m$ <br>
For this reason we also have $x_{n+1} = ax_n + c \mod m$ <br>
We can combine the equations to get:$$
x_{n+1} - x_n = a(x_n - x_{n-1}) \mod m$$
Let $y_n = x_{n+1} - x_n$ so that we have: $y_n = a y_{n-1} \mod m$ or $y_n - ay_{n-1} = 0 \mod m$.
Multiply both sides by $y_n + a y_{n-1}$ and we have:$$\begin{align} &(y_n + a y_{n-1})(y_n - a y_{n-1 }) = 0 \mod m \\
&y_{n}^2 - (a^2 y_{n-1}) y_{n-1} = 0 \mod m \\
&y_{n}^2 - y_{n+1}y_{n-1} = 0 \mod m
\end{align}$$
This is because $a^2 y_{n-1} = y_{n+1} \mod m$.

If we define yet another succession as $t_n = y_{n}^2 - y_{n+1}y_{n-1}$ then we can attempt to calculate the value of $m$ by calculating the gcd of a sufficient number of members of the succession.

Once we have found the value of $m$, calculating the value of $a$ and $b$ is trivial:
- To calculate the value of $a$ we simply have to calculate $a = y_n\cdot(y_{n-1})^{-1} \mod m$. <br>
This is because of the initial relationship $ y_n = a y_{n-1} \mod m$.
- To calculate the value of $c$ we calculate $c = x_n - ax_{n-1} \mod m $.

Once everything is known, we can invert the sequence, using the formula: $$x_n = (x_{n+1} - c) \cdot a^{-1} \mod m$$

