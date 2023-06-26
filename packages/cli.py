import requests
import json

def get_response(video_dir, server_address):
	

	url = server_address + "/predict"

	# The 'file' key here must match the key in request.files['file'] on the server.
	data = {
		'file': open(video_dir, 'rb')
	}

	response = requests.post(url, files=data)

	return json.loads(response.text)
