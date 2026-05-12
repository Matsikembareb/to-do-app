import type { AuthResponse, Todo, CreateTodoRequest, UpdateTodoRequest } from '../types/types';

const API_BASE_URL = 'http://localhost:5000/api';

// Helper to get token from localStorage
function getToken(): string | null {
  return localStorage.getItem('token');
}

// Helper to make fetch requests with error handling
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Add auth token if available
  const token = getToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error: { message?: string } = await response.json();
    throw new Error(error.message || `HTTP error! status: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

// Auth endpoints
export const authService = {
  register: async (username: string, email: string, password: string): Promise<AuthResponse> => {
    return fetchApi<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
  },

  login: async (username: string, password: string): Promise<AuthResponse> => {
    return fetchApi<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  },
};

// Todo endpoints
export const todoService = {
  getAllTodos: async (): Promise<{ data: Todo[] }> => {
    return fetchApi<{ data: Todo[] }>('/todos', {
      method: 'GET',
    });
  },

  createTodo: async (data: CreateTodoRequest): Promise<{ data: Todo }> => {
    return fetchApi<{ data: Todo }>('/todos', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  getTodoById: async (id: number): Promise<{ data: Todo }> => {
    return fetchApi<{ data: Todo }>(`/todos/${id}`, {
      method: 'GET',
    });
  },

  updateTodo: async (id: number, data: UpdateTodoRequest): Promise<{ data: Todo }> => {
    return fetchApi<{ data: Todo }>(`/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  deleteTodo: async (id: number): Promise<void> => {
    await fetchApi<void>(`/todos/${id}`, {
      method: 'DELETE',
    });
  },
};
