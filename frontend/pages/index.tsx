// pages/index.tsx
import { useState, useEffect, useRef } from 'react';
import Head from 'next/head';

export default function Home() {
  const [messages, setMessages] = useState<{id: number, role: string, content: string}[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [showAuth, setShowAuth] = useState<boolean>(true);
  const [authForm, setAuthForm] = useState<'login' | 'register'>('login');
  const [email, setEmail] = useState<string>('');
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check for existing token on load
  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    if (savedToken) {
      setToken(savedToken);
      setShowAuth(false);
    }
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const apiUrl = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
        ? 'https://todo-ai-chatbot-production.up.railway.app'
        : '';

      const response = await fetch(`${apiUrl}/auth/${authForm}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: authForm === 'register' ? email : undefined,
          username,
          password
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Authentication failed');
      }

      const data = await response.json();
      const AccessToken = data.access_token;

      // Save token to localStorage
      localStorage.setItem('token', AccessToken);
      setToken(AccessToken);
      setShowAuth(false);
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setShowAuth(true);
    setMessages([]);
    setConversationId(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading || !token) return;

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const apiUrl = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
        ? 'https://todo-ai-chatbot-production.up.railway.app'
        : '';

      // First attempt with existing conversation ID
      let response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          conversation_id: conversationId || null, // Use existing conversation or start new one
          message: inputValue
        })
      });

      // If we get a 404, try again with a null conversation ID
      if (response.status === 404) {
        console.warn('Conversation not found, retrying with new conversation...');
        setConversationId(null); // Reset conversation ID

        // Retry with null conversation ID
        response = await fetch(`${apiUrl}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            conversation_id: null, // Force new conversation
            message: inputValue
          })
        });
      } else if (response.status === 401) {
        // Token might be expired, redirect to login
        handleLogout();
        return;
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID with the one returned from the server
      setConversationId(data.conversation_id);

      // Add assistant response to messages
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response || 'Sorry, I encountered an error processing your request. Please try again later.'
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Check if this was a task-modifying operation and auto-refresh task list
      const lowerInput = inputValue.toLowerCase();
      if (lowerInput.includes('add ') || lowerInput.includes('delete ') ||
          lowerInput.includes('complete ') || lowerInput.includes('update ') ||
          lowerInput.includes('mark ')) {
        // Wait a bit to ensure the operation completes, then fetch updated task list
        setTimeout(async () => {
          try {
            // Use a fresh conversation ID to ensure we get the latest state
            const refreshResponse = await fetch(`${apiUrl}/api/chat`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify({
                conversation_id: null, // Use null to start fresh and get latest state
                message: "show all tasks" // Request updated task list
              })
            });

            if (refreshResponse.ok) {
              const refreshData = await refreshResponse.json();
              const refreshMessage = {
                id: Date.now() + 2,
                role: 'assistant',
                content: refreshData.response || 'Sorry, I encountered an error processing your request. Please try again later.'
              };

              // Add the refresh message to the messages array
              setMessages(prev => {
                // Filter out any previous task list messages to avoid duplicates
                const filtered = prev.filter(msg =>
                  !(msg.role === 'assistant' &&
                    (msg.content.includes('Here are your all tasks') ||
                     msg.content.includes('Here are your pending tasks') ||
                     msg.content.includes('You don\'t have any')))
                );
                return [...filtered, refreshMessage];
              });
            }
          } catch (error) {
            console.error('Error refreshing task list:', error);
          }
        }, 800); // Increased delay to ensure operation completes
      }
    } catch (error: any) {
      console.error('Error sending message:', error);
      // Add error message to UI
      let errorMessageText = 'Sorry, I encountered an error processing your request. Please try again later.';

      // Try to get more specific error message
      if (error.message) {
        errorMessageText = `Error: ${error.message}`;
      } else if (typeof error === 'string') {
        errorMessageText = `Error: ${error}`;
      }

      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: errorMessageText
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Head>
        <title>Todo AI Chatbot</title>
        <meta name="description" content="AI-powered chatbot for managing todos" />
      </Head>

      <style jsx global>{`
        body {
          font-family: 'Poppins', sans-serif;
        }

        .fade-in {
          animation: fadeIn 0.3s ease-in-out;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .slide-in {
          animation: slideIn 0.4s ease-out;
        }

        @keyframes slideIn {
          from { opacity: 0; transform: translateX(-20px); }
          to { opacity: 1; transform: translateX(0); }
        }

        .pulse {
          animation: pulse 2s infinite;
        }

        @keyframes pulse {
          0% { transform: scale(1); }
          50% { transform: scale(1.05); }
          100% { transform: scale(1); }
        }

        .bounce {
          animation: bounce 1s infinite;
        }

        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-5px); }
        }
      `}</style>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <header className="text-center mb-10 slide-in">
          <div className="flex justify-center mb-4">
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-2 rounded-full shadow-lg">
              <div className="bg-white p-2 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
            </div>
          </div>

          <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600 mb-3">
            Todo AI Chatbot
          </h1>
          <p className="text-gray-600 text-lg max-w-md mx-auto">
            Manage your tasks through natural language conversation
          </p>

          {token && (
            <div className="mt-6 flex justify-center items-center space-x-4">
              <span className="text-sm text-gray-500 bg-white px-3 py-1 rounded-full shadow-sm">
                Logged in
              </span>
              <button
                onClick={handleLogout}
                className="text-sm bg-gradient-to-r from-red-500 to-orange-500 hover:from-red-600 hover:to-orange-600 text-white py-1.5 px-4 rounded-full shadow-md transition-all duration-300 transform hover:scale-105"
              >
                Logout
              </button>
            </div>
          )}
        </header>

        {showAuth ? (
          <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md mx-auto transform transition-all duration-500 hover:shadow-2xl">
            <div className="flex bg-gray-100 rounded-lg p-1 mb-6">
              <button
                className={`flex-1 py-3 font-semibold rounded-md transition-colors duration-300 ${
                  authForm === 'login'
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
                onClick={() => setAuthForm('login')}
              >
                Sign In
              </button>
              <button
                className={`flex-1 py-3 font-semibold rounded-md transition-colors duration-300 ${
                  authForm === 'register'
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
                onClick={() => setAuthForm('register')}
              >
                Sign Up
              </button>
            </div>

            {error && (
              <div className="mb-6 p-3 bg-red-50 text-red-700 rounded-lg flex items-center animate-pulse">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                {error}
              </div>
            )}

            <form onSubmit={handleAuthSubmit} className="space-y-5">
              {authForm === 'register' && (
                <div className="animate-fadeIn">
                  <label className="block text-gray-700 text-sm font-medium mb-2" htmlFor="email">
                    Email
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                        <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                      </svg>
                    </div>
                    <input
                      id="email"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      placeholder="your@email.com"
                      required
                    />
                  </div>
                </div>
              )}

              <div className="animate-fadeIn">
                <label className="block text-gray-700 text-sm font-medium mb-2" htmlFor="username">
                  Username
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <input
                    id="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="Enter your username"
                    required
                  />
                </div>
              </div>

              <div className="animate-fadeIn">
                <label className="block text-gray-700 text-sm font-medium mb-2" htmlFor="password">
                  Password
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="••••••••"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-bold py-3 px-4 rounded-lg shadow-lg transition-all duration-300 transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 mt-4"
              >
                {authForm === 'login' ? 'Sign In' : 'Sign Up'}
              </button>
            </form>

            <div className="mt-6 text-center text-sm text-gray-500">
              {authForm === 'login'
                ? "Don't have an account? "
                : "Already have an account? "}
              <button
                onClick={() => setAuthForm(authForm === 'login' ? 'register' : 'login')}
                className="font-medium text-blue-600 hover:text-blue-800 underline"
              >
                {authForm === 'login' ? 'Sign up' : 'Sign in'}
              </button>
            </div>
          </div>
        ) : (
          <div className="animate-fadeIn">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden mb-6 transition-all duration-300">
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4">
                <h2 className="text-white text-lg font-semibold flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clipRule="evenodd" />
                  </svg>
                  Your Tasks Assistant
                </h2>
              </div>

              <div className="p-4 h-[60vh] overflow-y-auto">
                {messages.length === 0 ? (
                  <div className="h-full flex flex-col items-center justify-center text-center p-4 text-gray-500">
                    <div className="mb-6 transform transition-transform duration-500 hover:scale-110">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-blue-400 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-semibold text-gray-700 mb-2">Welcome to Todo AI!</h3>
                    <p className="mb-4 max-w-md">I'm your AI assistant for managing tasks. How can I help you today?</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-lg">
                      {[
                        "Add a task to buy groceries",
                        "Show me all my tasks",
                        "What's pending?",
                        "Mark task 3 as complete"
                      ].map((suggestion, idx) => (
                        <div
                          key={idx}
                          className="bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-lg p-3 text-sm cursor-pointer transition-all duration-200 hover:shadow-sm"
                          onClick={() => setInputValue(suggestion)}
                        >
                          <span className="text-blue-700">{suggestion}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {messages.map((message) => (
                      <div
                        key={message.id}
                        className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} fade-in`}
                      >
                        <div
                          className={`max-w-[85%] rounded-2xl p-4 shadow-sm ${
                            message.role === 'user'
                              ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-br-none'
                              : 'bg-gray-100 text-gray-800 rounded-bl-none'
                          }`}
                        >
                          <div className="flex items-start">
                            {message.role !== 'user' && (
                              <div className="mr-3 flex-shrink-0">
                                <div className="bg-gradient-to-r from-purple-500 to-indigo-600 w-8 h-8 rounded-full flex items-center justify-center">
                                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-white" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clipRule="evenodd" />
                                  </svg>
                                </div>
                              </div>
                            )}
                            <div className="break-words">
                              {(() => {
                                // Check if this is a task list message
                                if (message.content.includes('Task #')) {
                                  // Parse task list from message content
                                  const taskRegex = /Task #(\d+):\s*'([^']+)' \(([^)]+)\)/g;
                                  const tasks = [];
                                  let match;

                                  while ((match = taskRegex.exec(message.content)) !== null) {
                                    tasks.push({
                                      id: match[1],
                                      title: match[2],
                                      status: match[3]
                                    });
                                  }

                                  if (tasks.length > 0) {
                                    return (
                                      <div className="w-full">
                                        <p className="mb-3 font-medium">{message.content.split(':')[0]}:</p>
                                        <div className="overflow-x-auto">
                                          <table className="min-w-full divide-y divide-gray-200 rounded-lg overflow-hidden">
                                            <thead className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
                                              <tr>
                                                <th scope="col" className="px-4 py-2 text-left text-xs font-medium uppercase tracking-wider">ID</th>
                                                <th scope="col" className="px-4 py-2 text-left text-xs font-medium uppercase tracking-wider">Title</th>
                                                <th scope="col" className="px-4 py-2 text-left text-xs font-medium uppercase tracking-wider">Status</th>
                                              </tr>
                                            </thead>
                                            <tbody className="bg-white divide-y divide-gray-200">
                                              {tasks.map((task, idx) => (
                                                <tr key={idx} className={`hover:bg-gray-50 transition-colors duration-200 ${idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}`}>
                                                  <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">#{task.id}</td>
                                                  <td className="px-4 py-3 text-sm text-gray-700 max-w-xs truncate" title={task.title}>{task.title}</td>
                                                  <td className="px-4 py-3 whitespace-nowrap">
                                                    <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                                      task.status === 'completed'
                                                        ? 'bg-green-100 text-green-800'
                                                        : 'bg-yellow-100 text-yellow-800'
                                                    }`}>
                                                      {task.status}
                                                    </span>
                                                  </td>
                                                </tr>
                                              ))}
                                            </tbody>
                                          </table>
                                        </div>
                                      </div>
                                    );
                                  }
                                }

                                // Default rendering for non-task messages
                                return message.content.split('\n').map((line, i) => (
                                  <p key={i} className={i > 0 ? 'mt-1' : ''}>{line}</p>
                                ));
                              })()}
                            </div>
                            {message.role === 'user' && (
                              <div className="ml-3 flex-shrink-0">
                                <div className="bg-gradient-to-r from-blue-400 to-blue-500 w-8 h-8 rounded-full flex items-center justify-center">
                                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-white" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                                  </svg>
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                    <div ref={messagesEndRef} />
                    {isLoading && (
                      <div className="flex justify-start fade-in">
                        <div className="bg-gray-100 text-gray-800 rounded-2xl p-4 max-w-[85%] rounded-bl-none">
                          <div className="flex items-center">
                            <div className="mr-3 flex-shrink-0">
                              <div className="bg-gradient-to-r from-purple-500 to-indigo-600 w-8 h-8 rounded-full flex items-center justify-center">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-white" viewBox="0 0 20 20" fill="currentColor">
                                  <path fillRule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clipRule="evenodd" />
                                </svg>
                              </div>
                            </div>
                            <div className="flex space-x-2">
                              <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce"></div>
                              <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce delay-100"></div>
                              <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce delay-200"></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            <form onSubmit={handleSubmit} className="flex gap-3 animate-fadeIn">
              <div className="relative flex-grow">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Type your message here..."
                  className="w-full pl-4 pr-12 py-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all shadow-sm"
                  disabled={isLoading}
                />
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>
              <button
                type="submit"
                disabled={isLoading || !inputValue.trim()}
                className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-medium py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                </svg>
              </button>
            </form>

            {/* Task Display Panel */}
            {messages.length > 0 && (
              <div className="mt-8 bg-white rounded-2xl shadow-xl overflow-hidden animate-fadeIn">
                <div className="bg-gradient-to-r from-green-500 to-teal-600 p-4">
                  <h2 className="text-white text-lg font-semibold flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                    </svg>
                    Your Tasks Overview
                  </h2>
                </div>

                <div className="p-4">
                  {(() => {
                    // Extract all tasks from messages and track changes
                    const allTasks: { [key: string]: { id: string; title: string; status: string } } = {};

                    // Process all messages to track task changes
                    for (let i = 0; i < messages.length; i++) {
                      const message = messages[i];

                      // Skip user messages
                      if (message.role === 'user') continue;

                      // Check if this is a task list message
                      if (message.content.includes('Task #')) {
                        const taskRegex = /Task #(\d+):\s*'([^']+)' \(([^)]+)\)/g;
                        let match;

                        while ((match = taskRegex.exec(message.content)) !== null) {
                          const taskId = match[1];
                          allTasks[taskId] = {
                            id: taskId,
                            title: match[2],
                            status: match[3]
                          };
                        }
                      }

                      // Check if this is a task completion message
                      if (message.content.includes("marked the task") && message.content.includes("as completed")) {
                        const taskMatch = /marked the task '(.+)' as completed/.exec(message.content);
                        if (taskMatch) {
                          // Find the task ID by title
                          for (const id in allTasks) {
                            if (allTasks[id] && allTasks[id].title === taskMatch[1]) {
                              allTasks[id].status = 'completed';
                              break;
                            }
                          }
                        }
                      }

                      // Check if this is a task deletion message
                      if (message.content.includes("deleted the task")) {
                        const taskMatch = /deleted the task '(.+)'\./.exec(message.content);
                        if (taskMatch) {
                          // Find the task ID by title and remove it
                          for (const id in allTasks) {
                            if (allTasks[id] && allTasks[id].title === taskMatch[1]) {
                              delete allTasks[id];
                              break;
                            }
                          }
                        }
                      }

                      // Check if this is a task addition message
                      if (message.content.includes("added the task")) {
                        const taskMatch = /added the task '(.+)'/.exec(message.content);
                        if (taskMatch) {
                          // For new tasks, we need to assign a temporary ID or wait for a refresh
                          // Since we don't get the actual ID from the response, we'll need to
                          // rely on the next "show tasks" command to get the full list with IDs
                          // For now, we'll skip adding it until it appears in a task list
                        }
                      }

                      // Check if this is a general response that might contain a new task ID
                      // Look for patterns where the AI might return the new task with its ID
                      if (message.content.includes("I've added the task") && message.content.includes("to your list")) {
                        // This is tricky without knowing the actual ID assigned by the backend
                        // The most reliable way is to show a hint that a task was added
                        // but wait for the next task list to show the actual task with ID
                      }
                    }

                    // Convert object to array and sort
                    const taskArray = Object.values(allTasks);

                    if (taskArray.length > 0) {
                      return (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200 rounded-lg overflow-hidden">
                            <thead className="bg-gradient-to-r from-green-500 to-teal-600 text-white">
                              <tr>
                                <th scope="col" className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider">ID</th>
                                <th scope="col" className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider">Title</th>
                                <th scope="col" className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider">Status</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {taskArray
                                .sort((a, b) => parseInt(a.id) - parseInt(b.id)) // Sort by ID
                                .map((task, idx) => (
                                <tr
                                  key={task.id}
                                  className={`hover:bg-gray-50 transition-colors duration-200 animate-fadeIn ${idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}`}
                                  style={{ animationDelay: `${idx * 0.05}s` }}
                                >
                                  <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">#{task.id}</td>
                                  <td className="px-4 py-3 text-sm text-gray-700 max-w-xs truncate" title={task.title}>{task.title}</td>
                                  <td className="px-4 py-3 whitespace-nowrap">
                                    <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                      task.status === 'completed'
                                        ? 'bg-green-100 text-green-800'
                                        : 'bg-yellow-100 text-yellow-800'
                                    }`}>
                                      {task.status}
                                    </span>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      );
                    } else {
                      return (
                        <div className="text-center py-8 text-gray-500">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-300 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                          </svg>
                          <p>No tasks found. Add a task to get started!</p>
                        </div>
                      );
                    }
                  })()}
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}