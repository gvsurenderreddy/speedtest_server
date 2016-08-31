from flask import Flask,request
import datetime, os
app = Flask(__name__, static_url_path='')
app.config["DEBUG"] = True

@app.route("/", methods=['GET'])
def home():
    return "Servidor de pruebas de speedtest"

@app.route("/upload", methods=['POST'])
def hello2():
	msg = "Request via post\n sus parametros son: \n"
	print request
	print request.files['uploaded_file']
	filenombre = datetime.datetime.now().isoformat()
	f = open(filenombre, "wb")
	request.files['uploaded_file'].save(f)
	f.close()
	for k in request.form:
		msg += k+":"+request.form[k]+"\n"
	msg += "\n\n"
	msg += "Archivo guardado en " + filenombre
	return msg


@app.route("/speedtest/<int:mo_size>", methods=['GET','POST'])
def speedtest(mo_size):
	print request.method
	if request.method == 'POST':
		print "upload speedtest"
		return upload_speedtest()
	if request.method == 'GET':
		print "download speedtest"
		return download_speedtest(mo_size)

def download_speedtest(mo_size):
	return get_binary_file(mo_size)

def get_binary_file(mo_size):
	filename = str(mo_size)+'Mo.dat'
	try:
		return app.send_static_file(filename)
	except:
		create_random_binary_file(mo_size * 1024 * 1024)
		return get_binary_file(mo_size)

def upload_speedtest():
	print dir(request)
	return "OK"

def create_random_binary_file(bytes_size):
	mbytes = bytes_size/(1024**2)
	filepath = 'static/' + str(mbytes) + "Mo.dat"
	with open(filepath, 'wb') as fout:
		fout.write(os.urandom(bytes_size))
	return fout

@app.errorhandler(404)
def page_not_found(error):
    return 'La pagina no existe', 404

if __name__ == "__main__":
    app.run(host= '0.0.0.0')