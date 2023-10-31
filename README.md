# Inventory and Sales Analyzer

### Installation : 

---
##### Linux (Debian) : 

```bash 
sudo apt update
```

```bash
sudo apt install python3.11 
```

```bash
pip install -r requirements.txt
```

---
##### Windows : 

[Python Installation](https://realpython.com/installing-python/#how-to-install-python-on-windows)

```cmd prompt
pip install -r requirements.txt
```

---
### Run the App :

- You need to run the software on the same directory/folder where the app.py file exists 
- You have some browser installed on you system

##### Linux :

```bash
streamlit run app.py --server.port 5000
```

##### Windows :
```cmd
streamlit run app.py --server.port 5000
```

---

### How to Use : 

- You can open the side bar for navigation 
	- **Home** :
		- You can select the start date and end date for the categories
		- And select the Options in the side bar for the categories
		- It show the visualization
		- You can further choose the certain product or fabric etc..

	- **Storage** :
		- You can check the remain products in your storage
		- Both Raw Materials and Finished Products

	- **Sales** :
		- Here you can select the profit or sales and expenditure on the side bar
		- You can also select year wise and month wise to see the graphs

	- **Dataset** :
		- Here you can upload the new dataset in xlsx or csv format
		- Make sure it contains the new id number and date
		- you can also download the full dataset or selected dataset on the Home page here

---