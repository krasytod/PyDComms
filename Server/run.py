#!flask/bin/python



def run_flask():
	from app import app,return_comm_id
	app.jinja_env.filters['return_comm_id'] = return_comm_id
	app.run(debug=True,threaded=True)
	


if __name__ == "__main__":
    #pass    
    run_flask()   
