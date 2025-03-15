import React, { useState } from 'react';
import { Link2, BarChart3 } from 'lucide-react';
import axios from 'axios';

interface SentimentData {
  result: number[];
}

function App() {
  const [link, setLink] = useState<string>('');
  const [data, setData] = useState<SentimentData>({ result: [] });
  
  const handleAnalyze = () => {
    axios.get<SentimentData>(`http://127.0.0.1:5000/getSentiment?link=${link}`)
    .then((response) => {
      console.log(response.data);
      setData(response.data);
    })
    .catch((error) => {
      console.log(error);
    });
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
      <div className="max-w-4xl mx-auto space-y-12">
        {/* Link Input Section */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mt-12">
          <div className="flex items-center gap-3 mb-6">
            <Link2 className="w-8 h-8 text-blue-600" />
            <h1 className="text-2xl font-semibold text-gray-800">Paste Your Link</h1>
          </div>
          <div className="relative">
            <input
              type="text"
              value={link}
              onChange={(e) => setLink(e.target.value)}
              placeholder="https://example.com"
              className="w-full px-6 py-4 text-lg rounded-xl border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition duration-200"
            />
            <button
              className="absolute right-3 top-1/2 -translate-y-1/2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition duration-200"
              onClick={handleAnalyze}
            >
              Analyze
            </button>
          </div>
        </div>
        {/* Chart Section */}
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="flex items-center gap-3 mb-6">
            <BarChart3 className="w-8 h-8 text-blue-600" />
            <h2 className="text-2xl font-semibold text-gray-800">Analytics</h2>
          </div>
          <div className="h-[400px] flex items-end justify-around gap-4 p-4">
            {data.result.map((value, index) => {
              const height = (value * 100).toFixed(2);
              return (
                <div key={index} className="relative group w-full h-full flex flex-col justify-end">
                  <div
                    className="w-full bg-blue-500 hover:bg-blue-600 rounded-t-lg transition-all duration-300 cursor-pointer"
                    style={{ height: `${height}%` }}
                  >
                    <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-800 text-white px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                      {height}%
                    </div>
                  </div>
                  <div className="text-center mt-2 text-sm text-gray-600">
                    Category {index + 1}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;