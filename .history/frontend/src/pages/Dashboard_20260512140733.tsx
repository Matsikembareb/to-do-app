import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import type { Todo, CreateTodoRequest } from '../types/types';
import { todoService } from '../services/api';
import { LoadingSpinner } from '../components/LoadingSpinner';

export const Dashboard: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [newTodoDescription, setNewTodoDescription] = useState('');
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  // Fetch todos on mount
  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async (): Promise<void> => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await todoService.getAllTodos();
      // Handle both wrapped response { data: [] } and direct array []
      const todosData = response.data || response || [];
      setTodos(Array.isArray(todosData) ? todosData : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch todos');
      setTodos([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddTodo = async (e: React.FormEvent): Promise<void> => {
    e.preventDefault();
    if (!newTodoTitle.trim()) return;

    try {
      const createRequest: CreateTodoRequest = {
        title: newTodoTitle,
        description: newTodoDescription,
      };
      const response = await todoService.createTodo(createRequest);
      // Handle both wrapped response { data: todo } and direct todo
      const newTodo = response.data || response;
      if (newTodo && typeof newTodo === 'object') {
        setTodos([...todos, newTodo as Todo]);
        setNewTodoTitle('');
        setNewTodoDescription('');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create todo');
    }
  };

  const handleToggleTodo = async (todo: Todo): Promise<void> => {
    try {
      const response = await todoService.updateTodo(todo.id, {
        completed: !todo.completed,
      });
      setTodos(todos.map((t) => (t.id === todo.id ? response.data : t)));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update todo');
    }
  };

  const handleDeleteTodo = async (id: number): Promise<void> => {
    try {
      await todoService.deleteTodo(id);
      setTodos(todos.filter((t) => t.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete todo');
    }
  };

  const handleLogout = (): void => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-6 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Muzukuru Todos</h1>
            <p className="text-gray-600 mt-1">Welcome, {user?.username}</p>
          </div>
          <button
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded-md font-medium hover:bg-red-700 transition"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* Add Todo Form */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Add New Todo</h2>
          <form onSubmit={handleAddTodo} className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                Title
              </label>
              <input
                id="title"
                type="text"
                value={newTodoTitle}
                onChange={(e) => setNewTodoTitle(e.target.value)}
                placeholder="Enter todo title"
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                Description (optional)
              </label>
              <textarea
                id="description"
                value={newTodoDescription}
                onChange={(e) => setNewTodoDescription(e.target.value)}
                placeholder="Enter todo description"
                rows={3}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-green-600 text-white py-2 px-4 rounded-md font-medium hover:bg-green-700 transition"
            >
              Add Todo
            </button>
          </form>
        </div>

        {/* Todos List */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">My Todos</h2>

          {isLoading ? (
            <LoadingSpinner />
          ) : todos.length === 0 ? (
            <p className="text-gray-600 text-center py-8">No todos yet. Create one above!</p>
          ) : (
            <ul className="space-y-2">
              {todos.map((todo) => (
                <li
                  key={todo.id}
                  className="flex items-start gap-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition"
                >
                  <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={() => handleToggleTodo(todo)}
                    className="mt-1 w-5 h-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
                  />
                  <div className="flex-1">
                    <p className={`font-medium ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                      {todo.title}
                    </p>
                    {todo.description && (
                      <p className="text-gray-600 text-sm mt-1">{todo.description}</p>
                    )}
                    <p className="text-xs text-gray-400 mt-2">
                      Created: {new Date(todo.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <button
                    onClick={() => handleDeleteTodo(todo.id)}
                    className="text-red-600 hover:text-red-700 font-medium px-3 py-1 rounded hover:bg-red-50 transition"
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
    </div>
  );
};
