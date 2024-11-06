# Parcial Diseño de Sistemas
## Mutant Detector API
Esta API detecta si un humano es mutante en función de su secuencia de ADN. Recibe, mediante un método POST, un array de strings (NxN) que contiene la secuencia de ADN, permitiendo solo las letras {A, T, C, G}. Un humano es identificado como mutante si contiene más de una secuencia de cuatro letras iguales en cualquier dirección: horizontal, vertical u oblicua.
## ¿Como funciona?
Esta api esta hosteada en render y a ella una base de datos Postgres, donde se guardaran los registros de cada secuencia de ADN.
Para realizar el POST, ingresar:
```
https://parcial-ds.onrender.com/mutant
```
Y en el Body especificar un json que tenga el siguiente formato, la secuencia de ADN:
```
{ 
"dna": ["CCAAGA", 
        "CGCCGC", 
        "TTACCG", 
        "ATACCG", 
        "CAATTA", 
        "TAATAG"]
}
```
Para obtener las estadísticas por medio de un metodo GET ingresar:
```
https://parcial-ds.onrender.com/mutant/stats
```
