Constraint PRogramming EXAM Repository

Done with MiniZinc framework for python3














N Queens printed result:

| Model:         | NQueens:       |  Time:         | N. Solutions:  |
| :------------- | :------------- | :------------- | :------------- |
| Raw Model      |  8             | 0.5680 s       | 92             |
| alldiff Model  |  8             | 0.5360 s       | 92             |
| sym Model      |  8             | 0.5649 s       | 12             |
| Raw Model      |  9             | 0.6439 s       | 352            |
| alldiff Model  |  9             | 0.5909 s       | 352            |
| sym Model      |  9             | 0.5460 s       | 46             |
| Raw Model      |  10            | 1.0390 s       | 724            |
| alldiff Model  |  10            | 0.7270 s       | 724            |
| sym Model      |  10            | 0.5870 s       | 92             |
| Raw Model      |  11            | 3.2809 s       | 2680           |
| alldiff Model  |  11            | 1.4690 s       | 2680           |
| sym Model      |  11            | 0.7090 s       | 341            |
| Raw Model      |  12            | 18.0070 s      | 14200          |
| alldiff Model  |  12            | 6.3239 s       | 14200          |
| sym Model      |  12            | 1.6179 s       | 1787           |




| Model:        | Mode:           | NQueens:       |  Time:         | N. Solutions:  |
| :------------ | :-------------  | :------------- | :------------- | :------------- |
| Alldiff       | input_order_min |  10            | 0.5739 s       | 724            |
|               |     + min       |  15            | 0.     s       |                |
|               |                 |  20            | 0.     s       |                |
|               |                 |  30            | 0.     s       |                |
|               |                 |  40            | 0.     s       |                |
|               |                 |  50            | 0.     s       |                |
|               | first_fail      |  10            | 0.6350 s       | 724            |
|               |    +min         |  15            | 293.94 s       | 2279184        |
|               |                 |  20            | timeout        |                |
|               |                 |  30            | timeout        |                |
|               |                 |  40            | timeout        |                |
|               |                 |  50            | timeout        |                |
|               | first_fail      |  10            | 0.     s       |                |
|               |     +rnd        |  15            | 0.     s       |                |
|               |                 |  20            | 0.     s       |                |
|               |                 |  30            | 0.     s       |                |
|               |                 |  40            | 0.     s       |                |
|               |                 |  50            | 0.     s       |                |
|               | domWdeg         |  10            | 0.4729 s       | 724            |
|               |     +min        |  15            | 295.63 s       | 2279184        |
|               |                 |  20            | timeout        |                |
|               |                 |  30            | timeout        |                |
|               |                 |  40            | timeout        |                |
|               |                 |  50            | timeout        |                |
|               | domWdeg         |  10            | 0.5729 s       | 724            |
|               |     +rnd        |  15            | 0.     s       |                |
|               |                 |  20            | 0.     s       |                |
|               |                 |  30            | 0.     s       |                |
|               |                 |  40            | 0.     s       |                |
|               |                 |  50            | 0.     s       |                |
