We can see that the web app uses AES-CBC to encrypt session data. <br>
We are also given the IV in the base64 encoded json. <br>
For this reason we can perform a bit-flipping attack and login with another username.

The AES-CBC decryption of the i-th block works as follows:
$$P_{k} = D(C_{k}) = \begin{cases} AES^{-1}(C_{k}) \oplus IV & k = 0 \\ AES^{-1}(C_{k}) \oplus C_{k-1} & k > 0 \end{cases}$$
Thus we can change the original $IV$ with a new $IV'$ such that: $$P_{0}' = AES^{-1}(C_{0}) \oplus IV' = \operatorname{pad}(\text{new-username}) $$
Recall that $D(C_0) = AES^{1}(C_0) \oplus IV$ is simply our username (padded). <br>
Now let $IV' = IV \oplus x$ so that we can easily solve for its value:
$$ \begin{align}&\operatorname{pad}(\text{new-username}) = AES^{-1}(C_0) \oplus IV \oplus x = \operatorname{pad}(\text{your-username}) \oplus x \\ & \operatorname{pad}(\text{new-username}) \oplus \operatorname{pad}(\text{your-username}) = x \end{align}$$
At this point we could login as admin but the following lines would block us:
```python
# Admin won't be able to login but whatever
if name == "admin":
    return 'Hacker detected
```
But notice that the code which is querying the database is the following:
```python
tasks = cursor.execute(f"SELECT id, title, content, completed FROM tasks WHERE owner = '{name}'").fetchall()
```
So we can perform a simple sqlinjection by calling ourselves `admin' -- ` and the app will block us no more.