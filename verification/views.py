from django.shortcuts import render
from .models import Solution , Step
from .serializer import SolutionSerializer , StepSerializer , SolutionCreateSerializer
from django.conf import settings
import os
import json

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@api_view(['POST'])
def create_solution(request:Request):
    api_path = os.path.join(settings.BASE_DIR,"verification", "prompts", "api_key.txt")
    api = open(api_path).read()
    client = OpenAI(api_key=api)
    # check if solution already exists. for handeling errors. (check account when created)
    serializer = SolutionCreateSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.validated_data['question']

        sol = Solution(question=question, cur_chunk=0)
        sol.save()

        steps = serializer.validated_data['steps']
        for i in range(0, len(steps)):
            text = steps[i]
            step = Step(section=i, text=text , is_valid=False,confidence_score=0 , explanation="" , feedback="", solution=sol)
            step.save()  

        ##  Keep in mind that errors might happen , save everything
        for i in range(sol.cur_chunk ,len(steps)):
            step = sol.step_set.get(section=i)
            prompt_path = os.path.join(settings.BASE_DIR,"verification", "prompts", "step_prompt.txt")
            prompt = open(prompt_path ,'r', encoding='utf-8').read()
            prompt_data = {
                "question": question,
                "previous_corrected_sections":list(sol.step_set.all())[:i],
                "current_section": steps[i]
            }

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "شما یک ارزیاب خبره برای پاسخ‌های طولانی و مرحله‌به‌مرحله‌ی امتحانی هستید."},
                    {"role": "user", "content": prompt + str(prompt_data)}
                ],
                temperature=1
                ).choices[0].message.content
            # print("\n\n\n" ,response[7:-3],"\n\n\n")
            response = json.loads(response[7:-3])
                
            step.is_valid = response["is_valid"]
            step.confidence_score = response["confidence_score"]
            step.explanation = response["explanation"]
            step.feedback = response["feedback"]
            step.solution = sol
            step.save()

            sol.cur_chunk = sol.cur_chunk +1
            sol.save()
            

        return Response({"Correction" : SolutionSerializer(sol).data , "steps":StepSerializer(sol.step_set.all() , many=True).data}, status=200)
    return Response({'Not valid'}, status=200)

'''
{
"question" : string,
"steps" : ["step1" , "step2" , ... ]
}
'''

'''
{
"question" : "دو ضرب در دو چند میشه؟",
"steps" : ["دو ضرب در دو میشه همون دو به علاوه دو" , "پس جواب برابر 4 هستش" ]
}
'''