from django.shortcuts import render
from django.http import JsonResponse
import re
import subprocess
import os


def ide(request):
    return render(request, "ide/ide.html")


def compile_and_run(request):
    if request.method == "POST" and request.is_ajax():
        code = request.POST.get("source", " ")
        inp = request.POST.get("input", "")
        lang = request.POST.get("lang", "")
        token = "1"
        # Writing Code into the file
        f = open('./codes/tmp/' + token + '.cpp', 'w')
        f.seek(0)
        f.truncate()
        f.write(code)
        f.close()

        # Writing testcase into file
        f = open('./codes/tmp/' + token + '.txt', 'w')
        f.seek(0)
        f.truncate()
        f.write(inp)
        f.close()

        try:  # Compilation
            output = subprocess.check_output(["g++", "./codes/tmp/" + token + ".cpp"], stderr=subprocess.STDOUT)
            subprocess.call(["g++", "./codes/tmp/" + token + ".cpp"])
            result = "AC"
        except subprocess.CalledProcessError as e:
            output = e.output
            output = output.replace("./codes/tmp/" + token + ".cpp:", "");
            has = re.match(r'\/usr.*', output)
            if (has):
                output = re.sub(r'\/usr.*', '', output)
                output = re.sub(r'\s+', ' ', output)
            result = "Compilation Error"
            response_data = {'result': result, 'input': inp, 'output': output}
            return JsonResponse(response_data, safe=False)

        # Compilation Successful
        # ipdb.set_trace()
        try:  # running
            command = "./a.out < ./codes/tmp/" + token + ".txt > ./codes/tmp/out" + token + ".txt"
            os.system(command)
            f = open('./codes/tmp/out' + token + '.txt')
            output = f.read()
            f.close()
            result = "AC"
        except subprocess.CalledProcessError as er:  # error while running
            output = er.output
            result = "Execution Failed"
        # ipdb.set_trace()
        response_data = {'result': result, 'input': inp, 'output': output}
        return JsonResponse(response_data, safe=False)
    else:
        return render(request, "ide/error.html", {"test": " Oops bad request !! "})
