import React, { useState } from 'react';
import { Search, BookOpen, Key, Settings, Loader2, CheckCircle, XCircle, Download } from 'lucide-react';

const ResearchSec = () => {
  const [formData, setFormData] = useState({
    query: '',
    research_question: '',
    groq_api_key: '',
    max_results: 5,
    groq_model_name: 'llama-3.1-8b-instant'
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || 'Something went wrong');
      }
    } catch (err) {
      setError('Failed to connect to the server. Make sure the Flask API is running on localhost:5000');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2 flex items-center justify-center gap-3">
            <BookOpen className="text-blue-600" size={40} />
            Research Assistant
          </h1>
          <p className="text-gray-600">AI-powered research using ArXiv papers</p>
        </div>

        {/* Main Form */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="space-y-6">
            {/* Query Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
                <Search size={16} />
                Search Query
              </label>
              <input
                type="text"
                name="query"
                value={formData.query}
                onChange={handleInputChange}
                placeholder="e.g., quantum computing, NLP transformers"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            {/* Research Question */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Research Question
              </label>
              <textarea
                name="research_question"
                value={formData.research_question}
                onChange={handleInputChange}
                placeholder="What specific question do you want answered?"
                rows="3"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            {/* API Key */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
                <Key size={16} />
                Groq API Key
              </label>
              <input
                type="password"
                name="groq_api_key"
                value={formData.groq_api_key}
                onChange={handleInputChange}
                placeholder="Enter your Groq API key"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            {/* Advanced Settings */}
            <div className="border-t pt-4">
              <label className="block text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
                <Settings size={16} />
                Advanced Settings
              </label>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs text-gray-500 mb-1">Max Results</label>
                  <select
                    name="max_results"
                    value={formData.max_results}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value={3}>3 papers</option>
                    <option value={5}>5 papers</option>
                    <option value={10}>10 papers</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs text-gray-500 mb-1">Model</label>
                  <select
                    name="groq_model_name"
                    value={formData.groq_model_name}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="llama-3.1-8b-instant">Llama 3.1 8B</option>
                    <option value="llama-3.1-70b-versatile">Llama 3.1 70B</option>
                    <option value="mixtral-8x7b-32768">Mixtral 8x7B</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              onClick={handleSubmit}
            >
              {isLoading ? (
                <>
                  <Loader2 className="animate-spin" size={20} />
                  Researching...
                </>
              ) : (
                <>
                  <Search size={20} />
                  Start Research
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-center gap-2 text-red-700">
              <XCircle size={20} />
              <span className="font-medium">Error</span>
            </div>
            <p className="text-red-600 mt-1">{error}</p>
          </div>
        )}

        {result && (
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center gap-2 text-green-700 mb-4">
              <CheckCircle size={20} />
              <span className="font-medium">Research Complete!</span>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="flex items-center gap-2">
                  <Download size={16} className="text-blue-600" />
                  <span className="text-sm text-blue-600">Papers Downloaded</span>
                </div>
                <div className="text-2xl font-bold text-blue-700">{result.papers_downloaded}</div>
              </div>

              <div className="bg-green-50 rounded-lg p-4">
                <div className="flex items-center gap-2">
                  <CheckCircle size={16} className="text-green-600" />
                  <span className="text-sm text-green-600">Status</span>
                </div>
                <div className="text-lg font-semibold text-green-700">
                  {result.success ? 'Success' : 'Failed'}
                </div>
              </div>
            </div>

            {/* Answer */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Research Answer:</h3>
              <div className="bg-gray-50 rounded-lg p-4 border">
                <p className="text-gray-800 whitespace-pre-wrap leading-relaxed">
                  {result.answer || 'No answer provided'}
                </p>
              </div>
            </div>

            {/* Error in result */}
            {result.error && (
              <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div className="flex items-center gap-2 text-yellow-700">
                  <XCircle size={16} />
                  <span className="font-medium">Warning</span>
                </div>
                <p className="text-yellow-600 mt-1">{result.error}</p>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-8 text-gray-500 text-sm">
          <p>Make sure your Flask API is running on 127.0.0.1:5000</p>
          <p className="mt-1">Get your Groq API key from: <a href="https://console.groq.com" className="text-blue-600 hover:underline">console.groq.com</a></p>
        </div>
      </div>
    </div>
  );
};

export default ResearchSec;