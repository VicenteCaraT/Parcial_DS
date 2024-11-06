# Parcial Diseño de Sistemas
## Mutant Detector API
Esta API (con patron MVC) detecta si un humano es mutante en función de su secuencia de ADN. Recibe, mediante un método POST, un array de strings (NxN) que contiene la secuencia de ADN, permitiendo solo las letras {A, T, C, G}. Un humano es identificado como mutante si contiene más de una secuencia de cuatro letras iguales en cualquier dirección: horizontal, vertical u oblicua.
## ¿Como funciona?
## Opción 1 (docker)
Esta api esta dockerizada por lo cual ingresar:
```
docker compose up
```
Y hacer las pruebas en Postman:
POST:
```
http://127.0.0.1:8000/mutant
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
http://127.0.0.1:8000/mutant/stats
```
## Opción 2 (Render)
Esta api esta hosteada en render y a ella una base de datos Postgres, donde se guardaran los registros de cada secuencia de ADN.
Para realizar el POST, ingresar:
```
https://parcial-ds.onrender.com/mutant
```
Y en el Body:
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

### Alumno: Vicente Cara Tapia
### Legajo: 62089
