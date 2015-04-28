import subprocess as sp
import os
import re
import sys

cwd = '~'
submission_folder = 'Submission attachment(s)'
classpath = '.:'
directory = 'bin'
compile_cmd = 'javac'
junit_cmd = 'java org.junit.runner.JUnitCore'
checkstyle_cmd = 'java -jar checkstyle-6.2.jar -c CS1332-checkstyle.xml '
test = ' '

def setup():
	global cwd, classpath, directory, compile_cmd, checkstyle_cmd, test
	cwd = os.getcwd()

	if not os.path.exists(cwd+'/bin'):
		os.makedirs('bin')
	if not os.path.exists(cwd+'/given'):
		os.makedirs('given')
	if not os.path.exists(cwd+'/tests'):
		os.makedirs('tests')
	if not os.path.exists(cwd+'/subs'):
		os.makedirs('subs')

	classpath = '.:' + cwd +'/junit-4.11.jar:' + cwd + '/given:'
	directory = cwd + '/bin'
	compile_cmd = 'javac -cp ' + classpath + ' -d ' + directory + ' *.java ' + cwd + '/tests/*.java'
	checkstyle_cmd = 'java -jar ' +  cwd + '/checkstyle-6.2.jar -c ' + cwd + '/CS1332-checkstyle.xml '
	test = [test for test in os.listdir('tests') if re.match('.*java', test)]
	test = test[0][:-5]

def compile():
	print 'Compiling...'
	try:
		out = sp.check_output(compile_cmd, shell=True)
	except sp.CalledProcessError as e:
		print 'Did not compile'
		return False
	return True

def checkstyle(student_file):
	print 'Running checkstyle...'
	try:
		out = sp.check_output(checkstyle_cmd + '*.java', shell=True)
		student_file.write('0 checkstyle errors\n')
	except sp.CalledProcessError as e:
		errors = len(str.splitlines(e.output)) - 2
		student_file.write(str(errors) + ' checkstyle errors\n')

def junit(student_file):
	print 'Running JUnits...'
	prev_dir = os.getcwd()
	os.chdir(cwd + '/bin')
	try:
		out = sp.check_output(junit_cmd + ' ' + test, shell=True)
		student_file.write(out)
	except sp.CalledProcessError as e:
		student_file.write(e.output)

	os.chdir(prev_dir)


def grade():
	os.chdir(cwd + '/subs')
	students = [folder for folder in os.listdir('.') if os.path.isdir(folder)]
	for folder in students:
		print '\nGrading student: ' + folder
		os.chdir(folder+"/"+submission_folder)
		student_file = open('graded.txt', 'w')

		if compile():
			checkstyle(student_file)
			junit(student_file)
		else:
			student_file.write('Did not compile')

		student_file.close()
		os.chdir(cwd + '/subs')



if __name__ == "__main__":
	setup()
	if(len(sys.argv) <= 1):
		grade()




