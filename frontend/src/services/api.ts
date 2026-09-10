import axios, { AxiosError } from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface PredictionRequest {
  age: number;
  monthly_income: number;
  years_at_company: number;
  years_in_current_role: number;
  years_with_curr_manager: number;
  total_working_years: number;
  job_satisfaction: number;
  work_life_balance: number;
  job_role: string;
  department: string;
  distance_from_home: number;
  over_time: string;
}

export interface PredictionResponse {
  attrition_risk: boolean;
  probability: number;
  risk_level: "Low" | "Medium" | "High";
  confidence: number;
}

export interface Employee {
  id: number;
  name: string;
  department: string;
  job_role: string;
  age: number;
  gender: string;
  monthly_income: number;
  years_at_company: number;
  job_satisfaction: number;
  work_life_balance: number;
  created_at: string;
  updated_at: string;
}

export interface ModelMetrics {
  model_version: string;
  model_name: string;
  training_date: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  roc_auc: number;
}

export const apiService = {
  // Predictions
  async predictSingle(data: PredictionRequest): Promise<PredictionResponse> {
    try {
      const response = await apiClient.post<PredictionResponse>(
        "/api/predict",
        data,
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  async predictBatch(
    file: File,
  ): Promise<{
    processed_count: number;
    success_count: number;
    error_count: number;
  }> {
    try {
      const formData = new FormData();
      formData.append("file", file);
      const response = await apiClient.post("/api/predict/batch", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  async getModelMetrics(): Promise<ModelMetrics> {
    try {
      const response = await apiClient.get<ModelMetrics>("/api/model/metrics");
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Employees
  async listEmployees(
    skip = 0,
    limit = 50,
    department?: string,
  ): Promise<Employee[]> {
    try {
      const params: Record<string, any> = { skip, limit };
      if (department) params.department = department;
      const response = await apiClient.get<Employee[]>("/api/employees", {
        params,
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  async getEmployee(id: number): Promise<Employee> {
    try {
      const response = await apiClient.get<Employee>(`/api/employees/${id}`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  async createEmployee(data: Partial<Employee>): Promise<Employee> {
    try {
      const response = await apiClient.post<Employee>("/api/employees", data);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  async updateEmployee(id: number, data: Partial<Employee>): Promise<Employee> {
    try {
      const response = await apiClient.put<Employee>(
        `/api/employees/${id}`,
        data,
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  async deleteEmployee(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/employees/${id}`);
    } catch (error) {
      throw this.handleError(error);
    }
  },

  async getDepartmentStats(department: string): Promise<any> {
    try {
      const response = await apiClient.get(
        `/api/employees/department/${department}/stats`,
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      await apiClient.get("/api/health");
      return true;
    } catch {
      return false;
    }
  },

  // Error handling
  handleError(error: unknown): Error {
    if (error instanceof AxiosError) {
      const message =
        error.response?.data?.detail || error.message || "An error occurred";
      return new Error(message);
    }
    return error instanceof Error
      ? error
      : new Error("An unknown error occurred");
  },
};
