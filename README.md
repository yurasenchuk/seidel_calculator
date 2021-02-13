# seidel_calculator

Seidel calculator - educational project written in Django using Celery  
Also used Redis as Message broker, PostgreSQL as DB   
Written to show how we can work with time-consuming tasks (operating time simulated)

Project configurated to deploy on Heroku and doesn't work localy

To see how it works use link: https://webdjango122020.herokuapp.com/

Test data:  

Size = 4  

Matrix A: [[-1, 0.22, -0.11, 0.31],  
           [ 0.38, -1, -0.12, 0.22],  
           [0.11, 0.23, 1, -0.51],  
           [0.17, -0.21, 0.31, -1]]  
           
Vector B: [-2.7, 1.5, 1.2, 0.17]  

E: 0.001
