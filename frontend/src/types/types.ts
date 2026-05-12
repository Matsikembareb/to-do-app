// User and Auth types
export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

export interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  register: (username: string, email: string, password: string) => Promise<void>;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

// Todo types
export interface Todo {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface CreateTodoRequest {
  title: string;
  description: string;
}

export interface UpdateTodoRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

// API Error type
export interface ApiError {
  error: string;
  message: string;
}
