import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def parse_generated_output(output):
    question_list = []
    questions = output.split("\n")  # Split lines assuming questions are line-separated
    for question in questions:
        if question.strip() and not question.startswith("Answer"):  # Filter out any text that isn't a question
            question_list.append(question.strip())
    return question_list[:]