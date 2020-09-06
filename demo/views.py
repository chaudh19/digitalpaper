from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import base64
import json
import os
import requests
import xml.etree.ElementTree as ET
from itertools import permutations 

###################################
#
# Views
#
###################################

# x ^ { 2 } + 5

def index(request):
	return render(request, 'demo/index.html', {})

def mathpix_lookup(request):
	response_data = {}

	if request.POST.get('action') == 'post':
		dataURL = request.POST.get('dataURL')
		url = dataURL.split(",")[1]
		data = url.replace(' ', '+')
		imgdata = base64.b64decode(data)
		filename = 'demo/static/demo/some_image.png'  # I assume you have a way of picking unique filenames
		if os.path.exists(filename):
			os.remove(filename)
		with open(filename, 'wb') as f:
			f.write(imgdata)
		
		r = latex({
		    'src': image_uri(filename),
		    'formats': ['latex_simplified']
		})

		return render(request, 'demo/display_result.html', { 'latex': r['latex_simplified'] })
	else:
		dataURL = ''
		return HttpResponse("<p>no url<p>")


def wolfram(request):
	solution = '-5 k^({3}) - 6 k^({2}) - k + 1'
	terms = ['-5 k^({3}) ', '- 6 k^({2}) ', '- k ', '+ 1 ']
	# TODO programmatically add a space rather than manually
		
	l = list(permutations(terms)) 
	perms = []
	for item in l:
		perms.append(''.join(item).strip("+").strip())

	print(perms)

	steps = ['-5k^{3}-6k+5k-(6k^{2})+1', '-5k^{3}-k-6k^{2}+1', '-5k^{3}-6k^{2}-k+1']

	for s in steps:
		# TODO MAYBE able to combine the two wolfram queries?
		encoded_query = requests.utils.quote(s)
		r = requests.get('http://api.wolframalpha.com/v2/query?appid=32J79Q-R6UEQ4VQE2&input='+encoded_query+'&podtitle=Input&format=plaintext')
		tree = ET.fromstring(r.content)
		new_s = tree.findall('.//plaintext')[0].text
		
		if new_s == solution:
			print(new_s, ' correct answer')
		elif new_s in perms:
			print(new_s, ' nice work. how would you write this in standard form?')
		else:
			query = new_s + ' where k = 30'
			encoded_query = requests.utils.quote(query)
			r = requests.get('http://api.wolframalpha.com/v2/query?appid=32J79Q-R6UEQ4VQE2&input='+encoded_query+'&podtitle=Result&format=plaintext')
			tree = ET.fromstring(r.content)
			result = tree.findall('.//plaintext')[0].text
			if result == '-140429':
				print(new_s, ' correct, whats next')
			else:
				print(new_s, ' hm not quite')

	return HttpResponse("<p>no url<p>")


def wolfram2(request):
	solution = 'x = 7/6'
	terms = ['-5k^{3}', '-6k^{2}', '-k', '+1']
	
	l = list(permutations(['-5k^{3}', '-6k^{2}', '-k', '+1'])) 
	perms = []
	for item in l:
		perms.append(''.join(item).strip("+"))

	print(perms)

	steps = ['-5k^{3}-6k+5k-6k^{2}+1', '-5k^{3}-k-6k^{2}+1', '-5k^{3}-6k^{2}-k+1']

	for s in steps:
		if s == solution:
			print(s, ' correct answer')
		elif s in perms:
			print(s, ' nice work. how would you write this in standard form?')
		else:
			query = s + ' where k = 30'
			encoded_query = requests.utils.quote(query)
			r = requests.get('http://api.wolframalpha.com/v2/query?appid=32J79Q-R6UEQ4VQE2&input='+encoded_query+'&podtitle=Result&format=plaintext')
			tree = ET.fromstring(r.content)
			result = tree.findall('.//plaintext')[0].text
			if result == '-140429':
				print(s, ' correct, whats next')
			else:
				print(s, ' hm not quite')

	return HttpResponse("<p>no url<p>")


def perms(request):
	l = list(permutations(['-5k^{3}', '-6k^{2}', '-k', '+1'])) 
	new_l = []
	for item in l:
		new_l.append(''.join(item))
	return render(request, 'demo/perms.html', {'l':new_l})

###################################
#
# Wolfram Tests
#
###################################

def wolfram_expanded_form(request):
	query = '2x^2(x^2 + 2x -15)'
	encoded_query = requests.utils.quote(query)
	r = requests.get('http://api.wolframalpha.com/v2/query?appid=32J79Q-R6UEQ4VQE2&input='+encoded_query+'&podtitle=Expanded%20form&format=plaintext')
	tree = ET.fromstring(r.content)
	expanded_form = tree.findall('.//plaintext')[0].text
	return render(request, 'demo/wolfram_expanded_form.html', {
		'query': query,
		'expanded_form':expanded_form
		})


def wolfram_evaluate(request):
	query = '−5k^3 −6k+5k−6k ^2 +1 where k = 30'
	encoded_query = requests.utils.quote(query)
	r = requests.get('http://api.wolframalpha.com/v2/query?appid=32J79Q-R6UEQ4VQE2&input='+encoded_query+'&podtitle=Result&format=plaintext')
	tree = ET.fromstring(r.content)
	result = tree.findall('.//plaintext')[0].text
	return render(request, 'demo/wolfram_evaluate.html', {
		'query': query,
		'result':result
		})


def wolfram_terms(request):
	query = '−5k^3 −6k+5k + 1 −6k ^2 terms'
	encoded_query = requests.utils.quote(query)
	r = requests.get('http://api.wolframalpha.com/v2/query?appid=32J79Q-R6UEQ4VQE2&input='+encoded_query+'&podtitle=Result&format=plaintext')
	tree = ET.fromstring(r.content)
	result = tree.findall('.//plaintext')[0].text
	return render(request, 'demo/wolfram_evaluate.html', {
		'query': query,
		'result':result
		})


###################################
#
# Mathpix
#
###################################

env = os.environ

default_headers = {
    'app_id': env.get('APP_ID', 'simran_d_chaudhry_gmail_com_99db0f'),
    'app_key': env.get('APP_KEY', '486f4d7131692b82cd9a'),
    'Content-type': 'application/json'
}

service = 'https://api.mathpix.com/v3/latex'

#
# Return the base64 encoding of an image with the given filename.
#
def image_uri(filename):
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()

#
# Call the Mathpix service with the given arguments, headers, and timeout.
#
def latex(args, headers=default_headers, timeout=30):
    r = requests.post(service,
        data=json.dumps(args), headers=headers, timeout=timeout)
    return json.loads(r.text)
