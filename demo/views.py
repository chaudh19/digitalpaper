from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings

import base64
import json
import os
import requests
import xml.etree.ElementTree as ET
from itertools import permutations
import random 
import re


def test_1(request):
	return render(request, 'demo/test_1.html', { })


###################################
#
# New Views
#
###################################

# TODO - real questions, solutions, terms

questions = [

{'name': '(−5k^3−6k+1)+(−6k^2+5k)', 
	'type':'simplify', 
	'solution': ['-5 k^({3}) - 6 k^({2}) - k + 1'], 
	'terms': ['- 6 k^({2}) ', '- 5 k^({3}) ', '- k ', '+ 1 '], 
	'eval_input': ' where k = 30',
	'eval_output': '-140429',
},

{'name': '\sqrt{10-4x}=\sqrt{2x+3}', 'type':'solve', 
	'solution': ['x = 7/6', '7/6 = x'],
	'eval_output': 'x = 7/6'
},

{'name': '2x^{4}+4x^{3}-30x^{2}', 
	'type':'factor', 
	# 'terms': ['2 x^({2}) ', '(x - 3) ', '(x + 5) '], 
	'solution': ['2 x^2 (x - 3) (x + 5)', '2 x^2 (x + 5) (x - 3)' ],
	'eval_output': '2 x^4 + 4 x^3 - 30 x^2'
},

{'name': 'gcf of 3x^4, 15x^3, 21x^2',
	'type':'gcf',
	'solution': '3 x^2'
},
]

def bootstrap(request, num):
	return render(request, 'demo/bootstrap.html', { 'num': num, 'questions': questions, 'question': questions[int(num)-1]['name'] })

def bootstrap_query(request):
	if request.POST.get('action') == 'post':
		query = request.POST.get('input')
		num = request.POST.get('num')
		
		# valid = check(query, num)
		valid = random.randint(0,1)
		
		if valid == 0:
			response = JsonResponse({"status": "incorrect"})
			print('---- incorrect ----')
			return response
		else:
			print('---- correct ----')
			return render(request, 'demo/bootstrap_equation.html', {'num': num, 'hint': 'HINT'})

def check(query, num):
	question_type = questions[int(num)-1]['type']
	if( question_type == 'simplify' ): return simplify(query, num)
	if( question_type == 'solve' ): return solve(query, num)
	if( question_type == 'factor' ): return factor(query, num)
	if( question_type == 'expand' ): return expand(query, num)

	if random.randint(0,1) == 0:
		return False
	else: 
		return True

def clean(query):
	encoded_query = requests.utils.quote(query)
	r = requests.get('http://api.wolframalpha.com/v2/query?appid=32J79Q-R6UEQ4VQE2&input='+encoded_query+'&podtitle=Input&format=plaintext')
	tree = ET.fromstring(r.content)
	new_query = tree.findall('.//plaintext')[0].text
	print('cleaned: ', new_query)
	return new_query

def simplify(query, num):
	l = list(permutations(questions[int(num)-1]['terms'])) 
	perms_temp = []
	for item in l:
		perms_temp.append(''.join(item).strip("+").strip())

	perms = []
	for item in perms_temp:
		perms.append(re.sub('^%s' % '- ', '-', item))
		
	query = clean(query)
	if query in questions[int(num)-1]['solution']:
		print('correct')
	elif query in perms:
		print('put in standard form')
	else:
		query = query + questions[int(num)-1]['eval_input']
		encoded_query = requests.utils.quote(query)
		r = requests.get('http://api.wolframalpha.com/v2/query?appid=32J79Q-R6UEQ4VQE2&input='+encoded_query+'&podtitle=Result&format=plaintext')
		tree = ET.fromstring(r.content)
		result = tree.findall('.//plaintext')[0].text
		
		if result == questions[int(num)-1]['eval_output']:
			print('correct, whats next?')
		else:
			print('hm not quite')
	print('simplify')

def solve(query, num):
	# l = list(permutations(questions[int(num)-1]['terms'])) 
	# perms_temp = []
	# for item in l:
	# 	perms_temp.append(''.join(item).strip("+").strip())

	# perms = []
	# for item in perms_temp:
	# 	perms.append(re.sub('^%s' % '- ', '-', item))
		
	query = clean(query)
	print(query)
	if query in questions[int(num)-1]['solution']:
		print('correct')
	else:
		# query = query + questions[int(num)-1]['eval_input']
		encoded_query = requests.utils.quote(query)
		try: 
			r = requests.get('http://api.wolframalpha.com/v2/query?appid=32J79Q-R6UEQ4VQE2&input='+encoded_query+'&podtitle=Solution&format=plaintext')
			tree = ET.fromstring(r.content)
			result = tree.findall('.//plaintext')[0].text
			if result == questions[int(num)-1]['eval_output']:
				print('correct, whats next?')
		except: 
			try: 
				r = requests.get('http://api.wolframalpha.com/v2/query?appid=32J79Q-R6UEQ4VQE2&input='+encoded_query+'&podtitle=Exact%20result&format=plaintext')
				tree = ET.fromstring(r.content)
				result = tree.findall('.//plaintext')[0].text
				if result == questions[int(num)-1]['eval_output']:
					print('correct, whats next?')
			except:
				print('hm not quite')
	print('solve')

def factor(query, num):
	query = clean(query)


	print('query')
	print(query)
	if query in questions[int(num)-1]['solution']:
		print('correct')

	# TODO - enumerate terms

	else:
		encoded_query = requests.utils.quote(query)
		r = requests.get('http://api.wolframalpha.com/v2/query?appid=32J79Q-R6UEQ4VQE2&input='+encoded_query+'&podtitle=Expanded%20form&format=plaintext')
		tree = ET.fromstring(r.content)
		result = tree.findall('.//plaintext')[0].text
		if result == questions[int(num)-1]['eval_output']:
			print('correct, whats next?')
		else:
			print('hm not quite')

	print('factor')

def expand(query, num):
	# solution
	# terms
	# check against wolfram - expanded
	print('expand')

# def remove_prefix(text, prefix):
    # return text[text.startswith(prefix) and len(prefix):]

def lreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' starts 'string'.
    """
    return re.sub('^%s' % pattern, sub, string)

###################################
#
# Old Views
#
###################################

# x ^ { 2 } + 5

def index(request):
	return render(request, 'demo/index.html', {})

def mathpix_lookup(request):
	response_data = {}

	print('in mathpix_lookup')

	if request.POST.get('action') == 'post':
		dataURL = request.POST.get('dataURL')

		print('data URL ', dataURL)

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

		print('r ', r)
		print('r(latex_simplified) ', r['latex_simplified'])

		# return render(request, 'demo/display_result.html', { 'latex': r['latex_simplified'] })

		return HttpResponse(r['latex_simplified'])
	else:
		dataURL = ''
		return HttpResponse("No URL")

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
