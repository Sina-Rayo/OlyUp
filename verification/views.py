from django.shortcuts import render
from .models import Solution , Step
from .serializer import SolutionSerializer , StepSerializer , SolutionCreateSerializer

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@api_view(['POST'])
def create_solution(request:Request):
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
            prompt_path = "prompts/step_prompt.txt"
            prompt = open(prompt_path).read()
            prompt_data = {
                "question": question,
                "previous_corrected_sections":sol.set_step.all[:i],
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
                
            step.is_valid = response["is_valid"]
            step.confidence_score = response["confidence_score"]
            step.explanation = response["explanation"]
            step.feedback = response["feedback"]
            step.save()

            sol.cur_chunk = sol.cur_chunk +1
            sol.save()
            

        return Response({'Solution has been made Successfully'}, status=200)
    return Response({'Not valid'}, status=200)

'''
{
"question" : string,
"chunk_size" : int,
"steps" : ["step1" , "step2" , ... ]
}
'''