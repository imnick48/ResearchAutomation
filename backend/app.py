from flask import Flask, request, jsonify
from Services import run_research_workflow
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/research', methods=['POST'])
def research():
    data = request.json
    if not data or 'query' not in data or 'research_question' not in data or 'groq_api_key' not in data:
        return {"error": "Missing required fields: query, research_question, groq_api_key"}, 400
    
    try:
        result = run_research_workflow(
            query=data['query'],
            research_question=data['research_question'],
            groq_api_key=data['groq_api_key'],
            max_results=data.get('max_results', 5),
            groq_model_name=data.get('groq_model_name', 'llama-3.1-8b-instant')
        )
        
        return {
            "success": True,
            "answer": result.get('final_answer', ''),
            "papers_downloaded": len(result.get('downloaded_papers', [])),
            "error": result.get('error')
        }
        
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)