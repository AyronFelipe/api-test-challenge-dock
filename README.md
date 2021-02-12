# Challenge API Fintech

 - How to run the project locally?
	 - 
	 - Run: `docker-compose up --build`;
	 - If something wrong happens in connection between the application and database, run: `docker-compose restart web`;
	 - Run the migrations of the project: `docker-compose exec web python manage.py migrate`;
	 -  To populate the table of persons run: `docker-compose exec web python manage.py loaddata core.pessoas.json`
 - How to test the application?
	 - 
	 - Run: `docker-compose exec web pytest`;
- Project Architecture
	- 
	- [Diagram Class](https://ibb.co/m6swDmN)
- Documentation
	- 
	- The documentation can be found in: [http://localhost:8000/documentation/](http://localhost:8000/documentation/)
