# Vending Machine Tracking Application to manage all the vending machines in muic (stock etc).

### In this project I use python-flask for creating the backend. For this project, it will only have backend that return json file. The way to test it out to use postman (which will explain below).

## Database Model
![Database_A1-2](https://user-images.githubusercontent.com/104582029/213465209-07e3101a-13dc-4681-89cd-e9c9d4914301.jpg)

I use docker to run the database server and sqlalchemy for interact with the database.

This is the command I use to run the docker.
```
docker run -p 127.0.0.1:13310:3306 --name mysqldb -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=vendingMC -d --restart=always mysql
```

## Read All Machines & Products
You have to pass the url in the postman with the right method (in this case is GET method).
This will list all vending machine stocks & products as show in the picture.

### Example
![image](https://user-images.githubusercontent.com/104582029/213472163-3f95cafd-a6d7-4b06-9378-4b2e405da675.png)
![image](https://user-images.githubusercontent.com/104582029/213482636-950794da-f668-4533-9a0f-ebca5f959150.png)


## Create Machine & Product
For creating you need to pass the data. For vending Machine--name, location, relation(product in the vending Machine).
Moreover, you can pass multiple products in vending machine and There is a a quanitity for each vending machine.
For relation(or pid in the picture) you need to pass the value the this format (product_id1:quantity1),(product_id2:quantity2),... as show in the picture below.

### Example
![image](https://user-images.githubusercontent.com/104582029/213473443-781ce200-4152-43a9-8995-23ce8080408d.png)

For Product--name, price and pass the value same as the picture below.

![image](https://user-images.githubusercontent.com/104582029/213473502-34674d4c-c08d-4d1e-8c38-519d445c5abc.png)

## Edit Machine & Product

you can add/edit/remove item from stock in each machines as show in the picture below.

### Example
![image](https://user-images.githubusercontent.com/104582029/213480583-454dfa5b-b37d-4462-b05d-1e5e798a3155.png)
![image](https://user-images.githubusercontent.com/104582029/213483266-78fae274-c745-4b4e-9e24-9f9a64516ca5.png)

## Delete Machine & Product

Any relation that relate to the deleted machine or product will also deleted.

### Example
![image](https://user-images.githubusercontent.com/104582029/213484638-d29420b2-8bb6-45bb-833f-0000d4b4df62.png)
![image](https://user-images.githubusercontent.com/104582029/213484668-9418bf76-3a4d-4d0a-bf73-9c87c7db0f8c.png)

## PS. Data sample is in the tables.py uncommnet the code below to create database.
