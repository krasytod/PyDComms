#!flask/bin/python

def run_flask():
	from app import app
	app.run(debug=True)



if __name__ == "__main__":
    #pass    
    run_flask()   
