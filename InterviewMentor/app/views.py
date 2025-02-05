from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from sentence_transformers import SentenceTransformer, util
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request, 'content.html')

def services(request):
    # You can add context data for services if needed
    return render(request, 'services.html')

def about(request):
    # You can add context data for about page if needed
    return render(request, 'about.html')

def faq(request):
    # You can add context data for FAQ if needed
    return render(request, 'faq.html')




def start_interview(request):
    if request.method == 'POST' and request.FILES['resume']:
        resume = request.FILES['resume']
        fs = FileSystemStorage()
        filename = fs.save(resume.name, resume)
        uploaded_file_url = fs.url(filename)
        return render(request, 'start_interview.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'start_interview.html')


from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from groq import Groq
from difflib import SequenceMatcher
from .utils import extract_text_from_pdf, parse_generated_output

transformer = Groq(api_key="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")

# Generate questions view
def generate_questions(request):
    if request.method == "POST" and request.FILES.get('resume'):
        resume = request.FILES['resume']
        fs = FileSystemStorage()
        filename = fs.save(resume.name, resume)
        uploaded_file_path = fs.path(filename)

        resume_text = extract_text_from_pdf(uploaded_file_path)
        if not resume_text.strip():
            return JsonResponse({"error": "Failed to extract text from resume."})

        try:
            questions = pretrained_model.generate_questions(resume_text)
            request.session['questions'] = questions
            return redirect('chat_interface')
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return render(request, 'upload_resume.html')

@csrf_exempt
def verify_answer(question, user_answer):
    try:
        if not question or not user_answer:
            return {"error": "Both question and answer are required."}

        analysis = pretrained_model.analyze_answer(question, user_answer)
        detailed_feedback = pretrained_model.generate_feedback()
        return {
            "expected_answer": f"Expected answer for: {question}",
            "similarity_score": 0.42,  # Arbitrary value for demonstration
            "is_correct": analysis["score"] > 50,  # Arbitrary threshold
            "feedback": f"{analysis['feedback']} Additional feedback: {detailed_feedback}"
        }

    except Exception as e:
        return {"error": str(e)}

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  
def calculate_semantic_similarity(user_response, expected_response, threshold=0.7):
    embeddings = embedding_model.encode([user_response, expected_response])
    cosine_score = util.cos_sim(embeddings[0], embeddings[1]).item()
    return cosine_score >= threshold, cosine_score


@csrf_exempt
def chat_interface(request):
    questions = request.session.get('questions', [])
    if not questions:
        return redirect('generate_questions')
    return render(request, 'chat_interface.html', {"questions": questions})

from django.http import JsonResponse
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def save_answers(request):
    if request.method == "POST":
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            responses = data.get('responses', [])
            if not isinstance(responses, list):  # Ensure responses is a list
                return JsonResponse({"error": "Invalid data format. 'responses' must be a list."}, status=400)

            # Save responses to the session
            request.session['responses'] = responses
            
            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Something went wrong"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

def result(request):
    if request.method == "GET":
        # Retrieve responses from the session
        responses = request.session.get('responses', [])
        
        # Initialize the list to hold results
        results = []

        # Process each response to verify answers
        for response in responses:
            question = response.get('question', '')
            user_answer = response.get('answer', '')

            # Call verify_answer directly within the view
            verification_result = verify_answer(question, user_answer)

            if 'error' in verification_result:
                results.append({"error": verification_result["error"]})
            else:
                results.append({
                    'question': question,
                    'answer': user_answer,
                    'expected_answer': verification_result['expected_answer'],
                    'similarity_score': verification_result['similarity_score'],
                    'result': "Correct" if verification_result['is_correct'] else "Incorrect",
                })
        
        # Render the results in the template
        return render(request, 'result.html', {'results': results})
    
    return JsonResponse({"error": "Invalid request method"}, status=400)
